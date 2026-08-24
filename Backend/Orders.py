from database import db



Orders = db["orders"]
    

# To view  column names of customers table
def get_order_columns():
    sample_order = Orders.find_one()
    if sample_order:
        return list(sample_order.keys())
    else:
        return []   

print(get_order_columns())


def add_order(_id, orderId, customerId, status, totalAmount, createdAt):
    order = {
        "_id": _id,
        "orderId": orderId,
        "customerId": customerId,
        "status": status,
        "totalAmount": totalAmount,
        "createdAt": createdAt
    }

    result = Orders.insert_one(order)

    return {
        "success": True,
        "orderId": result.inserted_id
    }


# TO REMOVE AN ORDER
def remove_order(orderId):
    # PRINT ENTER AN ORDER ID TO REMOVE
    result = Orders.delete_one({"orderId": orderId})
    if result.deleted_count > 0:
        return {"success": True, "message": "Order removed successfully."}
    else:
        return {"success": False, "message": "Order not found."}


# TO GET AN ORDER
def get_order(orderId):
    return Orders.find_one(
        {"orderId": orderId},
        {"_id": 0}
    )

