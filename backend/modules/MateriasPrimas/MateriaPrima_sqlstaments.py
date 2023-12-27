

CREATE_MATERIA_PRIMA = """
    INSERT INTO materias_primas (id, nombre, cantidad, unidad_medida, created_at, updated_at)
    VALUES (:id, :nombre, :cantidad, :unidad_medida, :created_at, :updated_at)
    RETURNING id, nombre, cantidad, unidad_medida;
"""

GET_MATERIA_PRIMA_BY_ID = """
    SELECT id, nombre, cantidad, unidad_medida, created_at, updated_at
    FROM materias_primas
    WHERE id = :id;
"""

UPDATE_MATERIA_PRIMA_BY_ID = """
    UPDATE materias_primas
    SET nombre = :nombre, cantidad = :cantidad, unidad_medida = :unidad_medida, updated_at = :updated_at
    WHERE id = :id
    RETURNING id, nombre, cantidad, unidad_medida;
"""

DELETE_MATERIA_PRIMA_BY_ID = """
    DELETE FROM materias_primas
    WHERE id = :id
    RETURNING id;
"""

LIST_MATERIAS_PRIMAS = """
    SELECT id, nombre, cantidad, unidad_medida, created_at, updated_at
    FROM materias_primas;
"""
