# Schema Summary

| Collection | Key business fields | Regional field |
|---|---|---|
| Customers | customerId, name, email, address | region |
| Products | productId, name, category, price | none/global |
| Warehouses | warehouseId, name, location | region |
| Inventory | inventoryId, productId, warehouseId, quantity | region |
| Orders | orderId, customerId, status, totalAmount | customerRegion |
| Order Items | orderItemId, orderId, productId, quantity, unitPrice | orderRegion |
| Payments | paymentId, orderId, amount, method, status | region |
| Shipments | shipmentId, orderId, warehouseId, status | warehouseRegion |

## Relationships

```text
Customers
   |
   +----< Orders
            |
            +----< Order Items >---- Products
            |
            +---- Payments
            |
            +---- Shipments ---- Warehouses
                                  |
                                  +---- Inventory >---- Products
```

MongoDB itself does not enforce relational foreign keys here. The application/backend is responsible for validating referenced IDs.
