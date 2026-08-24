from datetime import datetime, timezone

from pymongo import ReturnDocument

from database import db, client



inventory = db["inventory"]


def add_inventory(
    inventory_id,
    product_id,
    warehouse_id,
    region,
    quantity,
    reserved_quantity=0
):
    item = {
        "inventoryId": inventory_id,
        "productId": product_id,
        "warehouseId": warehouse_id,
        "region": region,
        "quantity": quantity,
        "reservedQuantity": reserved_quantity,
        "lastUpdated": datetime.now(timezone.utc)
    }

    result = inventory.insert_one(item)

    return {
        "success": True,
        "inventoryId": result.inserted_id
    }


def get_inventory(product_id, warehouse_id=None):
    query = {"productId": product_id}

    if warehouse_id:
        query["warehouseId"] = warehouse_id

    return list(inventory.find(query, {"_id": 0}))


def get_available_quantity(product_id, warehouse_id):
    item = inventory.find_one(
        {
            "productId": product_id,
            "warehouseId": warehouse_id
        },
        {
            "_id": 0,
            "quantity": 1,
            "reservedQuantity": 1
        }
    )

    if item is None:
        return 0

    return item["quantity"] - item["reservedQuantity"]


def purchase_stock(inventory_id, region, quantity):
    """
    Atomically checks available stock and decreases quantity.
    The shard key is included so MongoDB targets one shard.
    """

    result = inventory.find_one_and_update(
        {
            "inventoryId": inventory_id,
            "region": region,
            "$expr": {
                "$gte": [
                    {"$subtract": ["$quantity", "$reservedQuantity"]},
                    quantity
                ]
            }
        },
        {
            "$inc": {
                "quantity": -quantity
            },
            "$set": {
                "lastUpdated": datetime.now(timezone.utc)
            }
        },
        return_document=ReturnDocument.AFTER,
        projection={
            "_id": 0,
            "inventoryId": 1,
            "productId": 1,
            "warehouseId": 1,
            "region": 1,
            "quantity": 1,
            "reservedQuantity": 1
        }
    )

    if result is None:
        return {
            "success": False,
            "message": "Insufficient stock"
        }

    return {
        "success": True,
        "message": "Purchase successful",
        "remainingQuantity": result["quantity"]
    }