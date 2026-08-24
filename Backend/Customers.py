from database import db

Customers = db["customers"]


# To view  column names of customers table
def get_customer_columns():
    sample_customer = Customers.find_one()
    if sample_customer:
        return list(sample_customer.keys())
    else:
        return []   

print(get_customer_columns())


def add_customer(_id, customerId, name, email, phone, address, createdAt):
    customer = {
        "_id": _id,
        "customerId": customerId,
        "name": name,
        "email": email,
        "phone": phone,
        "address": address,
        "createdAt": createdAt
    }

    result = Customers.insert_one(customer)

    return {
        "success": True,
        "customerId": result.inserted_id
    }

def get_customer(customerId):
    return Customers.find_one(
        {"customerId": customerId},
        {"_id": 0}
    )




