CREATE_ALERT = """
    INSERT INTO alert (id, id_factory_inventory, state, description, created_by, created_at)
    VALUES (:id, :id_factory_inventory, :state, :description, :created_by, :created_at)
    RETURNING id, id_factory_inventory, state, description, created_by, created_at;
"""
GET_ALERT_BY_ID = """
    SELECT id, id_factory_inventory, state, description,created_by, created_at, updated_by, updated_at
    FROM alert
    WHERE id = :id;
"""
DELETE_ALERT_BY_ID = """
    DELETE FROM alert
    WHERE id = :id;
"""

ATTENDED_ALERT_BY_ID = """
    UPDATE alert
    SET state = :state, updated_by = :updated_by, updated_at = :updated_at
    WHERE id = :id
    RETURNING id, id_factory_inventory,description, state, updated_by, updated_at;
"""
