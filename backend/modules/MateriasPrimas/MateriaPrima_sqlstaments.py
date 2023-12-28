

CREATE_MATERIA_PRIMA = """
    INSERT INTO materias_primas (id, nombre, codigo, created_at, updated_at)
    VALUES (:id, :nombre, :codigo, :created_at, :updated_at)
    RETURNING id, nombre, codigo;
"""

GET_MATERIA_PRIMA_BY_CODE = """
    SELECT id, nombre, codigo, created_at, updated_at
    FROM materias_primas
    WHERE codigo = :codigo;
"""

UPDATE_MATERIA_PRIMA_BY_CODE = """
    UPDATE materias_primas
    SET nombre = :nombre, codigo = :codigo, updated_at = :updated_at
    WHERE codigo = :codigo
    RETURNING id, nombre, codigo,updated_at;
"""

DELETE_MATERIA_PRIMA_BY_CODE = """
    DELETE FROM materias_primas
    WHERE codigo = :codigo
    RETURNING codigo;
"""

LIST_MATERIAS_PRIMAS = """
    SELECT id, nombre, codigo, created_at, updated_at
    FROM materias_primas;
"""
