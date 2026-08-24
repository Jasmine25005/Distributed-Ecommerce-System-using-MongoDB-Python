# 🛒 Distributed E-Commerce & Order Management System

This project is a comprehensive e-commerce system built on a **Distributed Database using MongoDB**. It demonstrates core distributed systems concepts including **Fragmentation**, **Concurrency Control**, **Distributed Transactions**, and **Query Optimization**.

---

## 📁 Project Structure

The project is divided into two main parts:

- **`distributed-ecommerce-project-database/`** — Contains database setup and sharding scripts.
  - `scripts/` — Scripts to build the shards and distribute data.
  - `docs/` — Fragmentation reports and schema documentation.
- **`Backend/`** — Contains the Python application logic.
  - `database.py` — Database connection setup.
  - `test_distributed.py` & `distributed_transaction.py` — Distributed transactions logic (**Task 3**).
  - `test_performance.py` — Performance and query optimization logic (**Task 4**).
  - `test_concurrency.py` — Concurrency control testing (**Task 2**).
  - Basic CRUD files (`Orders.py`, `Customers.py`, etc.).

---

## 🚀 Prerequisites

Before running any code, ensure the following are installed on your machine:

1. **Python 3.x** — To run the backend scripts.
2. **MongoDB Community Server (MSI)** — Download and install the official version.
3. **MongoDB Shell (`mongosh`)** — MongoDB command-line tool (ensure it is added to your system's Environment Variables).
4. **MongoDB Compass** — GUI to visualize data and verify transactions.
5. **`pymongo` library** — Python driver for MongoDB. Install via CMD:

```cmd
pip install pymongo
```

---

## 🛠️ Step 1: Database Setup

The following steps will build the virtual servers (shards) and seed the initial data.

### 1. Start the Servers

Open Command Prompt (CMD) or PowerShell **inside the `distributed-ecommerce-project-database` folder** and run:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\start-cluster.ps1
```

> This will open 4 blue windows representing the Egypt, Europe, and USA servers, plus the Router. **Leave them running in the background.**

### 2. Initialize Servers

In the same CMD window, run the following commands sequentially to initialize the replica sets:

```bash
mongosh --port 27019  --file .\scripts\01-init-config.js
mongosh --port 27101  --file .\scripts\02-init-egypt.js
mongosh --port 27102  --file .\scripts\02-init-europe.js
mongosh --port 27103  --file .\scripts\02-init-usa.js
```

### 3. Add Shards & Fragment Data

Run the following commands to create the schema, apply fragmentation, and seed the data:

```bash
mongosh --port 27017 --file .\scripts\03-add-shards.js
mongosh --port 27017 --file .\scripts\04-create-schema.js
mongosh --port 27017 --file .\scripts\05-configure-fragmentation.js
mongosh --port 27017 --file .\scripts\06-seed-data.js
```

---

## 💻 Step 2: Running the System

To test the backend operations, open a new CMD **inside the `Backend` folder**.

### Test Distributed Transactions (Role 3)

This script simulates a complex cross-shard purchase (e.g., charging payment and creating an order in **Europe** while deducting stock from **Egypt** simultaneously).

```bash
python test_distributed.py
```

### Test Query Optimization (Role 4)

This script measures query execution times before and after index creation to demonstrate performance improvements.

```bash
python test_performance.py
```

### Test Concurrency Control (Role 2)

This script stresses the system with simultaneous operations to verify locking and conflict handling.

```bash
python test_concurrency.py
```

---

## ⚠️ Troubleshooting & Fixes

During development, we encountered and resolved several technical challenges. Here is how to fix them if they occur:

| Error / Issue | Cause | Solution |
| --- | --- | --- |
| `Can't use localhost as a shard` (Script 03) | Hostname conflicts with `localhost` across shards. | Open `03-add-shards.js` and change dummy names (e.g. `shard-egypt:27018`) to `rsEgypt/localhost:27101`. |
| `ModuleNotFoundError: No module named 'backend'` | Incorrect Python relative import path. | Change the import statement from `from backend.database import db` to `from database import db`. |
| `Document failed validation... value not found in enum` | Inserting data that violates schema validation rules (e.g. passing `CREDIT_CARD`). | Strictly use allowed Enum values defined in the schema (e.g. use `CARD` or `PENDING`). |
| `missingProperties: ['createdAt']` in Orders | The database strictly requires a creation timestamp. | Import `datetime` and add `"createdAt": datetime.now(timezone.utc)` to the payload. |
| `tempCodeRunnerFile.py` causes crashes | The VS Code "Code Runner" extension creates temp files that break the project's working directory. | Delete the temp file and always run scripts via the Terminal using: `python filename.py`. |
| `Index already exists with a different name` (Performance Test) | Attempting to create an index that was already auto-generated during seeding. | Wrap the index creation code in a `try...except` block to gracefully skip existing indexes. |

---

## 🛑 Safe Shutdown

When you are done, **do not close the blue server windows forcibly** to avoid data corruption. Instead, open CMD in the `distributed-ecommerce-project-database` folder and run:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\stop-cluster.ps1
```
