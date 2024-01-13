CREATE_FACTORY_RAW_MATERIAL_INVENTORY = """
    INSERT INTO factory_raw_material_inventory (
        id, 
        id_factory, 
        id_raw_material, 
        min_quantity, 
        quantity, 
        created_by, 
        created_at
    ) VALUES (
        :id, 
        :factory, 
        :raw_material, 
        COALESCE(:min_quantity, 0),  
        :quantity,                 
        :created_by, 
        :created_at
    )
    RETURNING id, id_factory, id_raw_material, min_quantity, quantity, created_by, created_at;
"""
DELETE_FACTORY_RAW_MATERIAL_INVENTORY = """
    DELETE FROM factory_raw_material_inventory
    WHERE id_factory = :factory AND id_raw_material = :raw_material;
"""
GET_FACTORY_RAW_MATERIAL_INVENTORY = """
    SELECT id, id_factory, id_raw_material, min_quantity, quantity, created_by, created_at, updated_by, updated_at
    FROM factory_raw_material_inventory
    WHERE id_factory = :factory AND id_raw_material = :raw_material;
"""