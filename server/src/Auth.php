<?php
declare(strict_types=1);

final class Auth
{
    /** Prototype login: one account per random device id. Steam/Google/LINE will link to the same account_id later. */
    public static function guest(string $deviceId): array
    {
        if (!preg_match('/^[A-Za-z0-9-]{16,64}$/', $deviceId)) {
            throw new ApiError(400, 'bad_device_id');
        }

        $pdo = db();
        $stmt = $pdo->prepare('SELECT id, token FROM accounts WHERE device_id = ?');
        $stmt->execute([$deviceId]);
        $row = $stmt->fetch();
        if ($row) {
            return ['accountId' => (int) $row['id'], 'token' => $row['token']];
        }

        $now = ms_to_dt(now_ms());
        $token = bin2hex(random_bytes(32));
        $pdo->beginTransaction();
        $pdo->prepare('INSERT INTO accounts (device_id, token, created_at) VALUES (?, ?, ?)')
            ->execute([$deviceId, $token, $now]);
        $accountId = (int) $pdo->lastInsertId();
        $pdo->prepare('INSERT INTO heroes (account_id, auto_sell, last_sync_at) VALUES (?, ?, ?)')
            ->execute([$accountId, Rules::AUTO_SELL_DEFAULT, $now]);
        self::grantStarterBoxes($accountId, now_ms());
        $pdo->commit();

        return ['accountId' => $accountId, 'token' => $token];
    }

    private static function grantStarterBoxes(int $accountId, int $nowMs): void
    {
        $insert = db()->prepare(
            'INSERT INTO boxes (account_id, type, stage, created_at, unlock_at) VALUES (?, ?, 1, ?, ?)'
        );
        for ($i = 0; $i < Rules::STARTER_WOOD; $i++) {
            $insert->execute([$accountId, 'wood', ms_to_dt($nowMs), null]);
        }
        $insert->execute([$accountId, 'gold', ms_to_dt($nowMs), ms_to_dt($nowMs + Rules::STARTER_GOLD_UNLOCK_MS)]);
    }

    public static function requireAccount(): int
    {
        $token = $_SERVER['HTTP_X_AUTH_TOKEN'] ?? '';
        if (!preg_match('/^[a-f0-9]{64}$/', $token)) {
            throw new ApiError(401, 'unauthorized');
        }
        $stmt = db()->prepare('SELECT id FROM accounts WHERE token = ?');
        $stmt->execute([$token]);
        $id = $stmt->fetchColumn();
        if ($id === false) {
            throw new ApiError(401, 'unauthorized');
        }
        return (int) $id;
    }
}
