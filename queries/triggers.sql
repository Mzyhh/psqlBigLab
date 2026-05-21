CREATE OR REPLACE FUNCTION check_collection_has_items()
RETURNS TRIGGER AS $$
DECLARE
    item_count INTEGER;
BEGIN
    SELECT COUNT(*)
    INTO item_count
    FROM "Items"
    WHERE collection_id = NEW.collection_id;

    IF item_count = 0 THEN
        RAISE EXCEPTION 'Нельзя установить цену для коллекции "%" (id=%): в коллекции нет экспонатов',
            (SELECT name FROM Collections WHERE id = NEW.collection_id),
            NEW.collection_id
            USING ERRCODE = '23000';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER prevent_price_for_empty_collection
BEFORE INSERT OR UPDATE ON "PricesXCollections"
FOR EACH ROW
EXECUTE FUNCTION check_collection_has_items();