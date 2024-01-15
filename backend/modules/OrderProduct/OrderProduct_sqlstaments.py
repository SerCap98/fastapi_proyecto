
CREATE_ORDER_PRODUCT = """
    INSERT INTO order_product (id, id_product,client,total_cost,quantity,note,discount,delivered,date_delivered, created_by, created_at)
    VALUES (:id, :product,:client,:total_cost,:quantity,:note,:discount,:delivered,:date_delivered, :created_by, :created_at)
    RETURNING id, id_product,client,total_cost,quantity,note,discount,delivered,date_delivered, created_by, created_at;
"""

