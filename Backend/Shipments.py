from database import db



Shipments = db["shipments"]

# To view column names of shipments table
def get_shipment_columns():
    sample_shipment = Shipments.find_one()
    if sample_shipment:
        return list(sample_shipment.keys())
    else:
        return []
print(get_shipment_columns())

# TO ADD A SHIPMENT
def add_shipment(_id, shipmentId, orderId, customerId, region, amount, method, status, shippedAt):
    shipment = {
        "_id": _id,
        "shipmentId": shipmentId,
        "orderId": orderId,
        "customerId": customerId,
        "region": region,
        "amount": amount,
        "shipmentMethod": method,
        "status": status,
        "shippedAt": shippedAt
    }

    result = Shipments.insert_one(shipment)

    return {
        "success": True,
        "shipmentId": result.inserted_id
    }

    

# TO GET A SHIPMENT
def get_shipment(shipmentId):
    return Shipments.find_one(
        {"shipmentId": shipmentId},
        {"_id": 0}
    )

# TO REMOVE A SHIPMENT
def remove_shipment(shipmentId):
    result = Shipments.delete_one({"shipmentId": shipmentId})
    if result.deleted_count > 0:
        return {"success": True, "message": "Shipment removed successfully."}
    else:
        return {"success": False, "message": "Shipment not found."}


# TO UPDATE A SHIPMENT
def update_shipment(shipmentId, updated_fields):
    result = Shipments.update_one(
        {"shipmentId": shipmentId},
        {"$set": updated_fields}
    )
    if result.modified_count > 0:
        return {"success": True, "message": "Shipment updated successfully."}
    else:
        return {"success": False, "message": "Shipment not found or no changes made."}


# TO GET ALL SHIPMENTS
def get_all_shipments():
    return list(Shipments.find({}, {"_id": 0}))