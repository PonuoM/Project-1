<?php
declare(strict_types=1);

/**
 * Every balance number lives here. The client never computes rewards;
 * it only animates using the rates the server sends back.
 */
final class Rules
{
    const BASE_POWER      = 10;
    const WALK_MS         = 900;       // time between kills spent walking to the next monster
    const MIN_KILL_MS     = 600;
    const KILLS_PER_STAGE = 20;
    const ADVANCE_RATIO   = 0.35;      // power needed (vs next stage's enemy HP) to move on

    const P_WOOD = 0.015;              // wooden box chance per kill
    const P_GOLD = 0.0006;             // gold box chance per kill

    const GOLD_UNLOCK_MS = 30 * 60 * 1000;

    // First-session onboarding: new players hit the stage-3 wall within minutes, so they start with boxes
    // to open, plus one gold box that unlocks almost immediately to teach the timer.
    const STARTER_WOOD = 3;
    const STARTER_GOLD_UNLOCK_MS = 60 * 1000;
    const OFFLINE_CAP_MS = 8 * 60 * 60 * 1000;   // monthly pass will raise this to 12h
    const OPEN_ALL_LIMIT = 200;

    // Bag holds unequipped items. When it is full, new items that are not auto-equipped are sold
    // automatically so opening boxes never gets blocked.
    const BAG_CAPACITY = 80;
    const AUTO_SELL_DEFAULT = 0b00001;                // new players auto-sell common only
    const AUTO_SELL_MAX_RARITY = 2;                   // epic and legendary are never sold automatically
    const SELL_MULT = [1.0, 1.5, 2.5, 4.0, 6.0];

    const RARITY_MULT = [1.0, 1.4, 2.0, 3.0, 4.5];   // common, uncommon, rare, epic, legendary
    const RARITY_WEIGHTS = [
        'wood' => [600, 270, 100, 27, 3],
        'gold' => [0, 450, 350, 150, 50],
    ];

    const SLOTS = ['weapon', 'armor', 'ring'];
    const NAMES = [
        'weapon' => ['sword', 'axe', 'spear'],
        'armor'  => ['leather', 'chain', 'plate'],
        'ring'   => ['ring', 'amulet', 'charm'],
    ];

    public static function enemyHp(int $stage): float
    {
        return 20 * pow(1.13, $stage - 1);
    }

    public static function killMs(int $power, int $stage): int
    {
        $fight = (int) round(self::enemyHp($stage) / max(1, $power) * 1000);
        return max(self::MIN_KILL_MS, $fight + self::WALK_MS);
    }

    public static function goldPerKill(int $stage): int
    {
        return 1 + intdiv($stage * 3, 2);
    }

    public static function canAdvance(int $power, int $stage): bool
    {
        return $power >= self::enemyHp($stage + 1) * self::ADVANCE_RATIO;
    }

    public static function sellValue(int $power, int $rarity): int
    {
        return max(1, (int) round($power * self::SELL_MULT[$rarity]));
    }

    /** Published odds, shown to players before they open anything. Percent per rarity, 2 decimals. */
    public static function odds(): array
    {
        $boxes = [];
        foreach (self::RARITY_WEIGHTS as $type => $weights) {
            $sum = array_sum($weights);
            $boxes[$type] = array_map(function ($w) use ($sum) {
                return round($w / $sum * 100, 2);
            }, $weights);
        }
        return [
            'boxes'         => $boxes,
            'perKill'       => ['wood' => self::P_WOOD * 100, 'gold' => self::P_GOLD * 100],
            'goldUnlockMs'  => self::GOLD_UNLOCK_MS,
        ];
    }

    /** Integer count with the right expected value: floor(n*p) plus one more with the fractional chance. */
    public static function rollCount(int $n, float $p): int
    {
        $expected = $n * $p;
        $count = (int) floor($expected);
        if (self::rand01() < $expected - $count) {
            $count++;
        }
        return $count;
    }

    public static function rollItem(string $boxType, int $stage): array
    {
        $slot = self::SLOTS[random_int(0, count(self::SLOTS) - 1)];
        $names = self::NAMES[$slot];
        $rarity = self::pickWeighted(self::RARITY_WEIGHTS[$boxType]);
        $base = 2 + $stage * 1.2;
        $variance = 0.9 + self::rand01() * 0.2;
        return [
            'slot'     => $slot,
            'rarity'   => $rarity,
            'name_key' => $names[random_int(0, count($names) - 1)],
            'power'    => max(1, (int) round($base * self::RARITY_MULT[$rarity] * $variance)),
        ];
    }

    private static function pickWeighted(array $weights): int
    {
        $roll = random_int(1, (int) array_sum($weights));
        foreach ($weights as $index => $weight) {
            $roll -= $weight;
            if ($roll <= 0) {
                return $index;
            }
        }
        return 0;
    }

    private static function rand01(): float
    {
        return random_int(0, 999999) / 1000000;
    }
}
