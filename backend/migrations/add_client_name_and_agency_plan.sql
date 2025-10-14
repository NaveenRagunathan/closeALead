-- Migration: Add client_name to offers and update enterprise to agency
-- Date: 2025-10-14

-- Add client_name column to offers table
ALTER TABLE offers 
ADD COLUMN client_name VARCHAR(200);

-- Update existing enterprise plan users to agency plan
UPDATE users 
SET plan = 'agency' 
WHERE plan = 'enterprise';

-- Add index on client_name for faster searches (optional but recommended)
CREATE INDEX idx_offers_client_name ON offers(client_name) WHERE client_name IS NOT NULL;

-- Verify changes
SELECT 'Migration completed successfully' AS status;
