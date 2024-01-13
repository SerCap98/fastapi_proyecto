CREATE_FACTORY_RAW_MATERIAL_INVENTORY = """
    INSERT INTO factory_raw_material_inventory (
        id, 
        id_factory, 
        id_raw_material, 
        min_quantity, 
        quantity, 
        created_by, 
        created_at
    ) VALUES (
        :id, 
        :factory, 
        :raw_material, 
        COALESCE(:min_quantity, 0),  
        :quantity,                 
        :created_by, 
        :created_at
    )
    RETURNING id, id_factory, id_raw_material, min_quantity, quantity, created_by, created_at;
"""
DELETE_FACTORY_RAW_MATERIAL_INVENTORY = """
    DELETE FROM factory_raw_material_inventory
    WHERE id_factory = :factory AND id_raw_material = :raw_material;
"""
GET_FACTORY_RAW_MATERIAL_INVENTORY = """
    SELECT id, id_factory, id_raw_material, min_quantity, quantity, created_by, created_at, updated_by, updated_at
    FROM factory_raw_material_inventory
    WHERE id_factory = :factory AND id_raw_material = :raw_material;
"""

INCREASE_QUANTITY_FACTORY_RAW_MATERIAL_INVENTORY = """
    UPDATE factory_raw_material_inventory
    SET quantity = quantity + :quantity,
        updated_at = :updated_at,
        updated_by = :updated_by
    WHERE id_factory = :factory AND id_raw_material = :raw_material
    RETURNING id, id_factory, id_raw_material, min_quantity, quantity, created_by, created_at, updated_by, updated_at;
"""
UPDATE_MIN_QUANTITY_FACTORY_RAW_MATERIAL_INVENTORY = """
    UPDATE factory_raw_material_inventory
    SET min_quantity = :min_quantity,
        updated_at = :updated_at,
        updated_by = :updated_by
    WHERE id_factory = :factory AND id_raw_material = :raw_material
    RETURNING id, id_factory, id_raw_material, min_quantity, quantity, created_by, created_at, updated_by, updated_at;
"""

DECREASE_QUANTITY_FACTORY_RAW_MATERIAL_INVENTORY = """
    UPDATE factory_raw_material_inventory
    SET quantity = CASE
                       WHEN quantity - :quantity < 0 THEN 0
                       ELSE quantity - :quantity
                   END,
        updated_at = :updated_at,
        updated_by = :updated_by
    WHERE id_factory = :factory AND id_raw_material = :raw_material
    RETURNING id, id_factory, id_raw_material, min_quantity, quantity, created_by, created_at, updated_by, updated_at;
"""

LIST_INVENTORY = """
    SELECT inv.id, inv.quantity, inv.min_quantity, inv.created_by, inv.created_at, inv.updated_by, inv.updated_at,
        us1.fullname AS created_by_fullname, us2.fullname AS updated_by_fullname,
        fact.identifier AS factory_identifier, raw.code AS raw_material_code
    FROM factory_raw_material_inventory AS inv
    LEFT JOIN users AS us1 ON us1.id = inv.created_by
    LEFT JOIN users AS us2 ON us2.id = inv.updated_by
    LEFT JOIN factory AS fact ON fact.id = inv.id_factory
    LEFT JOIN raw_material AS raw ON raw.id = inv.id_raw_material
"""

def INVENTORY_COMPLEMENTS(order: str | None, direction: str | None):
    sql_sentence = ""
    if not order and not direction:
        sql_sentence = " ORDER BY inv.quantity ASC;"
    elif order == "quantity" and direction == "DESC":
        sql_sentence = " ORDER BY inv.quantity DESC;"
    elif order == "quantity" and (direction == "ASC" or direction == None):
        sql_sentence = " ORDER BY inv.quantity ASC;"


    return sql_sentence


def INVENTORY_SEARCH():
    return """ WHERE (raw.code ILIKE :search OR fact.identifier ILIKE :search) """

