const e = db.getSiblingDB("ecommerceDB");

print("\n================ CLUSTER STATUS ================\n");
sh.status();

print("\n================ SHARDED DATA DISTRIBUTION ================\n");
printjson(sh.getShardedDataDistribution());

print("\n================ CUSTOMERS DISTRIBUTION ================\n");
e.customers.getShardDistribution();

print("\n================ INVENTORY DISTRIBUTION ================\n");
e.inventory.getShardDistribution();

print("\n================ ORDERS DISTRIBUTION ================\n");
e.orders.getShardDistribution();

print("\n================ TARGETED QUERY EXPLAINS ================\n");

function showShards(label, collection, query) {
  const exp = collection.find(query).explain("executionStats");
  const shardNames = [];

  function walk(x) {
    if (!x || typeof x !== "object") return;
    if (Array.isArray(x)) {
      x.forEach(walk);
      return;
    }
    if (typeof x.shardName === "string") shardNames.push(x.shardName);
    for (const k of Object.keys(x)) walk(x[k]);
  }

  walk(exp);
  print(`${label}: ${JSON.stringify(query)}`);
  print(`Shards observed in explain: ${[...new Set(shardNames)].join(", ") || "(inspect explain output manually)"}`);
}

showShards(
  "Egypt customer lookup",
  e.customers,
  { region: "EGYPT", customerId: "C-EG-001" }
);

showShards(
  "Europe customer lookup",
  e.customers,
  { region: "EUROPE", customerId: "C-EU-001" }
);

showShards(
  "USA customer lookup",
  e.customers,
  { region: "USA", customerId: "C-US-001" }
);

print("\nVerification complete.");
