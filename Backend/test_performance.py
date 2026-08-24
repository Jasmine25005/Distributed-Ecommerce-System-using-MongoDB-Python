import time
import json
import os
from datetime import datetime

from database import db, client

def run_aggregation(collection_name, pipeline, label=""):
    collection = db[collection_name]
    start = time.perf_counter()
    results = list(collection.aggregate(pipeline, allowDiskUse=True))
    elapsed_ms = (time.perf_counter() - start) * 1000
    explain_cmd = {"aggregate": collection_name, "pipeline": pipeline, "cursor": {}, "explain": True}
    explain_result = db.command(explain_cmd)
    try:
        s = explain_result.get("executionStats", {})
        tke, tde, nr, etm = s.get("totalKeysExamined",0), s.get("totalDocsExamined",0), s.get("nReturned", len(results)), s.get("executionTimeMillis",0)
    except:
        tke, tde, nr, etm = 0, 0, len(results), 0
    # Shards info
    shards_info = []
    try:
        shards = explain_result.get("shards", {})
        for shard_name, shard_data in shards.items():
            ss = shard_data.get("executionStats", {})
            shards_info.append({
                "shard": shard_name,
                "docsExamined": ss.get("totalDocsExamined", 0),
                "keysExamined": ss.get("totalKeysExamined", 0),
                "nReturned": ss.get("nReturned", 0),
                "executionTimeMillis": ss.get("executionTimeMillis", 0),
            })
    except:
        pass
    return {
        "results": results, "results_count": len(results),
        "wall_clock_ms": round(elapsed_ms,2), "total_keys_examined": tke,
        "total_docs_examined": tde, "n_returned": nr, "execution_time_ms": etm,
        "shards_info": shards_info, "shards_accessed": len(shards_info),
    }

def print_separator(title=""):
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def print_metrics(m):
    print(f"  Wall-clock time      : {m['wall_clock_ms']} ms")
    print(f"  Execution time (exp) : {m['execution_time_ms']} ms")
    print(f"  Docs examined        : {m['total_docs_examined']}")
    print(f"  Keys examined        : {m['total_keys_examined']}")
    print(f"  Docs returned        : {m['n_returned']}")
    print(f"  Shards accessed      : {m['shards_accessed']}")
    if m["shards_info"]:
        for si in m["shards_info"]:
            print(f"    -> {si['shard']}: docs={si['docsExamined']}, keys={si['keysExamined']}, returned={si['nReturned']}, time={si['executionTimeMillis']}ms")

def print_comparison(b, a):
    print(f"\n  {'Metric':<25} {'Before':>12} {'After':>12} {'Improvement':>14}")
    print("  " + "-" * 65)
    for label, bv, av in [("Wall-clock time (ms)",b["wall_clock_ms"],a["wall_clock_ms"]),("Docs examined",b["total_docs_examined"],a["total_docs_examined"]),("Keys examined",b["total_keys_examined"],a["total_keys_examined"]),("Shards accessed",b["shards_accessed"],a["shards_accessed"])]:
        imp = f"{round(((bv-av)/bv)*100,1)}%" if bv > 0 else ("no change" if bv==av else "N/A")
        print(f"  {label:<25} {bv:>12} {av:>12} {imp:>14}")

