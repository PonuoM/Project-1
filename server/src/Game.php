<?php
declare(strict_types=1);

final class Game
{
    public static function state(int $accountId): array
    {
        $hero = self::hero($accountId, false);
        $equipped = self::equipped($accountId);
        $power = self::power($equipped);
        $now = now_ms();

        $stmt = db()->prepare(
            "SELECT id, unlock_at FROM boxes
             WHERE account_id = ? AND opened_at IS NULL AND type = 'gold' ORDER BY id"
        );
        $stmt->execute([$accountId]);
        $gold = [];
        foreach ($stmt->fetchAll() as $row) {
            $unlockAt = dt_to_ms($row['unlock_at']);
            $gold[] = ['id' => (int) $row['id'], 'unlockAt' => $unlockAt, 'ready' => $unlockAt <= $now];
        }

        $stmt = db()->prepare(
            "SELECT COUNT(*) FROM boxes WHERE account_id = ? AND opened_at IS NULL AND type = 'wood'"
        );
        $stmt->execute([$accountId]);

        $stage = (int) $hero['stage'];
        return [
            'serverTime' => $now,
            'hero' => [
                'cls'           => $hero['class'],
                'stage'         => $stage,
                'stageKills'    => (int) $hero['stage_kills'],
                'killsPerStage' => Rules::KILLS_PER_STAGE,
                'gold'          => (int) $hero['gold'],
                'totalKills'    => (int) $hero['total_kills'],
                'power'         => $power,
            ],
            'rates' => [
                'killMs'      => Rules::killMs($power, $stage),
                'goldPerKill' => Rules::goldPerKill($stage),
                'canAdvance'  => Rules::canAdvance($power, $stage),
            ],
            'equipped' => $equipped,
            'boxes'    => ['wood' => (int) $stmt->fetchColumn(), 'gold' => $gold],
            'limits'   => ['offlineCapMs' => Rules::OFFLINE_CAP_MS],
        ];
    }

    /** Credit everything earned since the last sync, using server time only. */
    public static function sync(int $accountId): array
    {
        $delta = self::transaction(function () use ($accountId) {
            return self::settle($accountId, self::hero($accountId, true));
        });
        return ['delta' => $delta, 'state' => self::state($accountId)];
    }

    /**
     * Credit kills, gold and drops up to now at the current power. Runs inside a transaction with the hero
     * row locked, and before anything that changes power, so new gear never applies to time already passed.
     */
    private static function settle(int $accountId, array $hero): array
    {
        $power = self::power(self::equipped($accountId));
        $now = now_ms();
        $elapsed = max(0, $now - dt_to_ms($hero['last_sync_at']));
        $credited = min($elapsed, Rules::OFFLINE_CAP_MS);
        $carry = $elapsed > Rules::OFFLINE_CAP_MS ? 0 : (int) $hero['carry_ms'];

        $sim = self::simulate($power, (int) $hero['stage'], (int) $hero['stage_kills'], $credited + $carry);

        db()->prepare(
            'UPDATE heroes SET stage = ?, stage_kills = ?, gold = gold + ?, total_kills = total_kills + ?,
             carry_ms = ?, last_sync_at = ? WHERE account_id = ?'
        )->execute([
            $sim['stage'], $sim['stageKills'], $sim['gold'], $sim['kills'],
            $sim['carryMs'], ms_to_dt($now), $accountId,
        ]);
        self::insertBoxes($accountId, $sim['drops'], $now);

        return [
            'elapsedMs'  => $elapsed,
            'creditedMs' => $credited,
            'capped'     => $elapsed > Rules::OFFLINE_CAP_MS,
            'kills'      => $sim['kills'],
            'gold'       => $sim['gold'],
            'wood'       => $sim['wood'],
            'goldBoxes'  => $sim['goldBoxes'],
            'stageFrom'  => (int) $hero['stage'],
            'stageTo'    => $sim['stage'],
        ];
    }

