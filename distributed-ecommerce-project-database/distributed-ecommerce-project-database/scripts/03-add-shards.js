function addShardIfMissing(name, connectionString) {
  const admin = db.getSiblingDB("admin");
  const existing = admin.runCommand({ listShards: 1 }).shards || [];
  if (!existing.some(s => s._id === name)) {
    print(`Adding ${name}...`);
    printjson(sh.addShard(connectionString));
  } else {
    print(`${name} already exists.`);
  }
}
addShardIfMissing("rsEgypt", "rsEgypt/localhost:27101");
addShardIfMissing("rsEurope", "rsEurope/localhost:27102");
addShardIfMissing("rsUSA", "rsUSA/localhost:27103");

print("Current shards:");
printjson(db.getSiblingDB("admin").runCommand({ listShards: 1 }));
