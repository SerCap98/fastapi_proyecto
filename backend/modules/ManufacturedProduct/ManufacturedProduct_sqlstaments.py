
CREATE_MANUFACTURED_PRODUCT = """
    INSERT INTO manufactured_product (id, id_product, lot_number, quantity, created_by, created_at)
    VALUES (:id, :id_product, :lot_number, :quantity, :created_by, :created_at)
    RETURNING id, id_product, lot_number, quantity, created_by, created_at;
"""

GET_MANUFACTURED_PRODUCT_BY_ID = """
    SELECT id, id_product, lot_number, quantity, created_by, created_at
    FROM manufactured_product
    WHERE id = :id;
"""

UPDATE_MANUFACTURED_PRODUCT_BY_ID = """
    UPDATE manufactured_product
    SET product_name = :product_name,
        updated_at = :updated_at,
        updated_by = :updated_by
    WHERE id = :id
    RETURNING id, id_product, lot_number, quantity, created_by, created_at;
"""

DELETE_MANUFACTURED_PRODUCT_BY_ID = """
    DELETE FROM manufactured_product
    WHERE id = :id;
"""

LIST_MANUFACTURED_PRODUCT = """
    SELECT mp.id, mp.lot_number, mp.quantity, mp.created_by, mp.created_at, mp.updated_by, mp.updated_at,
        us1.fullname AS created_by_fullname, us2.fullname AS updated_by_fullname,
        prod.name AS product_name
    FROM manufactured_product AS mp
    LEFT JOIN users AS us1 ON us1.id = mp.created_by
    LEFT JOIN users AS us2 ON us2.id = mp.updated_by
    LEFT JOIN product AS prod ON prod.id = mp.id_product
"""

def MANUFACTURED_PRODUCT_COMPLEMENTS(order: str | None, direction: str | None):
    sql_sentence = ""
    if not order and not direction:
        sql_sentence = " ORDER BY mp.quantity ASC;"
    elif order == "quantity" and direction == "DESC":
        sql_sentence = " ORDER BY mp.quantity DESC;"
    elif order == "quantity" and (direction == "ASC" or direction == None):
        sql_sentence = " ORDER BY mp.quantity ASC;"

    return sql_sentence


def MANUFACTURED_PRODUCT_SEARCH():
    return """ WHERE (prod.name ILIKE :search ) """
