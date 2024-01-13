

CREATE_MANUFACTURED_PRODUCT = """
    INSERT INTO manufactured_product (id, id_product, lot_number, quantity, created_by, created_at)
    VALUES (:id, :lot_number, :quantity, :created_by, :created_at)
    RETURNING id, id_product, lot_number, quantity, created_by, created_at;
"""


GET_MANUFACTURED_PRODUCT_BY_LOT_NUMBER = """
    SELECT id, id_product, lot_number, quantity, created_by, created_at, updated_by, updated_at
    FROM manufactured_product
    WHERE lot_number = :lot_number;
"""

UPDATE_MANUFACTURED_PRODUCT_BY_LOT_NUMBER = """
    UPDATE manufactured_product
    SET id_product = :id_product, lot_number = :lot_number, quantity = :quantity,updated_by = :updated_by, updated_at = :updated_at
    WHERE lot_number = :original_lot_number
    RETURNING id, id_product, lot_number, quantity,created_by, created_at, updated_by, updated_at;
"""

DELETE_MANUFACTURED_PRODUCT_BY_LOT_NUMBER = """
    DELETE FROM manufactured_product
    WHERE lot_number = :lot_number
"""

LIST_MANUFACTURED_PRODUCT = """
    SELECT mp.id, mp.id_product, mp.lot_number, mp.quantity, mp.created_by, mp.created_at, mp.updated_by, mp.updated_at,
        us1.fullname AS created_by, us2.fullname AS updated_by
    FROM manufactured_product AS mp
    LEFT JOIN users AS us1 ON us1.id = mp.created_by
    LEFT JOIN users AS us2 ON us2.id = mp.updated_by
"""

def MANUFACTURED_PRODUCT_COMPLEMENTS(order: str | None, direction: str | None):
    sql_sentence = ""
    if not order and not direction:
        sql_sentence = " ORDER BY mp.lot_number ASC;"
    elif order == "lot_number" and direction == "DESC":
        sql_sentence = " ORDER BY mp.lot_number DESC;"
    elif order == "lot_number" and (direction == "ASC" or direction == None):
        sql_sentence = " ORDER BY mp.lot_number ASC;"
    elif order == "quantity" and direction == "DESC":
        sql_sentence = " ORDER BY mp.quantity DESC;"
    elif order == "quantity" and (direction == "ASC" or direction == None):
        sql_sentence = " ORDER BY mp.quantity ASC;"

    return sql_sentence


def MANUFACTURED_PRODUCT_SEARCH():
    return """ WHERE (mp.lot_number LIKE :search
        or mp.quantity ILIKE :search or mp.id_product ILIKE : search """
