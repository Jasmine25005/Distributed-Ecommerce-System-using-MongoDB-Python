# Distributed E-Commerce Database — Native MongoDB

Docker is not required.

## Architecture

```text
                         Application
                              |
                     mongos : 27017
                              |
                    Config Server cfgRS
                          : 27019
                              |
           +------------------+------------------+
           |                  |                  |
        rsEgypt            rsEurope            rsUSA
        :27101             :27102              :27103
           |                  |                  |
      EGYPT_ZONE         EUROPE_ZONE          USA_ZONE
```

## Fragmentation

| Collection | Shard key |
|---|---|
| customers | `{ region: 1, customerId: 1 }` |
| warehouses | `{ region: 1, warehouseId: 1 }` |
| inventory | `{ region: 1, inventoryId: 1 }` |
| orders | `{ customerRegion: 1, orderId: 1 }` |
| orderItems | `{ orderRegion: 1, orderItemId: 1 }` |
| payments | `{ region: 1, paymentId: 1 }` |
| shipments | `{ warehouseRegion: 1, shipmentId: 1 }` |

`products` is intentionally unsharded as a shared global catalog.

## Start an already-initialized cluster

```powershell
.\scripts\start-cluster.ps1
```

## Connect

```powershell
mongosh --port 27017
```

If `mongosh` is not in PATH, use the full path to `mongosh.exe`.

## Seed demo data

```powershell
mongosh --port 27017 --file .\scripts\seed-data.js
```

## Verify fragmentation

```powershell
mongosh --port 27017 --file .\scripts\verify-fragmentation.js
```

## Stop the cluster

```powershell
.\scripts\stop-cluster.ps1
```

The three database sites are simulated as separate MongoDB processes on one Windows machine.
