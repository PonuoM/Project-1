<?php
// Defaults only. Put real credentials in config.local.php (git-ignored).
$config = [
    'db' => [
        'dsn'  => 'mysql:host=127.0.0.1;dbname=idle_loot;charset=utf8mb4',
        'user' => 'root',
        'pass' => '',
    ],
    'cors_origin' => '*',
];

$local = __DIR__ . '/config.local.php';
if (is_file($local)) {
    $config = array_replace_recursive($config, require $local);
}

return $config;
