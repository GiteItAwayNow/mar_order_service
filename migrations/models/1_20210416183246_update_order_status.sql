-- upgrade --
ALTER TYPE orders__status ADD VALUE IF NOT EXISTS 'confirmed';
