

CREATE_PRODUCT = """
    INSERT INTO product (id, name, cost_per_bag, created_by, created_at)
    VALUES (:id, :name, :cost_per_bag, :created_by, :created_at)
    RETURNING id, name, cost_per_bag, created_by, created_at;
"""


GET_PRODUCT_BY_NAME = """
    SELECT id, name, cost_per_bag, created_by, created_at, updated_by, updated_at
    FROM product
    WHERE name = :name;
"""

UPDATE_PRODUCT_BY_NAME = """
    UPDATE product
    SET name = :name, cost_per_bag = :cost_per_bag,updated_by = :updated_by, updated_at = :updated_at
    WHERE name = :original_name
    RETURNING id, name, cost_per_bag,created_by, created_at, updated_by, updated_at;
"""

DELETE_PRODUCT_BY_NAME = """
    DELETE FROM product
    WHERE name = :name
"""

LIST_PRODUCT = """
    SELECT prod.id, prod.name, prod.cost_per_bag, prod.created_by, prod.created_at, prod.updated_by, prod.updated_at,
        us1.fullname AS created_by, us2.fullname AS updated_by
    FROM product AS prod
    LEFT JOIN users AS us1 ON us1.id = prod.created_by
    LEFT JOIN users AS us2 ON us2.id = prod.updated_by
"""

def PRODUCT_COMPLEMENTS(order: str | None, direction: str | None):
    sql_sentence = ""
    if not order and not direction:
        sql_sentence = " ORDER BY prod.name ASC;"
    elif order == "name" and direction == "DESC":
        sql_sentence = " ORDER BY prod.name DESC;"
    elif order == "name" and (direction == "ASC" or direction == None):
        sql_sentence = " ORDER BY prod.name ASC;"
    elif order == "cost_per_bag" and direction == "DESC":
        sql_sentence = " ORDER BY prod.cost_per_bag DESC;"
    elif order == "cost_per_bag" and (direction == "ASC" or direction == None):
        sql_sentence = " ORDER BY prod.cost_per_bag ASC;"

    return sql_sentence


def PRODUCT_SEARCH():
    return """ WHERE (prod.name LIKE :search
        or prod.cost_per_bag ILIKE :search  """
