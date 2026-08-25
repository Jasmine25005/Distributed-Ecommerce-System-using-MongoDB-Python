print("==============================================");
print("      FAILURE HANDLING VERIFICATION");
print("==============================================");

const status = rs.status();

status.members.forEach(function(member) {
    print(
        member.name +
        " | State: " +
        member.stateStr +
        " | Health: " +
        member.health
    );
});

const primary = status.members.find(
    member => member.stateStr === "PRIMARY"
);

if (primary) {
    print("");
    print("CURRENT PRIMARY: " + primary.name);
    print("FAILOVER STATUS: PASS");
} else {
    print("");
    print("CURRENT PRIMARY: NONE");
    print("FAILOVER STATUS: FAIL");
}

print("==============================================");