    public static function openBox(int $accountId, string $type, ?int $boxId): array
    {
        if ($type !== 'wood' && $type !== 'gold') {
            throw new ApiError(400, 'bad_box_type');
        }

        $result = self::transaction(function () use ($accountId, $type, $boxId) {
            $pdo = db();
            $hero = self::hero($accountId, true);
            if ($type === 'wood') {
                $stmt = $pdo->prepare(
                    "SELECT id, stage, unlock_at FROM boxes
                     WHERE account_id = ? AND opened_at IS NULL AND type = 'wood' ORDER BY id LIMIT 1 FOR UPDATE"
                );
                $stmt->execute([$accountId]);
            } else {
                $stmt = $pdo->prepare(
                    "SELECT id, stage, unlock_at FROM boxes
                     WHERE id = ? AND account_id = ? AND opened_at IS NULL AND type = 'gold' FOR UPDATE"
                );
                $stmt->execute([$boxId ?? 0, $accountId]);
            }
            $box = $stmt->fetch();
            if (!$box) {
                throw new ApiError(409, 'no_box');
            }
            $now = now_ms();
            if ($type === 'gold' && dt_to_ms($box['unlock_at']) > $now) {
                throw new ApiError(409, 'not_ready');
            }

            self::settle($accountId, $hero);
            $powerBefore = self::power(self::equipped($accountId));
            $loot = self::lootContext($accountId, $hero);
            $item = self::grantItem($accountId, $type, (int) $box['id'], (int) $box['stage'], $now, $loot);
            $pdo->prepare('UPDATE boxes SET opened_at = ? WHERE id = ?')->execute([ms_to_dt($now), $box['id']]);
            self::creditSales($accountId, $loot);
            return ['item' => $item, 'powerBefore' => $powerBefore, 'autoSold' => self::soldSummary($loot)];
        });

        $state = self::state($accountId);
        return $result + ['powerAfter' => $state['hero']['power'], 'state' => $state];
    }

    public static function openAllWood(int $accountId): array
    {
        $result = self::transaction(function () use ($accountId) {
            $pdo = db();
            $hero = self::hero($accountId, true);
            $stmt = $pdo->prepare(
                "SELECT id, stage FROM boxes
                 WHERE account_id = ? AND opened_at IS NULL AND type = 'wood' ORDER BY id LIMIT " . Rules::OPEN_ALL_LIMIT . ' FOR UPDATE'
            );
            $stmt->execute([$accountId]);
            $boxes = $stmt->fetchAll();
            if (!$boxes) {
                throw new ApiError(409, 'no_box');
            }

            self::settle($accountId, $hero);
            $now = now_ms();
            $powerBefore = self::power(self::equipped($accountId));
            $loot = self::lootContext($accountId, $hero);
            $byRarity = [0, 0, 0, 0, 0];
            $best = null;
            $markOpened = $pdo->prepare('UPDATE boxes SET opened_at = ? WHERE id = ?');
            foreach ($boxes as $box) {
                $item = self::grantItem($accountId, 'wood', (int) $box['id'], (int) $box['stage'], $now, $loot);
                $markOpened->execute([ms_to_dt($now), $box['id']]);
                $byRarity[$item['rarity']]++;
                if ($best === null || $item['rarity'] > $best['rarity']
                    || ($item['rarity'] === $best['rarity'] && $item['power'] > $best['power'])) {
                    $best = $item;
                }
            }
            self::creditSales($accountId, $loot);
            return [
                'opened'      => count($boxes),
                'byRarity'    => $byRarity,
                'best'        => $best,
                'powerBefore' => $powerBefore,
                'autoSold'    => self::soldSummary($loot),
            ];
        });

        $state = self::state($accountId);
        return $result + ['powerAfter' => $state['hero']['power'], 'state' => $state];
    }

