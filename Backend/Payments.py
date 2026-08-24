from database import db



Payments = db["payments"]

# To view  column names of payments table
def get_payment_columns():
    sample_payment = Payments.find_one()
    if sample_payment:
        return list(sample_payment.keys())
    else:
        return []
print(get_payment_columns())

# TO ADD A PAYMENT
def add_payment(_id, paymentId, orderId, customerId, region, amount, method, status, paidAt):
    payment = {
        "_id": _id,
        "paymentId": paymentId,
        "orderId": orderId,
        "customerId": customerId,
        "region": region,
        "amount": amount,
        "paymentMethod": method,
        "status": status,
        "paidAt": paidAt
    }

    result = Payments.insert_one(payment)

    return {
        "success": True,
        "paymentId": result.inserted_id
    }

    

# TO GET A PAYMENT
def get_payment(paymentId):
    return Payments.find_one(
        {"paymentId": paymentId},
        {"_id": 0}
    )

# TO REMOVE A PAYMENT
def remove_payment(paymentId):
    result = Payments.delete_one({"paymentId": paymentId})
    if result.deleted_count > 0:
        return {"success": True, "message": "Payment removed successfully."}
    else:
        return {"success": False, "message": "Payment not found."}


# TO UPDATE A PAYMENT
def update_payment(paymentId, updated_fields):
    result = Payments.update_one(
        {"paymentId": paymentId},
        {"$set": updated_fields}
    )
    if result.modified_count > 0:
        return {"success": True, "message": "Payment updated successfully."}
    else:
        return {"success": False, "message": "Payment not found or no changes made."}


# TO GET ALL PAYMENTS
def get_all_payments():
    return list(Payments.find({}, {"_id": 0}))

