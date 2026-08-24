use("ecommerceDB");

print("\n========================================");
print("       DISTRIBUTED DATABASE CHECK");
print("========================================\n");

print("=== 1. DATABASE SITES / SHARDS ===");
printjson(sh.listShards());

print("\n=== 2. SHARDED DATA DISTRIBUTION ===");
const distribution = sh.getShardedDataDistribution();
printjson(distribution);

print("\n=== 3. ZONE ASSIGNMENTS ===");
const configDB = db.getSiblingDB("config");

printjson(
    configDB.shards.find(
        {},
        { _id: 1, host: 1, tags: 1 }
    ).toArray()
);

print("\n=== 4. SHARDED COLLECTIONS ===");

printjson(
    configDB.collections.find(
        {
            _id: /^ecommerceDB\./,
            dropped: { $ne: true }
        },
        {
            _id: 1,
            key: 1
        }
    ).toArray()
);

print("\n=== 5. ZONE RANGES ===");

printjson(
    configDB.tags.find(
        { ns: /^ecommerceDB\./ }
    ).sort(
        { ns: 1 }
    ).toArray()
);

print("\n=== 6. GLOBAL PRODUCTS COLLECTION ===");

print(
    "Products documents: " +
    db.products.countDocuments({})
);

print(
    "Products is intentionally unsharded."
);

print("\n=== VERIFICATION COMPLETE ===");