    /** Unequipped items, newest first, with what they sell for. Equipped gear is in state(). */
    public static function inventory(int $accountId): array
    {
        $stmt = db()->prepare(
            'SELECT id, slot, rarity, power, name_key, created_at FROM items
             WHERE account_id = ? AND equipped = 0 ORDER BY id DESC'
        );
        $stmt->execute([$accountId]);
        $items = [];
        foreach ($stmt->fetchAll() as $row) {
            $item = self::itemRow($row);
            $item['sellValue'] = Rules::sellValue($item['power'], $item['rarity']);
            $item['createdAt'] = dt_to_ms($row['created_at']);
            $items[] = $item;
        }

        $stmt = db()->prepare('SELECT auto_sell FROM heroes WHERE account_id = ?');
        $stmt->execute([$accountId]);
        $mask = (int) $stmt->fetchColumn();
        $autoSell = [];
        for ($r = 0; $r <= Rules::AUTO_SELL_MAX_RARITY; $r++) {
            if ($mask & (1 << $r)) {
                $autoSell[] = $r;
            }
        }

        return [
            'items'       => $items,
            'capacity'    => Rules::BAG_CAPACITY,
            'autoSell'    => $autoSell,
            'autoSellMax' => Rules::AUTO_SELL_MAX_RARITY,
        ];
    }

    /** Swap a bag item into its slot; the previously equipped item goes back to the bag. */
    public static function equip(int $accountId, int $itemId): array
    {
        self::transaction(function () use ($accountId, $itemId) {
            $pdo = db();
            $hero = self::hero($accountId, true);
            $stmt = $pdo->prepare('SELECT slot FROM items WHERE id = ? AND account_id = ? AND equipped = 0');
            $stmt->execute([$itemId, $accountId]);
            $slot = $stmt->fetchColumn();
            if ($slot === false) {
                throw new ApiError(409, 'no_item');
            }
            self::settle($accountId, $hero);
            $pdo->prepare('UPDATE items SET equipped = 0 WHERE account_id = ? AND slot = ? AND equipped = 1')
                ->execute([$accountId, $slot]);
            $pdo->prepare('UPDATE items SET equipped = 1 WHERE id = ?')->execute([$itemId]);
        });

        return ['state' => self::state($accountId), 'inventory' => self::inventory($accountId)];
    }

    /** Sell bag items for gold. Equipped items and ids that are not ours are ignored. */
    public static function sell(int $accountId, array $ids): array
    {
        $ids = array_values(array_unique(array_filter(array_map('intval', $ids), function ($id) {
            return $id > 0;
        })));
        if (!$ids || count($ids) > 500) {
            throw new ApiError(400, 'bad_items');
        }

        $sold = self::transaction(function () use ($accountId, $ids) {
            $pdo = db();
            self::hero($accountId, true);
            $marks = implode(',', array_fill(0, count($ids), '?'));
            $stmt = $pdo->prepare(
                "SELECT id, power, rarity FROM items WHERE account_id = ? AND equipped = 0 AND id IN ($marks) FOR UPDATE"
            );
            $stmt->execute(array_merge([$accountId], $ids));
            $rows = $stmt->fetchAll();
            if (!$rows) {
                throw new ApiError(409, 'no_item');
            }
            $gold = 0;
            foreach ($rows as $row) {
                $gold += Rules::sellValue((int) $row['power'], (int) $row['rarity']);
            }
            $found = array_column($rows, 'id');
            $pdo->prepare('DELETE FROM items WHERE id IN (' . implode(',', array_fill(0, count($found), '?')) . ')')
                ->execute($found);
            $pdo->prepare('UPDATE heroes SET gold = gold + ? WHERE account_id = ?')->execute([$gold, $accountId]);
            return ['count' => count($rows), 'gold' => $gold];
        });

        return ['sold' => $sold, 'state' => self::state($accountId), 'inventory' => self::inventory($accountId)];
    }

