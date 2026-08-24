use("ecommerceDB");

for (const c of [
    "customers", "products", "warehouses", "inventory",
    "orders", "orderItems", "payments", "shipments"
]) {
    db[c].deleteMany({});
}

db.customers.insertMany([
  { customerId: "C-EG-001", name: "Ahmed", email: "ahmed@example.com", region: "EGYPT", createdAt: new Date() },
  { customerId: "C-EU-001", name: "Anna", email: "anna@example.com", region: "EUROPE", createdAt: new Date() },
  { customerId: "C-US-001", name: "John", email: "john@example.com", region: "USA", createdAt: new Date() }
]);

db.products.insertMany([
  { productId: "P001", name: "Laptop", category: "Electronics", price: 1200 },
  { productId: "P002", name: "Headphones", category: "Electronics", price: 150 },
  { productId: "P003", name: "Keyboard", category: "Electronics", price: 90 }
]);

db.warehouses.insertMany([
  { warehouseId: "W-EG-001", name: "Cairo Warehouse", region: "EGYPT" },
  { warehouseId: "W-EU-001", name: "Berlin Warehouse", region: "EUROPE" },
  { warehouseId: "W-US-001", name: "New York Warehouse", region: "USA" }
]);

db.inventory.insertMany([
  { inventoryId: "I-EG-001", productId: "P001", warehouseId: "W-EG-001", region: "EGYPT", quantity: 2 },
  { inventoryId: "I-EU-001", productId: "P002", warehouseId: "W-EU-001", region: "EUROPE", quantity: 10 },
  { inventoryId: "I-US-001", productId: "P003", warehouseId: "W-US-001", region: "USA", quantity: 15 }
]);

db.orders.insertMany([
  { orderId: "O-EG-001", customerId: "C-EG-001", customerRegion: "EGYPT", totalAmount: 1200, status: "CONFIRMED", createdAt: new Date() },
  { orderId: "O-EU-001", customerId: "C-EU-001", customerRegion: "EUROPE", totalAmount: 1200, status: "CONFIRMED", createdAt: new Date() },
  { orderId: "O-US-001", customerId: "C-US-001", customerRegion: "USA", totalAmount: 90, status: "CONFIRMED", createdAt: new Date() }
]);

db.orderItems.insertMany([
  { orderItemId: "OI-EG-001", orderId: "O-EG-001", orderRegion: "EGYPT", productId: "P001", quantity: 1, unitPrice: 1200 },
  { orderItemId: "OI-EU-001", orderId: "O-EU-001", orderRegion: "EUROPE", productId: "P001", quantity: 1, unitPrice: 1200 },
  { orderItemId: "OI-US-001", orderId: "O-US-001", orderRegion: "USA", productId: "P003", quantity: 1, unitPrice: 90 }
]);

db.payments.insertMany([
  { paymentId: "PAY-EG-001", orderId: "O-EG-001", region: "EGYPT", amount: 1200, status: "SUCCESS" },
  { paymentId: "PAY-EU-001", orderId: "O-EU-001", region: "EUROPE", amount: 1200, status: "SUCCESS" },
  { paymentId: "PAY-US-001", orderId: "O-US-001", region: "USA", amount: 90, status: "SUCCESS" }
]);

db.shipments.insertMany([
  { shipmentId: "S-EG-001", orderId: "O-EG-001", warehouseId: "W-EG-001", warehouseRegion: "EGYPT", destinationRegion: "EGYPT", status: "SHIPPED" },
  { shipmentId: "S-EU-001", orderId: "O-EU-001", warehouseId: "W-EG-001", warehouseRegion: "EGYPT", destinationRegion: "EUROPE", status: "SHIPPED" },
  { shipmentId: "S-US-001", orderId: "O-US-001", warehouseId: "W-US-001", warehouseRegion: "USA", destinationRegion: "USA", status: "SHIPPED" }
]);

print("Demo data inserted.");
