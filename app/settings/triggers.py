from alembic_utils.pg_function import PGFunction
from alembic_utils.pg_trigger import PGTrigger

TRIGGER_FUNCTION_SQL = """
RETURNS TRIGGER AS $$
BEGIN
    IF (TG_OP = 'INSERT' OR TG_OP = 'UPDATE') THEN
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