    /** Which rarities to sell on drop. Epic and legendary can never be auto-sold. */
    public static function setAutoSell(int $accountId, array $rarities): array
    {
        $mask = 0;
        foreach ($rarities as $r) {
            $r = (int) $r;
            if ($r < 0 || $r > Rules::AUTO_SELL_MAX_RARITY) {
                throw new ApiError(400, 'bad_rarity');
            }
            $mask |= 1 << $r;
        }
        db()->prepare('UPDATE heroes SET auto_sell = ? WHERE account_id = ?')->execute([$mask, $accountId]);
        return self::inventory($accountId);
    }

    /**
     * Walk stage by stage through the credited time. Power is constant here because
     * gear only changes when the player opens boxes.
     */
    private static function simulate(int $power, int $stage, int $stageKills, int $ms): array
    {
        $kills = 0;
        $gold = 0;
        $wood = 0;
        $goldBoxes = 0;
        $drops = [];

        while (true) {
            $killMs = Rules::killMs($power, $stage);
            $need = Rules::KILLS_PER_STAGE - $stageKills;
            $advancing = Rules::canAdvance($power, $stage) && $need * $killMs <= $ms;
            $n = $advancing ? $need : intdiv($ms, $killMs);

            $kills += $n;
            $gold += $n * Rules::goldPerKill($stage);
            $w = Rules::rollCount($n, Rules::P_WOOD);
            $g = Rules::rollCount($n, Rules::P_GOLD);
            $wood += $w;
            $goldBoxes += $g;
            if ($w > 0) {
                $drops[] = ['wood', $stage, $w];
            }
            if ($g > 0) {
                $drops[] = ['gold', $stage, $g];
            }
            $ms -= $n * $killMs;

            if (!$advancing) {
                $stageKills = min(Rules::KILLS_PER_STAGE, $stageKills + $n);
                break;
            }
            $stage++;
            $stageKills = 0;
        }

        return [
            'kills' => $kills, 'gold' => $gold, 'wood' => $wood, 'goldBoxes' => $goldBoxes,
            'stage' => $stage, 'stageKills' => $stageKills, 'carryMs' => $ms, 'drops' => $drops,
        ];
    }

    private static function insertBoxes(int $accountId, array $drops, int $now): void
    {
        $rows = [];
        $params = [];
        $created = ms_to_dt($now);
        $unlock = ms_to_dt($now + Rules::GOLD_UNLOCK_MS);
        foreach ($drops as $drop) {
            list($type, $stage, $count) = $drop;
            for ($i = 0; $i < $count; $i++) {
                $rows[] = '(?, ?, ?, ?, ?)';
                array_push($params, $accountId, $type, $stage, $created, $type === 'gold' ? $unlock : null);
            }
        }
        foreach (array_chunk($rows, 200) as $chunkIndex => $chunk) {
            $chunkParams = array_slice($params, $chunkIndex * 200 * 5, count($chunk) * 5);
            db()->prepare(
                'INSERT INTO boxes (account_id, type, stage, created_at, unlock_at) VALUES ' . implode(',', $chunk)
            )->execute($chunkParams);
        }
    }

    private static function lootContext(int $accountId, array $hero): array
    {
        $stmt = db()->prepare('SELECT COUNT(*) FROM items WHERE account_id = ? AND equipped = 0');
        $stmt->execute([$accountId]);
        return ['mask' => (int) $hero['auto_sell'], 'bag' => (int) $stmt->fetchColumn(), 'sold' => 0, 'gold' => 0];
    }

