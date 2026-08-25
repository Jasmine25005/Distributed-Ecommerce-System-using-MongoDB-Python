# Failure Handling — Role 5

## 1. Objective

Demonstrate fault tolerance and recovery in the distributed
MongoDB e-commerce system.

## 2. Failure Scenario

The Egypt shard contains three replica-set members:

- localhost:27101 — Primary
- localhost:27111 — Secondary
- localhost:27112 — Secondary

## 3. Normal State

Before failure:

27101 → PRIMARY
27111 → SECONDARY
27112 → SECONDARY

## 4. Failure

The primary node on port 27101 is stopped intentionally.

## 5. Failover

The remaining replica-set members detect the failure.
An election is performed and one of the secondary members
becomes the new primary.

Expected result:

27101 → DOWN
27111 → SECONDARY
27112 → PRIMARY

## 6. Data Availability

The system is accessed through mongos on port 27017.
The database remains accessible after the primary failure.

## 7. Recovery

The failed node on port 27101 is restarted.

It rejoins the replica set and synchronizes with the current
primary.

Final state:

27101 → SECONDARY
27111 → SECONDARY
27112 → PRIMARY

## 8. Result

The failure-handling scenario demonstrates:

- Failure detection
- Replica-set election
- Automatic failover
- Continued database availability
- Recovery and resynchronization