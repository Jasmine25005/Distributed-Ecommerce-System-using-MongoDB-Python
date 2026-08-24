from database import db


products = db["products"]


def add_product(product_id, name, category, price, description=""):
    product = {
        "productId": product_id,
        "name": name,
        "category": category,
        "price": price,
        "description": description
    }

    result = products.insert_one(product)

    return {
        "success": True,
        "productId": result.inserted_id
    }


def get_product(product_id):
    return products.find_one(
        {"productId": product_id},
        {"_id": 0}
    )


def search_products(keyword):
    query = {
        "$or": [
            {"name": {"$regex": keyword, "$options": "i"}},
            {"category": {"$regex": keyword, "$options": "i"}}
        ]
    }

    return list(products.find(query, {"_id": 0}))