const admin = db.getSiblingDB("admin");

// 1) Assign each physical shard to one geographic zone.
sh.addShardToZone("rsEgypt", "EGYPT_ZONE");
sh.addShardToZone("rsEurope", "EUROPE_ZONE");
sh.addShardToZone("rsUSA", "USA_ZONE");

// 2) Regional collections use a compound shard key:
//    region-like field first for locality + hashed ID second for better cardinality.
const specs = [
  { ns: "ecommerceDB.customers",  regionField: "region",          idField: "customerId" },
  { ns: "ecommerceDB.warehouses", regionField: "region",          idField: "warehouseId" },
  { ns: "ecommerceDB.inventory",  regionField: "region",          idField: "inventoryId" },
  { ns: "ecommerceDB.orders",     regionField: "customerRegion",  idField: "orderId" },
  { ns: "ecommerceDB.orderItems", regionField: "orderRegion",     idField: "orderItemId" },
  { ns: "ecommerceDB.payments",   regionField: "region",          idField: "paymentId" },
  { ns: "ecommerceDB.shipments",  regionField: "warehouseRegion", idField: "shipmentId" }
];

function makeBound(regionField, idField, regionValue, idValue) {
  const o = {};
  o[regionField] = regionValue;
  o[idField] = idValue;
  return o;
}

function alreadySharded(ns) {
  const [dbName, collName] = ns.split(".");
  const config = db.getSiblingDB("config");
  return config.collections.findOne({ _id: ns, dropped: { $ne: true } }) !== null;
}

for (const s of specs) {
  const egyptMin  = makeBound(s.regionField, s.idField, "EGYPT",  MinKey);
  const europeMin = makeBound(s.regionField, s.idField, "EUROPE", MinKey);
  const usaMin    = makeBound(s.regionField, s.idField, "USA",    MinKey);
  const maxBound  = makeBound(s.regionField, s.idField, MaxKey,   MinKey);

  // Zone ranges are defined BEFORE sharding so MongoDB can pre-split the empty collection.
  sh.updateZoneKeyRange(s.ns, egyptMin,  europeMin, "EGYPT_ZONE");
  sh.updateZoneKeyRange(s.ns, europeMin, usaMin,    "EUROPE_ZONE");
  sh.updateZoneKeyRange(s.ns, usaMin,    maxBound,  "USA_ZONE");

  if (!alreadySharded(s.ns)) {
    const key = {};
    key[s.regionField] = 1;
    key[s.idField] = "hashed";

    print(`Sharding ${s.ns} with ${JSON.stringify(key)}...`);
    printjson(
      sh.shardCollection(
        s.ns,
        key,
        false,
        { presplitHashedZones: true }
      )
    );
  } else {
    print(`${s.ns} is already sharded.`);
  }
}

// Products are global, so they are fragmented by hash across all three shards.
if (!alreadySharded("ecommerceDB.products")) {
  print("Sharding global product catalog by hashed productId...");
  printjson(
    sh.shardCollection(
      "ecommerceDB.products",
      { productId: "hashed" }
    )
  );
}

// Helpful secondary indexes for teammates. These do not replace Team Member 4's
// before/after optimization experiment; they are only baseline application indexes.
const e = db.getSiblingDB("ecommerceDB");
e.customers.createIndex({ email: 1 });
e.products.createIndex({ category: 1 });
e.inventory.createIndex({ region: 1, productId: 1, warehouseId: 1 });
e.orders.createIndex({ customerId: 1, createdAt: -1 });
e.orderItems.createIndex({ orderId: 1 });
e.payments.createIndex({ orderId: 1 });
e.shipments.createIndex({ orderId: 1 });

print("Fragmentation and baseline indexes configured.");
