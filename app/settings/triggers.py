from alembic_utils.pg_function import PGFunction
from alembic_utils.pg_trigger import PGTrigger

SUPPLIES_PRODUCT_SQL = """
RETURNS TRIGGER AS $$
DECLARE
    final_quantity INT;
    is_draft BOOLEAN;
BEGIN
    -- Skip change product quantity if draft supplies
    SELECT s.draft
    INTO is_draft
    FROM supplies s
    WHERE s.id = NEW.supplies_id;
    
    IF is_draft THEN
        RETURN NEW;
    END IF;
    IF (TG_OP = 'INSERT' OR TG_OP = 'UPDATE') THEN
        IF (TG_OP = 'UPDATE') THEN
            -- FOR UPDATE.
            SELECT p.quantity - OLD.quantity + NEW.quantity
            INTO final_quantity
            FROM product p
            WHERE p.id = NEW.product_id;
        ELSIF (TG_OP = 'INSERT') THEN
            -- FOR INSERT.
            SELECT p.quantity + NEW.quantity
            INTO final_quantity
            FROM product p
            WHERE p.id = NEW.product_id;
        ELSE
            -- FOR DELETE.
            SELECT p.quantity - OLD.quantity
            INTO final_quantity
            FROM product p
            WHERE p.id = NEW.product_id;
        END IF;

        -- CHECK: final_quantity >= 0
        IF final_quantity IS NULL THEN
            RAISE EXCEPTION 'Product not found.';
        ELSIF final_quantity < 0 THEN
            RAISE EXCEPTION 'Not enough products. Operation leads to a negative remainder';
        END IF;

        IF (TG_OP = 'UPDATE') THEN
            UPDATE product
            SET quantity = final_quantity
            WHERE id = NEW.product_id;
        ELSIF (TG_OP = 'INSERT') THEN
            UPDATE product
            SET quantity = final_quantity
            WHERE id = NEW.product_id;
        ELSE 
            UPDATE product
            SET quantity = final_quantity
            WHERE id = NEW.product_id;
        END IF;
    END IF;
 RETURN NEW;
END;
$$ LANGUAGE plpgsql;
"""

update_supplies_product_fn = PGFunction(
    schema="public",
    signature="update_supplies_product_fn()",
    definition=SUPPLIES_PRODUCT_SQL
)

supplies_product_insert_tg = PGTrigger(
    schema="public",
    signature="supplies_product_insert_tg",
    on_entity="supplies_product",
    definition="""
        AFTER INSERT ON supplies_product
        FOR EACH ROW
        EXECUTE FUNCTION update_supplies_product_fn();
    """,
)

supplies_product_update_tg = PGTrigger(
    schema="public",
    signature="supplies_product_update_tg",
    on_entity="supplies_product",
    definition="""
        AFTER UPDATE ON supplies_product
        FOR EACH ROW
        EXECUTE FUNCTION update_supplies_product_fn();
    """,
)

supplies_product_delete_tg = PGTrigger(
    schema="public",
    signature="supplies_product_delete_tg",
    on_entity="supplies_product",
    definition="""
        AFTER DELETE ON supplies_product
        FOR EACH ROW
        EXECUTE FUNCTION update_supplies_product_fn();
    """,
)

UPDATE_SUPPLIES_DRAFT_SQL = """
RETURNS TRIGGER AS $$
BEGIN
    IF (TG_OP = 'UPDATE') THEN
        IF (NEW.draft != OLD.draft) THEN
            IF (NEW.draft = TRUE) THEN
                IF NOT EXISTS (
                        SELECT 1
                        FROM supplies_product sp
                        JOIN product p ON p.id = sp.product_id
                        WHERE sp.supplies_id = NEW.id AND p.quantity < sp.quantity
                    ) THEN
                        UPDATE product p
                        SET quantity = p.quantity - sp.quantity
                        FROM supplies_product sp
                        WHERE sp.supplies_id = NEW.id AND p.id = sp.product_id;
                    ELSE
                        RAISE EXCEPTION 'Not enough products. Is Draft leads to a negative remainder';
                    END IF;
                END IF;
                IF (NEW.draft = FALSE) THEN
                    UPDATE product p
                    SET quantity = p.quantity + sp.quantity
                    FROM supplies_product sp
                    WHERE sp.supplies_id = NEW.id AND p.id = sp.product_id;
                END IF;
            END IF;
        END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
"""

update_supplies_draft_fn = PGFunction(
    schema="public",
    signature="update_supplies_draft_fn()",
    definition=UPDATE_SUPPLIES_DRAFT_SQL
)

update_supplies_draft_tg = PGTrigger(
    schema="public",
    signature="update_supplies_draft_tg",
    on_entity="supplies",
    definition="""
        AFTER UPDATE ON supplies
        FOR EACH ROW
        EXECUTE FUNCTION update_supplies_draft_fn();
    """,
)
