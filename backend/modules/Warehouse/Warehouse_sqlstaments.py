

CREATE_WAREHOUSE = """
    INSERT INTO warehouse (id, name, type, type_num, created_by, created_at)
    VALUES (:id, :name, :type, :type_num, :created_by, :created_at)
    RETURNING id, name, type, type_num, created_by, created_at;
"""

GET_WAREHOUSE_BY_NAME = """
    SELECT id, name, type, type_num, created_by, created_at
    FROM warehouse
    WHERE name = :name;
"""

UPDATE_WAREHOUSE_BY_NAME = """
    UPDATE warehouse
    SET name = :name, type = :type, type_num = :type_num, updated_by = :updated_by, updated_at = :updated_at
    WHERE name = :original_name
    RETURNING id, name, type, type_num,created_by, created_at, updated_by, updated_at;
"""

DELETE_WAREHOUSE_BY_NAME = """
    DELETE FROM warehouse
    WHERE name = :name
"""

LIST_WAREHOUSE = """
    SELECT wh.id, wh.name, wh.type, wh.type_num, wh.created_by, wh.created_at, wh.updated_by, wh.updated_at,
        us1.fullname AS created_by_fullname, us2.fullname AS updated_by_fullname
    FROM warehouse AS wh
    LEFT JOIN users AS us1 ON us1.id = wh.created_by
    LEFT JOIN users AS us2 ON us2.id = wh.updated_by
"""

def WAREHOUSE_COMPLEMENTS(order: str | None, direction: str | None):
    sql_sentence = ""
    if not order and not direction:
        sql_sentence = " ORDER BY wh.name ASC;"
    elif order == "name" and direction == "DESC":
        sql_sentence = " ORDER BY wh.name DESC;"
    elif order == "name" and (direction == "ASC" or direction == None):
        sql_sentence = " ORDER BY wh.name ASC;"
    elif order == "type" and direction == "DESC":
        sql_sentence = " ORDER BY wh.type DESC;"
    elif order == "type" and (direction == "ASC" or direction == None):
        sql_sentence = " ORDER BY wh.type ASC;"
    elif order == "type_num" and direction == "DESC":
        sql_sentence = " ORDER BY wh.type_num DESC;"
    elif order == "type_num" and (direction == "ASC" or direction == None):
        sql_sentence = " ORDER BY wh.type_num ASC;"

    return sql_sentence


def WAREHOUSE_SEARCH():
    return """ WHERE (wh.name ILIKE :search or wh.type::text ILIKE :search or wh.type_num ILIKE :search) """
