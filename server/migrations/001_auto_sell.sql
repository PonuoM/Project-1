-- 2026-10-13: bag + auto-sell. For databases created before this column existed in schema.sql.
USE idle_loot;
ALTER TABLE heroes ADD COLUMN auto_sell TINYINT UNSIGNED NOT NULL DEFAULT 1 AFTER carry_ms;
