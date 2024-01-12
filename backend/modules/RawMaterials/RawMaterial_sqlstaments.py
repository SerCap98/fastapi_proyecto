

CREATE_RAW_MATERIAL = """
    INSERT INTO raw_material (id, name, code, created_at, updated_at)
    VALUES (:id, :name, :code, :created_at, :updated_at)
    RETURNING id, name, code;
"""

GET_RAW_MATERIAL_BY_CODE = """
    SELECT id, name, code, created_at, updated_at
    FROM raw_material
    WHERE code = :code;
"""

UPDATE_RAW_MATERIAL_BY_CODE = """
    UPDATE raw_material
    SET name = :name, code = :code, updated_at = :updated_at
    WHERE code = :code
    RETURNING id, name, code,updated_at;
"""

DELETE_RAW_MATERIAL_BY_CODE = """
    DELETE FROM raw_material
    WHERE code = :code
    RETURNING code;
"""

LIST_RAW_MATERIALS = """
    SELECT id, name, code, created_at, updated_at
    FROM raw_material;
"""
