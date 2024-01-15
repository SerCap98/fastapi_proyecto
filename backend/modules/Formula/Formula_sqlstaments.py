CREATE_FORMULA = """
    INSERT INTO formula (id, quantity, id_raw_material, id_product, created_by, created_at)
    VALUES ( :id, :quantity, :raw_material, :product, :created_by, :created_at )
    RETURNING id, quantity, id_raw_material, id_product, created_by, created_at;
"""
DELETE_RAW_MATERIAL_PRODUCT_FORMULA = """
    DELETE FROM formula
    WHERE id_raw_material = :raw_material AND id_product = :product;
"""

DELETE_PRODUCT_FORMULA = """
    DELETE FROM formula
    WHERE id_product = :product;
"""

GET_RAW_MATERIAL_PRODUCT_FORMULA = """
    SELECT id, quantity, id_raw_material, id_product, created_by, created_at, updated_by, updated_at
    FROM formula
    WHERE id_raw_material = :raw_material AND id_product = :product;
"""

INCREASE_QUANTITY_RAW_MATERIAL_PRODUCT_FORMULA = """
    UPDATE formula
    SET quantity = quantity + :quantity,
        updated_at = :updated_at,
        updated_by = :updated_by
    WHERE id_raw_material = :raw_material AND id_product = :product
    RETURNING id, quantity, id_raw_material, id_product, created_by, created_at, updated_by, updated_at;
"""

DECREASE_QUANTITY_RAW_MATERIAL_PRODUCT_FORMULA = """
    UPDATE formula
    SET quantity = CASE
                       WHEN quantity - :quantity < 0 THEN 0
                       ELSE quantity - :quantity
                   END,
        updated_at = :updated_at,
        updated_by = :updated_by
    WHERE id_raw_material = :raw_material AND id_product = :product
    RETURNING id, quantity, id_raw_material, id_product, created_by, created_at, updated_by, updated_at;
"""

LIST_FORMULA = """
    SELECT fm.id, fm.quantity, fm.created_by, fm.created_at, fm.updated_by, fm.updated_at,
        us1.fullname AS created_by_fullname, us2.fullname AS updated_by_fullname,
        raw.code AS raw_material_code, prod.name AS product_name
    FROM formula AS fm
    LEFT JOIN users AS us1 ON us1.id = fm.created_by
    LEFT JOIN users AS us2 ON us2.id = fm.updated_by
    LEFT JOIN raw_material AS raw ON raw.id = fm.id_raw_material
    LEFT JOIN product AS prod ON prod.id = fm.id_product
"""


def FORMULA_COMPLEMENTS(order: str | None, direction: str | None):
    sql_sentence = ""
    if not order and not direction:
        sql_sentence = " ORDER BY fm.quantity ASC;"
    elif order == "quantity" and direction == "DESC":
        sql_sentence = " ORDER BY fm.quantity DESC;"
    elif order == "quantity" and (direction == "ASC" or direction == None):
        sql_sentence = " ORDER BY fm.quantity ASC;"


    return sql_sentence


def FORMULA_SEARCH():
    return """ WHERE (raw.code ILIKE :search OR prod.name ILIKE :search) """

