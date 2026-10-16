-- Prototype schema. All DATETIME values are UTC, written by PHP (never NOW()).
CREATE DATABASE IF NOT EXISTS idle_loot CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE idle_loot;

CREATE TABLE IF NOT EXISTS accounts (
  id          BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  device_id   VARCHAR(64) NOT NULL UNIQUE,   -- prototype guest login; Steam/Google/LINE links come later
  token       CHAR(64)    NOT NULL UNIQUE,
  created_at  DATETIME(3) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS heroes (
  account_id    BIGINT UNSIGNED PRIMARY KEY,
  class         VARCHAR(16)     NOT NULL DEFAULT 'melee',
  stage         INT UNSIGNED    NOT NULL DEFAULT 1,
  stage_kills   INT UNSIGNED    NOT NULL DEFAULT 0,
  gold          BIGINT UNSIGNED NOT NULL DEFAULT 0,
  total_kills   BIGINT UNSIGNED NOT NULL DEFAULT 0,
  carry_ms      INT UNSIGNED    NOT NULL DEFAULT 0,  -- leftover time that did not complete a kill
  auto_sell     TINYINT UNSIGNED NOT NULL DEFAULT 1, -- bit per rarity: sell new drops of that rarity unless equipped
  last_sync_at  DATETIME(3)     NOT NULL,
  CONSTRAINT fk_heroes_account FOREIGN KEY (account_id) REFERENCES accounts(id)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS boxes (
  id          BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  account_id  BIGINT UNSIGNED NOT NULL,
  type        ENUM('wood','gold') NOT NULL,
  stage       INT UNSIGNED NOT NULL,           -- stage it dropped on; scales item power
  created_at  DATETIME(3)  NOT NULL,
  unlock_at   DATETIME(3)  NULL,               -- gold boxes only
  opened_at   DATETIME(3)  NULL,
  KEY idx_boxes_unopened (account_id, opened_at, type, id)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS items (
  id             BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  account_id     BIGINT UNSIGNED NOT NULL,
  slot           ENUM('weapon','armor','ring') NOT NULL,
  rarity         TINYINT UNSIGNED NOT NULL,    -- 0 common .. 4 legendary
  power          INT UNSIGNED NOT NULL,
  name_key       VARCHAR(32)  NOT NULL,        -- client localizes
  equipped       TINYINT(1)   NOT NULL DEFAULT 0,
  source_box_id  BIGINT UNSIGNED NULL,
  created_at     DATETIME(3)  NOT NULL,
  KEY idx_items_slot (account_id, slot, equipped)
) ENGINE=InnoDB;
