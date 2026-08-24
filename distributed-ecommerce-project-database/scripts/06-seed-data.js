const e = db.getSiblingDB("ecommerceDB");

// Make this script safely repeatable for the demo.
for (const c of ["customers", "products", "warehouses", "inventory", "orders", "orderItems", "payments", "shipments"]) {
  e[c].deleteMany({});
}

e.customers.insertMany([
  {
    customerId: "C-EG-001", name: "Ahmed Hassan", email: "ahmed@example.com",
    region: "EGYPT",
    address: { country: "Egypt", city: "Cairo", street: "Nasr City" },
    createdAt: new Date()
  },
  {
    customerId: "C-EU-001", name: "Anna Schmidt", email: "anna@example.com",
    region: "EUROPE",
    address: { country: "Germany", city: "Berlin", street: "Alexanderplatz" },
    createdAt: new Date()
  },
  {
    customerId: "C-US-001", name: "John Smith", email: "john@example.com",
    region: "USA",
    address: { country: "USA", city: "New York", street: "5th Avenue" },
    createdAt: new Date()
  }
]);

e.products.insertMany([
  { productId: "P001", name: "Laptop", category: "Electronics", price: 1200.0, description: "Demo laptop" },
  { productId: "P002", name: "Headphones", category: "Electronics", price: 150.0, description: "Wireless headphones" },
  { productId: "P003", name: "Backpack", category: "Accessories", price: 70.0, description: "Travel backpack" },
  { productId: "P004", name: "Keyboard", category: "Electronics", price: 90.0, description: "Mechanical keyboard" },
  { productId: "P005", name: "Mouse", category: "Electronics", price: 50.0, description: "Wireless mouse" },
  { productId: "P006", name: "Monitor", category: "Electronics", price: 300.0, description: "27-inch monitor" }
]);

e.warehouses.insertMany([
  { warehouseId: "W-EG-001", name: "Cairo Warehouse", region: "EGYPT", location: { country: "Egypt", city: "Cairo" } },
  { warehouseId: "W-EU-001", name: "Berlin Warehouse", region: "EUROPE", location: { country: "Germany", city: "Berlin" } },
  { warehouseId: "W-US-001", name: "New York Warehouse", region: "USA", location: { country: "USA", city: "New York" } }
]);

e.inventory.insertMany([
  { inventoryId: "I-EG-001", productId: "P001", warehouseId: "W-EG-001", region: "EGYPT", quantity: NumberInt(2), reservedQuantity: NumberInt(0), lastUpdated: new Date() },
  { inventoryId: "I-EG-002", productId: "P002", warehouseId: "W-EG-001", region: "EGYPT", quantity: NumberInt(15), reservedQuantity: NumberInt(0), lastUpdated: new Date() },
  { inventoryId: "I-EU-001", productId: "P003", warehouseId: "W-EU-001", region: "EUROPE", quantity: NumberInt(20), reservedQuantity: NumberInt(0), lastUpdated: new Date() },
  { inventoryId: "I-EU-002", productId: "P004", warehouseId: "W-EU-001", region: "EUROPE", quantity: NumberInt(10), reservedQuantity: NumberInt(0), lastUpdated: new Date() },
  { inventoryId: "I-US-001", productId: "P005", warehouseId: "W-US-001", region: "USA", quantity: NumberInt(25), reservedQuantity: NumberInt(0), lastUpdated: new Date() },
  { inventoryId: "I-US-002", productId: "P006", warehouseId: "W-US-001", region: "USA", quantity: NumberInt(12), reservedQuantity: NumberInt(0), lastUpdated: new Date() }
]);

// Cross-region example intentionally supports Team Member 3:
// European customer + Egyptian inventory/warehouse.
e.orders.insertOne({
  orderId: "O-EU-001",
  customerId: "C-EU-001",
  customerRegion: "EUROPE",
  status: "CONFIRMED",
  totalAmount: 1200.0,
  createdAt: new Date()
});

e.orderItems.insertOne({
  orderItemId: "OI-EU-001",
  orderId: "O-EU-001",
  orderRegion: "EUROPE",
  productId: "P001",
  quantity: NumberInt(1),
  unitPrice: 1200.0
});

e.payments.insertOne({
  paymentId: "PAY-EU-001",
  orderId: "O-EU-001",
  customerId: "C-EU-001",
  region: "EUROPE",
  amount: 1200.0,
  method: "CARD",
  status: "SUCCESS",
  paidAt: new Date()
});

e.shipments.insertOne({
  shipmentId: "S-EG-001",
  orderId: "O-EU-001",
  warehouseId: "W-EG-001",
  warehouseRegion: "EGYPT",
  destinationRegion: "EUROPE",
  status: "PACKED",
  trackingNumber: "TRK-DEMO-001"
});

print("Seed data inserted.");
