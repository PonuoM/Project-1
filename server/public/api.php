<?php
declare(strict_types=1);

require __DIR__ . '/../src/bootstrap.php';

header('Access-Control-Allow-Origin: ' . config()['cors_origin']);
header('Access-Control-Allow-Headers: Content-Type, X-Auth-Token');
header('Access-Control-Allow-Methods: POST, GET, OPTIONS');
header('Content-Type: application/json; charset=utf-8');

if (($_SERVER['REQUEST_METHOD'] ?? '') === 'OPTIONS') {
    http_response_code(204);
    exit;
}

function respond(int $status, array $payload): void
{
    http_response_code($status);
    echo json_encode($payload, JSON_UNESCAPED_UNICODE);
    exit;
}

$action = $_GET['a'] ?? '';
$body = json_decode((string) file_get_contents('php://input'), true);
if (!is_array($body)) {
    $body = [];
}

try {
    switch ($action) {
        case 'auth.guest':
            respond(200, Auth::guest((string) ($body['deviceId'] ?? '')));
            break;
        case 'state':
            respond(200, Game::state(Auth::requireAccount()));
            break;
        case 'sync':
            respond(200, Game::sync(Auth::requireAccount()));
            break;
        case 'box.open':
            $id = isset($body['id']) ? (int) $body['id'] : null;
            respond(200, Game::openBox(Auth::requireAccount(), (string) ($body['type'] ?? 'wood'), $id));
            break;
        case 'box.openAll':
            respond(200, Game::openAllWood(Auth::requireAccount()));
            break;
        case 'box.odds':
            respond(200, Rules::odds());
            break;
        case 'inventory':
            respond(200, Game::inventory(Auth::requireAccount()));
            break;
        case 'item.equip':
            respond(200, Game::equip(Auth::requireAccount(), (int) ($body['id'] ?? 0)));
            break;
        case 'item.sell':
            respond(200, Game::sell(Auth::requireAccount(), (array) ($body['ids'] ?? [])));
            break;
        case 'settings.autoSell':
            respond(200, Game::setAutoSell(Auth::requireAccount(), (array) ($body['rarities'] ?? [])));
            break;
        default:
            respond(404, ['error' => 'unknown_action']);
    }
} catch (ApiError $e) {
    respond($e->status, ['error' => $e->getMessage()]);
} catch (Throwable $e) {
    error_log('[idle-loot] ' . $e);
    respond(500, ['error' => 'server_error']);
}
