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





LIST_ALERT = """
    SELECT 
        ale.id, 
        ale.id_factory_inventory, 
        ale.state, 
        ale.description, 
        ale.created_by, 
        ale.created_at, 
        ale.updated_by, 
        ale.updated_at,
        us1.fullname AS created_by_fullname, 
        us2.fullname AS updated_by_fullname,
        fact.identifier AS factory_identifier, 
        raw_mat.code AS raw_material_code
    FROM alert AS ale
    LEFT JOIN users AS us1 ON us1.id = ale.created_by
    LEFT JOIN users AS us2 ON us2.id = ale.updated_by
    LEFT JOIN factory_raw_material_inventory AS inv ON inv.id = ale.id_factory_inventory
    LEFT JOIN factory AS fact ON fact.id = inv.id_factory
    LEFT JOIN raw_material AS raw_mat ON raw_mat.id = inv.id_raw_material
"""





def ALERT_COMPLEMENTS(order: str | None, direction: str | None):

    sql_sentence = ""
    if not order and not direction:
        sql_sentence = " ORDER BY ale.created_at ASC;"
    elif order == "created_at" and direction == "DESC":
        sql_sentence = " ORDER BY ale.created_at DESC;"
    elif order == "created_at" and (direction == "ASC" or direction == None):
        sql_sentence = " ORDER BY ale.created_at ASC;"
    


    return sql_sentence



def ALERT_SEARCH():
    return """
            WHERE 
                (fact.identifier ILIKE :search 
                OR raw_mat.code ILIKE :search
                OR ale.state::text ILIKE :search)
        """

