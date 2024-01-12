CREATE_FACTORY = """
    INSERT INTO factory (id, identifier, created_by, created_at)
    VALUES (:id, :identifier, :created_by, :created_at)
    RETURNING id, identifier, created_by, created_at;
"""


GET_FACTORY_BY_IDENTIFIER = """
    SELECT id, identifier, created_by, created_at, updated_by, updated_at
    FROM factory
    WHERE identifier = :identifier;
"""

UPDATE_FACTORY_BY_IDENTIFIER = """
    UPDATE factory
    SET identifier = :identifier,updated_by = :updated_by, updated_at = :updated_at
    WHERE identifier = :original_identifier
    RETURNING id, identifier,created_by, created_at, updated_by, updated_at;
"""

DELETE_FACTORY_BY_IDENTIFIER = """
    DELETE FROM factory
    WHERE identifier = :identifier
"""

LIST_FACTORY = """
    SELECT fty.id, fty.identifier, fty.created_by, fty.created_at, fty.updated_by, fty.updated_at,
        us1.fullname AS created_by, us2.fullname AS updated_by
    FROM factory AS fty
    LEFT JOIN users AS us1 ON us1.id = fty.created_by
    LEFT JOIN users AS us2 ON us2.id = fty.updated_by
"""

def FACTORY_COMPLEMENTS(order: str | None, direction: str | None):
    sql_sentence = ""
    if not order and not direction:
        sql_sentence = " ORDER BY fty.identifier ASC;"
    elif order == "identifier" and direction == "DESC":
        sql_sentence = " ORDER BY fty.identifier DESC;"
    elif order == "identifier" and (direction == "ASC" or direction == None):
        sql_sentence = " ORDER BY fty.identifier ASC;"

    return sql_sentence

def FACTORY_SEARCH():
    return """ WHERE (fty.identifier LIKE :search """