

CREATE_RAW_MATERIAL = """
    INSERT INTO raw_material (id, name, code, created_by, created_at)
    VALUES (:id, :name, :code, :created_by, :created_at)
    RETURNING id, name, code, created_by, created_at;
"""


GET_RAW_MATERIAL_BY_CODE = """
    SELECT id, name, code, created_by, created_at, updated_by, updated_at
    FROM raw_material
    WHERE code = :code;
"""

UPDATE_RAW_MATERIAL_BY_CODE = """
    UPDATE raw_material
    SET name = :name, code = :code,updated_by = :updated_by, updated_at = :updated_at
    WHERE code = :original_code
    RETURNING id, name, code,created_by, created_at, updated_by, updated_at;
"""

DELETE_RAW_MATERIAL_BY_CODE = """
    DELETE FROM raw_material
    WHERE code = :code
"""

LIST_RAW_MATERIALS = """
    SELECT raw.id, raw.name, raw.code, raw.created_by, raw.created_at, raw.updated_by, raw.updated_at,
        us1.fullname AS created_by_fullname, us2.fullname AS updated_by_fullname
    FROM raw_material AS raw
    LEFT JOIN users AS us1 ON us1.id = raw.created_by
    LEFT JOIN users AS us2 ON us2.id = raw.updated_by
"""

def RAW_MATERIALS_COMPLEMENTS(order: str | None, direction: str | None):
    sql_sentence = ""
    if not order and not direction:
        sql_sentence = " ORDER BY raw.name ASC;"
    elif order == "name" and direction == "DESC":
        sql_sentence = " ORDER BY raw.name DESC;"
    elif order == "name" and (direction == "ASC" or direction == None):
        sql_sentence = " ORDER BY raw.name ASC;"
    elif order == "code" and direction == "DESC":
        sql_sentence = " ORDER BY raw.code DESC;"
    elif order == "code" and (direction == "ASC" or direction == None):
        sql_sentence = " ORDER BY raw.code ASC;"

    return sql_sentence


def RAW_MATERIALS_SEARCH():
    return """ WHERE (raw.name ILIKE :search 
        or raw.code ILIKE :search  """
