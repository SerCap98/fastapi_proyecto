
CREATE_ORDER_PRODUCT = """
    INSERT INTO order_product (id, id_product,client,total_cost,quantity,note,discount,delivered,date_delivered, created_by, created_at)
    VALUES (:id, :product,:client,:total_cost,:quantity,:note,:discount,:delivered,:date_delivered, :created_by, :created_at)
    RETURNING id, id_product,client,total_cost,quantity,note,discount,delivered,date_delivered, created_by, created_at;
"""

GET_ORDER_PRODUCT_BY_NAME = """
    SELECT id, id_product, client, total_cost, quantity , note , discount , delivered , date_delivered, created_by, created_at
    FROM order_product
    WHERE id_product = :product;
"""

LIST_ORDER_PRODUCT = """
    SELECT op.id, op.id_product, op.client, op.total_cost, op.quantity ,op.note ,op.discount ,op.delivered ,op.date_delivered, op.created_by, op.created_at, op.updated_by, op.updated_at,
        us1.fullname AS created_by_fullname, us2.fullname AS updated_by_fullname,
        prod.name AS product_name
    FROM order_product AS op
    LEFT JOIN users AS us1 ON us1.id = op.created_by
    LEFT JOIN users AS us2 ON us2.id = op.updated_by
    LEFT JOIN product AS prod ON prod.id = op.id_product
"""

DELETE_ORDER_PRODUCT_BY_ID = """
    DELETE from order_product
    WHERE id = :id
    RETURNING id
"""

def ORDER_PRODUCT_COMPLEMENTS(order: str | None, direction: str | None):
    sql_sentence = ""
    if not order and not direction:
        sql_sentence = " ORDER BY op.quantity ASC;"
    elif order == "created_at" and direction == "DESC":
        sql_sentence = " ORDER BY op.created_at DESC;"
    elif order == "created_at" and (direction == "ASC" or direction == None):
        sql_sentence = " ORDER BY op.created_at ASC;"

    return sql_sentence


def ORDER_PRODUCT_SEARCH():
    return """ WHERE (prod.name ILIKE :search """
