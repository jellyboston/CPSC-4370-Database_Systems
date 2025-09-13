-- TODO: Finish implementing the calculate_fine function 
CREATE OR REPLACE FUNCTION calculate_fine()
RETURNS TRIGGER AS $$
DECLARE
    days_overdue INT;
    fine_rate DECIMAL(10, 2) := 0.50;  -- Daily fine rate
    fine_due DECIMAL(10, 2);
BEGIN
    IF NEW.return_date > NEW.due_date THEN
        -- TODO IMPLEMENT FUNCTIONALITY HERE

    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- TODO: Add CREATE TRIGGER statement here