

CREATE_FACTORY = """
    INSERT INTO factory (id, identifier, created_at, updated_at)
    VALUES (:id, :identifier, :created_at, :updated_at)
    RETURNING id, identifier;
"""

GET_FACTORY_BY_IDENTIFIER = """
    SELECT id, identifier, created_at, updated_at
    FROM factory
    WHERE identifier = :identifier;
"""

UPDATE_FACTORY_BY_IDENTIFIER = """
    UPDATE factory
    SET identifier = :identifier, updated_at = :updated_at
    WHERE identifier = :identifier
    RETURNING id, identifier, updated_at;
"""

DELETE_FACTORY_BY_IDENTIFIER = """
    DELETE FROM factory
    WHERE identifier = :coidentifierde
    RETURNING identifier;
"""

LIST_FACTORY = """
    SELECT id, name, identifier, created_at, updated_at
    FROM factory;
"""
