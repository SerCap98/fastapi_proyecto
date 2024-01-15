CREATE_BACKLOG = """
    INSERT INTO backlog (id, id_order_product, missing_amount, state, created_by, created_at)
    VALUES (:id, :id_order_product, :missing_amount, :state, :created_by, :created_at)
    RETURNING id, id_order_product, missing_amount, state, created_by, created_at;
"""
GET_BACKLOG_BY_ID = """
    SELECT id, id_order_product, missing_amount, state,created_by, created_at, updated_by, updated_at
    FROM backlog
    WHERE id = :id;
"""
DELETE_BACKLOG_BY_ID = """
    DELETE FROM backlog
    WHERE id = :id;
"""

ATTENDED_BACKLOG_BY_ID = """
    UPDATE backlog
    SET state = :state, updated_by = :updated_by, updated_at = :updated_at
    WHERE id = :id
    RETURNING id, id_order_product, missing_amount, state, updated_by, updated_at;
"""



LIST_BACKLOG = """
    SELECT 
        back.id, 
        back.id_order_product, 
        back.missing_amount, 
        back.state, 
        back.created_by, 
        back.created_at, 
        back.updated_by, 
        back.updated_at,
        us1.fullname AS created_by_fullname, 
        us2.fullname AS updated_by_fullname,
        prod.name AS product_name,
    FROM backlog AS back
    LEFT JOIN users AS us1 ON us1.id = back.created_by
    LEFT JOIN users AS us2 ON us2.id = back.updated_by
    LEFT JOIN order_product AS ord ON ord.id = back.id_order_product
    LEFT JOIN product AS prod ON prod.id = ord.id_product
"""

def BACKLOG_COMPLEMENTS(order: str | None, direction: str | None):

    sql_sentence = ""
    if not order and not direction:
        sql_sentence = " ORDER BY back.created_at ASC;"
    elif order == "created_at" and direction == "DESC":
        sql_sentence = " ORDER BY back.created_at DESC;"
    elif order == "created_at" and (direction == "ASC" or direction == None):
        sql_sentence = " ORDER BY back.created_at ASC;"
    


    return sql_sentence



def BACKLOG_SEARCH():
    return """
            WHERE 
                (prod.name ILIKE :search 
                OR back.state::text ILIKE :search)
        """

