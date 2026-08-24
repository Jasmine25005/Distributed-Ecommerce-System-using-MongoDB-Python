# Fragmentation Report

## What was fragmented?

Customers, Warehouses, Inventory, Orders, Order Items, Payments, and Shipments were horizontally fragmented.

Products were kept unsharded as a shared global catalog.

## How?

Regional fields form the first part of each compound shard key:

- Customers: `{ region: 1, customerId: 1 }`
- Warehouses: `{ region: 1, warehouseId: 1 }`
- Inventory: `{ region: 1, inventoryId: 1 }`
- Orders: `{ customerRegion: 1, orderId: 1 }`
- Order Items: `{ orderRegion: 1, orderItemId: 1 }`
- Payments: `{ region: 1, paymentId: 1 }`
- Shipments: `{ warehouseRegion: 1, shipmentId: 1 }`

MongoDB Zones map regional ranges to the correct shard.

## Where?

- `EGYPT` -> `rsEgypt`
- `EUROPE` -> `rsEurope`
- `USA` -> `rsUSA`

## Why?

The approach makes regional data local to the appropriate database site and provides a clear distributed-database design.

Customer-side data follows the customer/order region, while fulfillment-side data follows the warehouse region.

This enables cross-site transactions. For example, a European customer can place an order fulfilled from an Egyptian warehouse, requiring access to both `rsEurope` and `rsEgypt`.
