const config = rs.conf();

const existingHosts = config.members.map(m => m.host);

if (!existingHosts.includes("localhost:27111")) {
    rs.add("localhost:27111");
    print("Added Egypt Secondary 1: localhost:27111");
} else {
    print("Egypt Secondary 1 already exists.");
}

sleep(5000);

const updatedConfig = rs.conf();
const updatedHosts = updatedConfig.members.map(m => m.host);

if (!updatedHosts.includes("localhost:27112")) {
    rs.add("localhost:27112");
    print("Added Egypt Secondary 2: localhost:27112");
} else {
    print("Egypt Secondary 2 already exists.");
}

print("Egypt Replica Set configuration:");
rs.status();