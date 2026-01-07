from alembic_utils.pg_function import PGFunction
from alembic_utils.pg_trigger import PGTrigger

TRIGGER_FUNCTION_SQL = """
RETURNS TRIGGER AS $$
BEGIN
    IF (TG_OP = 'INSERT' OR TG_OP = 'UPDATE') THEN
        IF (TG_OP = 'UPDATE') THEN
            UPDATE warehouse
            SET quantity = warehouse.quantity - OLD.quantity
            WHERE product_id = OLD.product_id;
        END IF;

        INSERT INTO warehouse (product_id, quantity)
        VALUES (NEW.product_id, NEW.quantity)
        ON CONFLICT (product_id) DO UPDATE
        SET quantity = warehouse.quantity + NEW.quantity;
    END IF;

    IF (TG_OP = 'DELETE') THEN
        UPDATE warehouse
        SET quantity = warehouse.quantity - OLD.quantity
        WHERE product_id = OLD.product_id;

        IF (SELECT quantity FROM warehouse WHERE product_id = OLD.product_id) < 0 THEN
            RAISE EXCEPTION 'Not enough supplies to remove the cargo';
        END IF;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
"""

update_warehouse_from_supplies = PGFunction(
    schema="public",
    signature="update_warehouse_from_supplies()",
    definition=TRIGGER_FUNCTION_SQL
)

trg_supplies_product_insert = PGTrigger(
    schema="public",
    signature="trigger_supplies_product_insert",
    on_entity="supplies_product",
    definition="""
        AFTER INSERT ON supplies_product
        FOR EACH ROW
        EXECUTE FUNCTION update_warehouse_from_supplies();
    """,
)

trg_supplies_product_update = PGTrigger(
    schema="public",
    signature="trigger_supplies_product_update",
    on_entity="supplies_product",
    definition="""
        AFTER UPDATE ON supplies_product
        FOR EACH ROW
        EXECUTE FUNCTION update_warehouse_from_supplies();
    """,
)

trg_supplies_product_delete = PGTrigger(
    schema="public",
    signature="trigger_supplies_product_delete",
    on_entity="supplies_product",
    definition="""
        AFTER DELETE ON supplies_product
        FOR EACH ROW
        EXECUTE FUNCTION update_warehouse_from_supplies();
    """,
)

TRIGGER_FUNCTION_SUPPLIES_SQL = """
RETURNS TRIGGER AS $$
BEGIN
       IF (TG_OP = 'UPDATE') THEN
            IF (NEW.draft != OLD.draft) THEN
                IF (NEW.draft = TRUE) THEN
                -- Проверяем, хватит ли запасов на складе для списания
                    IF NOT EXISTS (
                            SELECT 1
                            FROM supplies_product sp
                            JOIN warehouse w ON w.product_id = sp.product_id
                            WHERE sp.supplies_id = NEW.id AND w.quantity < sp.quantity
                        ) THEN
                            UPDATE warehouse w
                            SET quantity = w.quantity - sp.quantity
                            FROM supplies_product sp
                            WHERE sp.supplies_id = NEW.id AND w.product_id = sp.product_id;
                        ELSE
                        RAISE EXCEPTION 'There are not enough goods in the warehouse to process the document. ID %', NEW.id;
                    END IF;
                END IF;
                IF (NEW.draft = FALSE) THEN
                    UPDATE warehouse w
                    SET quantity = w.quantity + sp.quantity
                    FROM supplies_product sp
                    WHERE sp.supplies_id = 4 AND w.product_id = sp.product_id;
                END IF;
            END IF;
        END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
"""

update_warehouse_draft_supplies = PGFunction(
    schema="public",
    signature="update_warehouse_draft_supplies()",
    definition=TRIGGER_FUNCTION_SUPPLIES_SQL
)

trg_supplies_update = PGTrigger(
    schema="public",
    signature="trigger_supplies_update",
    on_entity="supplies",
    definition="""
        AFTER UPDATE ON supplies
        FOR EACH ROW
        EXECUTE FUNCTION update_warehouse_draft_supplies();
    """,
)
