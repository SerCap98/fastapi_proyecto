

CREATE_WAREHOUSE_PRODUCT_INVENTORY = """
    INSERT INTO warehouse_product_inventory (id, id_warehouse, id_manufactured_product, available_product, created_by, created_at)
    VALUES (:id, :id_warehouse, :id_manufactured_product, :available_product, :created_by, :created_at)
    RETURNING id, id_warehouse, id_manufactured_product, available_product, created_by, created_at;
"""

GET_WAREHOUSE_PRODUCT_INVENTORY_BY_ID = """
    SELECT * FROM warehouse_product_inventory
    WHERE id = :id;
"""

DISCOUNT_WAREHOUSE_PRODUCT_INVENTORY_BY_ID = """
    UPDATE warehouse_product_inventory
    SET available_product = available_product - :decrease_quantity,
        updated_at = :updated_at,
        updated_by = :updated_by
    WHERE id = :id
    RETURNING *
"""

TRANSFER_WAREHOUSE_PRODUCT_INVENTORY_BY_ID = """
    UPDATE warehouse_product_inventory
    SET id_warehouse = :new_warehouse_id,
        updated_at = :updated_at,
        updated_by = :updated_by
    WHERE id = :id
    RETURNING *;
"""
DELETE_WAREHOUSE_PRODUCT_INVENTORY_BY_ID = """
     DELETE FROM warehouse_product_inventory
     WHERE id = :id;
"""

LIST_WAREHOUSE_PRODUCT_INVENTORY  = """
    SELECT wpi.*, prod.name AS product_name, wh.name AS warehouse_name, wh.type AS warehouse_type, mp.lot_number AS lot_number,
           us1.fullname AS created_by_fullname, us2.fullname AS updated_by_fullname
    FROM warehouse_product_inventory AS wpi
    LEFT JOIN users AS us1 ON us1.id = wpi.created_by
    LEFT JOIN users AS us2 ON us2.id = wpi.updated_by
    JOIN warehouse AS wh ON wpi.id_warehouse = wh.id
    JOIN manufactured_product AS mp ON wpi.id_manufactured_product = mp.id
    JOIN product AS prod ON mp.id_product = prod.id
"""

def WAREHOUSE_PRODUCT_INVENTORY_COMPLEMENTS(order: str | None, direction: str | None):
    sql_sentence = ""
    if not order and not direction:
        sql_sentence = " ORDER BY wpi.available_product ASC"
    elif order == "available_product" and direction == "DESC":
        sql_sentence = " ORDER BY wpi.available_product DESC"
    elif order == "available_product" and (direction == "ASC" or direction is None):
        sql_sentence = " ORDER BY wpi.available_product ASC"
    elif order == "created_at" and direction == "DESC":
        sql_sentence = " ORDER BY wpi.created_at DESC"
    elif order == "created_at" and (direction == "ASC" or direction is None):
        sql_sentence = " ORDER BY wpi.created_at ASC"

    return sql_sentence



def WAREHOUSE_PRODUCT_INVENTORY_SEARCH():
    return """ WHERE (wh.name ILIKE :search or wh.type::text ILIKE :search OR prod.name ILIKE :search ) """

LIST_SUMMARY_WAREHOUSE_PRODUCT_INVENTORY= """
SELECT 
    W.name AS warehouse_name,
    P.name AS product_name,
    SUM(WPI.available_product) AS total_available
FROM 
    WAREHOUSE_PRODUCT_INVENTORY WPI
LEFT JOIN 
    WAREHOUSE W ON WPI.id_warehouse = W.id
LEFT JOIN 
    MANUFACTURED_PRODUCT MP ON WPI.id_manufactured_product = MP.id
LEFT JOIN 
    PRODUCT P ON MP.id_product = P.id
{search_condition}
GROUP BY 
    W.name, P.name
{order_condition}
"""


def WAREHOUSE_SUMMARY_PRODUCT_INVENTORY_SEARCH(search: str | None):
    if search:
        return "WHERE (W.name ILIKE '%' || :search || '%' OR P.name ILIKE '%' || :search || '%') "
    else:
        return ""


def WAREHOUSE_SUMMARY_PRODUCT_INVENTORY_COMPLEMENTS(order: str | None, direction: str | None):
    sql_sentence = ""
    if not order and not direction:
        sql_sentence = " ORDER BY total_available ASC"
    elif order == "total_available" and direction == "DESC":
        sql_sentence = " ORDER BY total_available DESC"
    elif order == "total_available" and (direction == "ASC" or direction is None):
        sql_sentence = " ORDER BY total_available ASC"

    return sql_sentence