QUERY1 = [
    {"$match":{"region":"EGYPT","status":{"$in":["completed","shipped","processing"]}}},
    {"$lookup":{"from":"customers","let":{"custId":"$customerId"},"pipeline":[{"$match":{"$expr":{"$eq":["$customerId","$$custId"]}}},{"$project":{"_id":0,"customerId":1,"name":1,"email":1}}],"as":"customer_info"}},
    {"$unwind":{"path":"$customer_info","preserveNullAndEmptyArrays":True}},
    {"$lookup":{"from":"orderItems","localField":"orderId","foreignField":"orderId","as":"items"}},
    {"$unwind":{"path":"$items","preserveNullAndEmptyArrays":True}},
    {"$lookup":{"from":"products","localField":"items.productId","foreignField":"productId","as":"product_info"}},
    {"$unwind":{"path":"$product_info","preserveNullAndEmptyArrays":True}},
    {"$lookup":{"from":"payments","localField":"orderId","foreignField":"orderId","as":"payment_info"}},
    {"$unwind":{"path":"$payment_info","preserveNullAndEmptyArrays":True}},
    {"$lookup":{"from":"shipments","localField":"orderId","foreignField":"orderId","as":"shipment_info"}},
    {"$unwind":{"path":"$shipment_info","preserveNullAndEmptyArrays":True}},
    {"$group":{"_id":"$orderId","orderDate":{"$first":"$orderDate"},"status":{"$first":"$status"},"customerName":{"$first":"$customer_info.name"},"customerEmail":{"$first":"$customer_info.email"},"totalAmount":{"$sum":{"$multiply":["$items.quantity","$items.unitPrice"]}},"itemsCount":{"$sum":1},"paymentStatus":{"$first":"$payment_info.status"},"paymentMethod":{"$first":"$payment_info.method"},"shipmentStatus":{"$first":"$shipment_info.status"},"products":{"$push":{"name":"$product_info.name","quantity":"$items.quantity","unitPrice":"$items.unitPrice"}}}},
    {"$sort":{"totalAmount":-1}},
    {"$project":{"_id":0,"orderId":"$_id","orderDate":1,"status":1,"customerName":1,"customerEmail":1,"totalAmount":1,"itemsCount":1,"paymentStatus":1,"paymentMethod":1,"shipmentStatus":1,"products":1}}
]

QUERY2 = [
    {"$match":{"$expr":{"$lte":[{"$subtract":["$quantity","$reservedQuantity"]},50]},"quantity":{"$gt":0}}},
    {"$lookup":{"from":"products","localField":"productId","foreignField":"productId","as":"product_info"}},
    {"$unwind":{"path":"$product_info","preserveNullAndEmptyArrays":True}},
    {"$lookup":{"from":"warehouses","localField":"warehouseId","foreignField":"warehouseId","as":"warehouse_info"}},
    {"$unwind":{"path":"$warehouse_info","preserveNullAndEmptyArrays":True}},
    {"$addFields":{"availableQuantity":{"$subtract":["$quantity","$reservedQuantity"]}}},
    {"$sort":{"availableQuantity":1,"region":1}},
    {"$project":{"_id":0,"inventoryId":1,"productId":1,"productName":"$product_info.name","category":"$product_info.category","price":"$product_info.price","warehouseId":1,"warehouseName":"$warehouse_info.name","warehouseCity":"$warehouse_info.location.city","region":1,"quantity":1,"reservedQuantity":1,"availableQuantity":1}}
]

INDEXES = [
    {"collection":"orders","keys":[("region",1),("status",1)],"name":"idx_orders_region_status"},
    {"collection":"customers","keys":[("customerId",1)],"name":"idx_customers_customerId"},
    {"collection":"orderItems","keys":[("orderId",1)],"name":"idx_orderItems_orderId"},
    {"collection":"orderItems","keys":[("productId",1)],"name":"idx_orderItems_productId"},
    {"collection":"products","keys":[("productId",1)],"name":"idx_products_productId"},
    {"collection":"payments","keys":[("orderId",1)],"name":"idx_payments_orderId"},
    {"collection":"shipments","keys":[("orderId",1)],"name":"idx_shipments_orderId"},
    {"collection":"inventory","keys":[("quantity",1),("reservedQuantity",1)],"name":"idx_inventory_qty_reserved"},
    {"collection":"inventory","keys":[("warehouseId",1)],"name":"idx_inventory_warehouseId"},
    {"collection":"warehouses","keys":[("warehouseId",1)],"name":"idx_warehouses_warehouseId"}
]

