const ecommerce = db.getSiblingDB("ecommerceDB");

function ensureCollection(name, validator) {
  const exists = ecommerce.getCollectionInfos({ name }).length > 0;
  if (!exists) {
    ecommerce.createCollection(name, {
      validator: { $jsonSchema: validator },
      validationLevel: "strict",
      validationAction: "error"
    });
    print(`Created collection: ${name}`);
  } else {
    ecommerce.runCommand({
      collMod: name,
      validator: { $jsonSchema: validator },
      validationLevel: "strict",
      validationAction: "error"
    });
    print(`Updated validator: ${name}`);
  }
}

const regionEnum = ["EGYPT", "EUROPE", "USA"];

ensureCollection("customers", {
  bsonType: "object",
  required: ["customerId", "name", "email", "region", "createdAt"],
  properties: {
    customerId: { bsonType: "string" },
    name: { bsonType: "string" },
    email: { bsonType: "string" },
    region: { enum: regionEnum },
    address: {
      bsonType: "object",
      properties: {
        country: { bsonType: "string" },
        city: { bsonType: "string" },
        street: { bsonType: "string" }
      }
    },
    createdAt: { bsonType: "date" }
  }
});

ensureCollection("products", {
  bsonType: "object",
  required: ["productId", "name", "category", "price"],
  properties: {
    productId: { bsonType: "string" },
    name: { bsonType: "string" },
    category: { bsonType: "string" },
    price: { bsonType: ["double", "int", "long", "decimal"] },
    description: { bsonType: "string" }
  }
});

ensureCollection("warehouses", {
  bsonType: "object",
  required: ["warehouseId", "name", "region"],
  properties: {
    warehouseId: { bsonType: "string" },
    name: { bsonType: "string" },
    region: { enum: regionEnum },
    location: {
      bsonType: "object",
      properties: {
        country: { bsonType: "string" },
        city: { bsonType: "string" }
      }
    }
  }
});

ensureCollection("inventory", {
  bsonType: "object",
  required: ["inventoryId", "productId", "warehouseId", "region", "quantity", "reservedQuantity", "lastUpdated"],
  properties: {
    inventoryId: { bsonType: "string" },
    productId: { bsonType: "string" },
    warehouseId: { bsonType: "string" },
    region: { enum: regionEnum },
    quantity: { bsonType: "int", minimum: 0 },
    reservedQuantity: { bsonType: "int", minimum: 0 },
    lastUpdated: { bsonType: "date" }
  }
});

ensureCollection("orders", {
  bsonType: "object",
  required: ["orderId", "customerId", "customerRegion", "status", "totalAmount", "createdAt"],
  properties: {
    orderId: { bsonType: "string" },
    customerId: { bsonType: "string" },
    customerRegion: { enum: regionEnum },
    status: { enum: ["PENDING", "CONFIRMED", "CANCELLED", "SHIPPED", "DELIVERED"] },
    totalAmount: { bsonType: ["double", "int", "long", "decimal"] },
    createdAt: { bsonType: "date" }
  }
});

ensureCollection("orderItems", {
  bsonType: "object",
  required: ["orderItemId", "orderId", "orderRegion", "productId", "quantity", "unitPrice"],
  properties: {
    orderItemId: { bsonType: "string" },
    orderId: { bsonType: "string" },
    orderRegion: { enum: regionEnum },
    productId: { bsonType: "string" },
    quantity: { bsonType: "int", minimum: 1 },
    unitPrice: { bsonType: ["double", "int", "long", "decimal"] }
  }
});

ensureCollection("payments", {
  bsonType: "object",
  required: ["paymentId", "orderId", "customerId", "region", "amount", "method", "status"],
  properties: {
    paymentId: { bsonType: "string" },
    orderId: { bsonType: "string" },
    customerId: { bsonType: "string" },
    region: { enum: regionEnum },
    amount: { bsonType: ["double", "int", "long", "decimal"] },
    method: { enum: ["CARD", "CASH", "WALLET", "BANK_TRANSFER"] },
    status: { enum: ["PENDING", "SUCCESS", "FAILED", "REFUNDED"] },
    paidAt: { bsonType: "date" }
  }
});

ensureCollection("shipments", {
  bsonType: "object",
  required: ["shipmentId", "orderId", "warehouseId", "warehouseRegion", "destinationRegion", "status"],
  properties: {
    shipmentId: { bsonType: "string" },
    orderId: { bsonType: "string" },
    warehouseId: { bsonType: "string" },
    warehouseRegion: { enum: regionEnum },
    destinationRegion: { enum: regionEnum },
    status: { enum: ["PENDING", "PACKED", "SHIPPED", "DELIVERED", "FAILED"] },
    trackingNumber: { bsonType: "string" }
  }
});

print("Schema created/updated.");
