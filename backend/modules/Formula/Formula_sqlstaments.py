CREATE_FORMULA = """
    INSERT INTO formula (id, id_raw_material, id_product, quantity, created_by, created_at)
    VALUES ( :id, :raw_material, :product, :quantity, :created_by, :created_at )
    RETURNING id, id_raw_material, id_product, quantity, created_by, created_at;
"""
DELETE_PRODUCT_RAW_MATERIAL_FORMULA = """
    DELETE FROM formula
    WHERE id_product = :product AND id_raw_material = :raw_material;
"""
GET_PRODUCT_RAW_MATERIAL_FORMULA = """
    SELECT id, id_raw_material, id_product, quantity, created_by, created_at, updated_by, updated_at
    FROM formula
    WHERE id_product = :product AND id_raw_material = :raw_material;
"""

INCREASE_QUANTITY_PRODUCT_RAW_MATERIAL_FORMULA = """
    UPDATE formula
    SET quantity = quantity + :quantity,
        updated_at = :updated_at,
        updated_by = :updated_by
    WHERE id_product = :product AND id_raw_material = :raw_material
    RETURNING id, id_raw_material, id_product, quantity, created_by, created_at, updated_by, updated_at;
"""

DECREASE_QUANTITY_PRODUCT_RAW_MATERIAL_FORMULA = """
    UPDATE formula
    SET quantity = CASE
                       WHEN quantity - :quantity < 0 THEN 0
                       ELSE quantity - :quantity
                   END,
        updated_at = :updated_at,
        updated_by = :updated_by
    WHERE id_product = :product AND id_raw_material = :raw_material
    RETURNING id, id_raw_material, id_product, quantity, created_by, created_at, updated_by, updated_at;
"""

LIST_FORMULA = """
    SELECT fm.id, fm.quantity, fm.created_by, fm.created_at, fm.updated_by, fm.updated_at,
        us1.fullname AS created_by_fullname, us2.fullname AS updated_by_fullname,
        prod.name AS product_name, raw.code AS raw_material_code
    FROM formula AS fm
    LEFT JOIN users AS us1 ON us1.id = fm.created_by
    LEFT JOIN users AS us2 ON us2.id = fm.updated_by
    LEFT JOIN product AS prod ON prod.id = fm.id_product
    LEFT JOIN raw_material AS raw ON raw.id = fm.id_raw_material
"""
LIST_FORMULA_BY_NAME = """
    SELECT fm.id, fm.quantity, fm.created_by, fm.created_at, fm.updated_by, fm.updated_at,
        us1.fullname AS created_by_fullname, us2.fullname AS updated_by_fullname,
        prod.name AS product_name, raw.code AS raw_material_code
    FROM formula AS fm
    LEFT JOIN users AS us1 ON us1.id = fm.created_by
    LEFT JOIN users AS us2 ON us2.id = fm.updated_by
    LEFT JOIN product AS prod ON prod.id = fm.id_product
    LEFT JOIN raw_material AS raw ON raw.id = fm.id_raw_material
    WHERE prod.name = :name
"""

LIST_FORMULA_BY_CODE = """
    SELECT fm.id, fm.quantity, fm.created_by, fm.created_at, fm.updated_by, fm.updated_at,
        us1.fullname AS created_by_fullname, us2.fullname AS updated_by_fullname,
        prod.name AS product_name, raw.code AS raw_material_code
    FROM formula AS fm
    LEFT JOIN users AS us1 ON us1.id = fm.created_by
    LEFT JOIN users AS us2 ON us2.id = fm.updated_by
    LEFT JOIN product AS prod ON prod.id = fm.id_product
    LEFT JOIN raw_material AS raw ON raw.id = fm.id_raw_material
    WHERE raw.code = :code
"""

def FORMULA_COMPLEMENTS(order: str | None, direction: str | None):
    sql_sentence = ""
    if not order and not direction:
        sql_sentence = " ORDER BY inv.quantity ASC;"
    elif order == "quantity" and direction == "DESC":
        sql_sentence = " ORDER BY inv.quantity DESC;"
    elif order == "quantity" and (direction == "ASC" or direction == None):
        sql_sentence = " ORDER BY inv.quantity ASC;"


    return sql_sentence


def FORMULA_SEARCH():
    return """ WHERE (raw.code ILIKE :search OR prod.name ILIKE :search) """