    /**
     * Roll an item and auto-equip it when it beats the current item in that slot. Whatever would go to the
     * bag (the new item, or the one it replaced) is sold instead when its rarity is set to auto-sell or the
     * bag is full.
     */
    private static function grantItem(int $accountId, string $boxType, int $boxId, int $stage, int $now, array &$loot): array
    {
        $pdo = db();
        $roll = Rules::rollItem($boxType, $stage);

        $stmt = $pdo->prepare('SELECT id, power, rarity FROM items WHERE account_id = ? AND slot = ? AND equipped = 1 FOR UPDATE');
        $stmt->execute([$accountId, $roll['slot']]);
        $current = $stmt->fetch();
        $equip = !$current || $roll['power'] > (int) $current['power'];

        $toBag = $equip ? $current : $roll;
        $sellToBag = $toBag && self::shouldSell($loot, (int) $toBag['rarity']);
        $soldFor = 0;
        if ($sellToBag) {
            $soldFor = Rules::sellValue((int) $toBag['power'], (int) $toBag['rarity']);
            $loot['sold']++;
            $loot['gold'] += $soldFor;
        } elseif ($toBag) {
            $loot['bag']++;
        }

        if ($equip && $current) {
            $pdo->prepare($sellToBag ? 'DELETE FROM items WHERE id = ?' : 'UPDATE items SET equipped = 0 WHERE id = ?')
                ->execute([$current['id']]);
        }

        $id = 0;
        if ($equip || !$sellToBag) {
            $pdo->prepare(
                'INSERT INTO items (account_id, slot, rarity, power, name_key, equipped, source_box_id, created_at)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
            )->execute([
                $accountId, $roll['slot'], $roll['rarity'], $roll['power'], $roll['name_key'],
                $equip ? 1 : 0, $boxId, ms_to_dt($now),
            ]);
            $id = (int) $pdo->lastInsertId();
        }

        return [
            'id'            => $id,
            'slot'          => $roll['slot'],
            'rarity'        => $roll['rarity'],
            'power'         => $roll['power'],
            'nameKey'       => $roll['name_key'],
            'equipped'      => $equip,
            'replacedPower' => $current ? (int) $current['power'] : 0,
            'soldFor'       => $equip ? 0 : $soldFor,
        ];
    }

    private static function shouldSell(array $loot, int $rarity): bool
    {
        return ($loot['mask'] & (1 << $rarity)) !== 0 || $loot['bag'] >= Rules::BAG_CAPACITY;
    }

    private static function creditSales(int $accountId, array $loot): void
    {
        if ($loot['gold'] > 0) {
            db()->prepare('UPDATE heroes SET gold = gold + ? WHERE account_id = ?')->execute([$loot['gold'], $accountId]);
        }
    }

    private static function soldSummary(array $loot): array
    {
        return ['count' => $loot['sold'], 'gold' => $loot['gold']];
    }

    /** Run $fn in a transaction; roll back and rethrow on any error. */
    private static function transaction(callable $fn)
    {
        $pdo = db();
        $pdo->beginTransaction();
        try {
            $result = $fn();
            $pdo->commit();
            return $result;
        } catch (Throwable $e) {
            $pdo->rollBack();
            throw $e;
        }
    }

    private static function itemRow(array $row): array
    {
        return [
            'id' => (int) $row['id'], 'slot' => $row['slot'], 'rarity' => (int) $row['rarity'],
            'power' => (int) $row['power'], 'nameKey' => $row['name_key'],
        ];
    }

    private static function hero(int $accountId, bool $forUpdate): array
    {
        $stmt = db()->prepare('SELECT * FROM heroes WHERE account_id = ?' . ($forUpdate ? ' FOR UPDATE' : ''));
        $stmt->execute([$accountId]);
        $hero = $stmt->fetch();
        if (!$hero) {
            throw new ApiError(404, 'no_hero');
        }
        return $hero;
    }

    private static function equipped(int $accountId): array
    {
        $stmt = db()->prepare(
            'SELECT id, slot, rarity, power, name_key FROM items WHERE account_id = ? AND equipped = 1'
        );
        $stmt->execute([$accountId]);
        $out = ['weapon' => null, 'armor' => null, 'ring' => null];
        foreach ($stmt->fetchAll() as $row) {
            $out[$row['slot']] = self::itemRow($row);
        }
        return $out;
    }

    private static function power(array $equipped): int
    {
        $power = Rules::BASE_POWER;
        foreach ($equipped as $item) {
            if ($item !== null) {
                $power += $item['power'];
            }
        }
        return $power;
    }
}
