CREATE_RAW_MATERIAL_ORDER = """
    INSERT INTO raw_material_order (
        id, id_raw_material, id_factory, quantity, state, note, cost, delivered, date_delivered, created_by, created_at
    ) VALUES (
        :id, :raw_material, :factory, :quantity, :state, :note, :cost, :delivered, :date_delivered, :created_by, :created_at
    )
    RETURNING id, id_raw_material, id_factory, quantity, state, note, cost, delivered, date_delivered, created_by, created_at;
"""
DELETE_RAW_MATERIAL_ORDER = """
    DELETE FROM raw_material_order
    WHERE id = :id;
"""
GET_RAW_MATERIAL_ORDER = """
    SELECT id, id_raw_material, id_factory, quantity, state, note, cost, delivered, date_delivered, created_by, created_at, updated_by, updated_at
    FROM raw_material_order
    WHERE id = :id;
"""

UPDATED_ORDER = """
    UPDATE raw_material_order
    SET
        quantity = :quantity,
        note = :note,
        cost = :cost,
        updated_by = :updated_by,
        updated_at = :updated_at
    WHERE id = :id
    RETURNING id, id_raw_material, id_factory, quantity, state, note, cost, delivered, date_delivered, created_by, created_at;
"""

SET_DELIVERED_RAW_MATERIAL_ORDER = """
    UPDATE raw_material_order
    SET delivered = :delivered,
        date_delivered= :date_delivered,
        updated_at = :updated_at,
        updated_by = :updated_by
    WHERE id = :id 
    RETURNING id, id_raw_material, id_factory, quantity, state, note, cost, delivered, date_delivered, created_by, created_at, updated_by, updated_at;
"""



LIST_RAW_MATERIAL_ORDER = """
    SELECT rmo.id, rmo.id_raw_material, rmo.id_factory, rmo.quantity, rmo.state, rmo.note, rmo.cost, rmo.delivered, rmo.date_delivered, rmo.created_by, rmo.created_at, rmo.updated_by, rmo.updated_at,
        us1.fullname AS created_by_fullname, us2.fullname AS updated_by_fullname,
        raw.code AS raw_material_code, fact.identifier AS factory_identifier
    FROM raw_material_order AS rmo
    LEFT JOIN users AS us1 ON us1.id = rmo.created_by
    LEFT JOIN users AS us2 ON us2.id = rmo.updated_by
    LEFT JOIN raw_material AS raw ON raw.id = rmo.id_raw_material
    LEFT JOIN factory AS fact ON fact.id = rmo.id_factory
"""


def RAW_MATERIAL_ORDER_COMPLEMENTS(order: str | None, direction: str | None):
    if not order:
        order = "created_at"  # Default ordering field
    if direction not in ["ASC", "DESC"]:
        direction = "ASC"  # Default direction

    # Validate order field
    if order in ["cost", "created_at"]:
        sql_sentence = f" ORDER BY rmo.{order} {direction}"
    else:
        sql_sentence = " ORDER BY rmo.created_at ASC"  # Fallback default

    return sql_sentence


def RAW_MATERIAL_ORDER_SEARCH():
    return """ WHERE (raw.code ILIKE :search OR fact.identifier ILIKE :search or rmo.state::text ILIKE :search OR rmo.delivered::text ILIKE :search OR rmo.created_at::text ILIKE :search) """

