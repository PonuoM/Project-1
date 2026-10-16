<?php
declare(strict_types=1);

date_default_timezone_set('UTC');

require __DIR__ . '/Rules.php';
require __DIR__ . '/Auth.php';
require __DIR__ . '/Game.php';

final class ApiError extends RuntimeException
{
    /** @var int */
    public $status;

    public function __construct(int $status, string $code)
    {
        parent::__construct($code);
        $this->status = $status;
    }
}

function config(): array
{
    static $config = null;
    if ($config === null) {
        $config = require __DIR__ . '/../config.php';
    }
    return $config;
}

function db(): PDO
{
    static $pdo = null;
    if ($pdo === null) {
        $c = config()['db'];
        $pdo = new PDO($c['dsn'], $c['user'], $c['pass'], [
            PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
            PDO::ATTR_EMULATE_PREPARES   => false,
        ]);
        $pdo->exec("SET time_zone = '+00:00'");
    }
    return $pdo;
}

/** Server clock in milliseconds. The only clock rewards are based on. */
function now_ms(): int
{
    return (int) round(microtime(true) * 1000);
}

function ms_to_dt(int $ms): string
{
    return gmdate('Y-m-d H:i:s', intdiv($ms, 1000)) . sprintf('.%03d', $ms % 1000);
}

function dt_to_ms(string $dt): int
{
    $parts = explode('.', $dt);
    $ms = isset($parts[1]) ? (int) str_pad(substr($parts[1], 0, 3), 3, '0') : 0;
    return strtotime($parts[0] . ' UTC') * 1000 + $ms;
}
