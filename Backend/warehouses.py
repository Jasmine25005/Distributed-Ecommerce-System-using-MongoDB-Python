from database import db, client


warehouses = db["warehouses"]


def add_warehouse(warehouse_id, name, region, country, city):
    warehouse = {
        "warehouseId": warehouse_id,
        "name": name,
        "region": region,
        "location": {
            "country": country,
            "city": city
        }
    }

    result = warehouses.insert_one(warehouse)

    return {
        "success": True,
        "warehouseId": result.inserted_id
    }


def get_warehouse(warehouse_id):
    return warehouses.find_one(
        {"warehouseId": warehouse_id},
        {"_id": 0}
    )


def get_warehouses_by_region(region):
    return list(
        warehouses.find(
            {"region": region},
            {"_id": 0}
        )
    )