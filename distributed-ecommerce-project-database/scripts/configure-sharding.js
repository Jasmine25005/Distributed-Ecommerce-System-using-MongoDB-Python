use("ecommerceDB");

sh.addShardToZone("rsEgypt", "EGYPT_ZONE");
sh.addShardToZone("rsEurope", "EUROPE_ZONE");
sh.addShardToZone("rsUSA", "USA_ZONE");

function configureRegionalCollection(ns, regionField, idField) {
    sh.updateZoneKeyRange(
        ns,
        { [regionField]: "EGYPT", [idField]: MinKey },
        { [regionField]: "EGYPT", [idField]: MaxKey },
        "EGYPT_ZONE"
    );

    sh.updateZoneKeyRange(
        ns,
        { [regionField]: "EUROPE", [idField]: MinKey },
        { [regionField]: "EUROPE", [idField]: MaxKey },
        "EUROPE_ZONE"
    );

    sh.updateZoneKeyRange(
        ns,
        { [regionField]: "USA", [idField]: MinKey },
        { [regionField]: "USA", [idField]: MaxKey },
        "USA_ZONE"
    );

    const key = {};
    key[regionField] = 1;
    key[idField] = 1;

    try {
        sh.shardCollection(ns, key);
        print(`Sharded ${ns}`);
    } catch (e) {
        print(`${ns}: ${e.message}`);
    }
}

configureRegionalCollection("ecommerceDB.customers",   "region",          "customerId");
configureRegionalCollection("ecommerceDB.warehouses",  "region",          "warehouseId");
configureRegionalCollection("ecommerceDB.inventory",   "region",          "inventoryId");
configureRegionalCollection("ecommerceDB.orders",      "customerRegion",  "orderId");
configureRegionalCollection("ecommerceDB.orderItems",  "orderRegion",     "orderItemId");
configureRegionalCollection("ecommerceDB.payments",    "region",          "paymentId");
configureRegionalCollection("ecommerceDB.shipments",   "warehouseRegion", "shipmentId");

print("Products remain unsharded as a shared global catalog.");
print("Sharding configuration complete.");