def main():
    print("#" * 70)
    print("#  TASK 4 - Performance & Query Optimization")
    print("#  Uses existing cluster data - does NOT modify any collections")
    print("#" * 70)
    try:
        client.admin.command("ping")
        print("\n  [OK] Connected to MongoDB!")
    except Exception as e:
        print(f"\n  [ERROR] {e}")
        return

    # Check sharding
    try:
        shards = db.command("listShards").get("shards", [])
        print(f"  [OK] Sharded cluster: {len(shards)} shards")
        for s in shards:
            print(f"       - {s['_id']}")
    except:
        print("  [INFO] Standalone MongoDB (not sharded)")

    # Check data
    colls = ["orders","customers","orderItems","products","payments","shipments","inventory","warehouses"]
    total = 0
    print("\n  Existing data:")
    for c in colls:
        try: cnt = db[c].count_documents({})
        except: cnt = 0
        total += cnt
        print(f"    {c}: {cnt}")
    print(f"  Total: {total} documents")
    if total == 0:
        print("  [ERROR] No data found! Run Task 1 first.")
        return

    # Check if collection name is orderitems (lowercase) or orderItems (camelCase)
    real_name = "orderItems"
    if db["orderItems"].count_documents({}) == 0 and db["orderitems"].count_documents({}) > 0:
        real_name = "orderitems"
        print(f"\n  [INFO] Using collection name: {real_name}")
        QUERY1[3]["$lookup"]["from"] = real_name

    print_separator("PHASE 1: QUERIES WITHOUT INDEXES")
    for idx in INDEXES:
        try: db[idx["collection"]].drop_index(idx["name"])
        except: pass
    print("\n  >> Query 1 (Regional Sales - EGYPT) WITHOUT indexes...")
    q1b = run_aggregation("orders", QUERY1)
    print_metrics(q1b)
    print("\n  >> Query 2 (Low-Stock Products) WITHOUT indexes...")
    q2b = run_aggregation("inventory", QUERY2)
    print_metrics(q2b)


    print_separator("PHASE 2: CREATING INDEXES")
    for idx in INDEXES:
        try:
            db[idx["collection"]].create_index(idx["keys"], name=idx["name"])
            print(f"    Created: {idx['collection']}.{idx['name']}")
        except Exception as e:
            print(f"    [INFO] Skipped: {idx['collection']}.{idx['name']} (Index already exists)")

    print_separator("PHASE 3: QUERIES WITH INDEXES")
    print("\n  >> Query 1 WITH indexes...")
    q1a = run_aggregation("orders", QUERY1)
    print_metrics(q1a)
    print("\n  >> Query 2 WITH indexes...")
    q2a = run_aggregation("inventory", QUERY2)
    print_metrics(q2a)

    print_separator("PHASE 4: COMPARISON")
    print("\nQuery 1: Regional Sales Report")
    print_comparison(q1b, q1a)
    print("\nQuery 2: Low-Stock Products")
    print_comparison(q2b, q2a)

    # Save results to JSON
    def calc_imp(bv, av):
        if bv > 0: return round(((bv-av)/bv)*100, 1)
        return 0.0
    output = {
        "timestamp": datetime.now().isoformat(),
        "query1": {
            "description": "Regional Sales Report (Targeted - EGYPT)",
            "before": {k:v for k,v in q1b.items() if k!="results"},
            "after":  {k:v for k,v in q1a.items() if k!="results"},
            "improvement_pct": calc_imp(q1b["wall_clock_ms"], q1a["wall_clock_ms"]),
        },
        "query2": {
            "description": "Low-Stock Products (Scatter-Gather)",
            "before": {k:v for k,v in q2b.items() if k!="results"},
            "after":  {k:v for k,v in q2a.items() if k!="results"},
            "improvement_pct": calc_imp(q2b["wall_clock_ms"], q2a["wall_clock_ms"]),
        },
        "indexes_created": [{"collection":i["collection"],"name":i["name"],"keys":", ".join(f"{x}:{v}" for x,v in i["keys"])} for i in INDEXES],
    }
    results_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results.json")
    with open(results_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\n  Results saved to: {results_path}")

    print_separator("SUMMARY")
    print(f"\n  Query 1: {q1a['results_count']} results | {q1b['wall_clock_ms']}ms -> {q1a['wall_clock_ms']}ms")
    print(f"  Query 2: {q2a['results_count']} results | {q2b['wall_clock_ms']}ms -> {q2a['wall_clock_ms']}ms")
    print("\n  Indexes:")
    for idx in INDEXES:
        k = ", ".join(f"{x}:{v}" for x,v in idx["keys"])
        print(f"    - {idx['collection']}.{idx['name']} ({k})")
    print("\n" + "#" * 70 + "\n")

if __name__ == "__main__":
    main()