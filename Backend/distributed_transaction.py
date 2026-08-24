from database import db, client
from datetime import datetime, timezone

def Ordering(orderId, customerId, customer_region, warehouse_region, inventory_id, amount):
    print("************************\nStarting the distributed ordering process...\n************************")

    with client.start_session() as session:
        with session.start_transaction():
            try:
                print (f"Processing payment for {customer_region} region...")
                db["payments"].insert_one({
                    "paymentId": f"PAY-{orderId}",
                    "orderId": orderId,
                    "customerId": customerId,
                    "region": customer_region,
                    "amount": amount,
                    "method": "CARD", 
                    "status": "SUCCESS",
                          
                }, session=session)

                print (f"Creating order in {customer_region} region...")
                db["orders"].insert_one({
                    "orderId": orderId,
                    "customerId": customerId,
                    "customerRegion": customer_region,
                    "status": "PENDING",    
                    "totalAmount": amount,
                    "createdAt": datetime.now(timezone.utc)
                }, session=session)

                print (f"Reserving stock from warehouse in {warehouse_region} region...")
                stock_result = db["inventory"].update_one(
                    {"inventoryId": inventory_id, "region": warehouse_region},
                    {"$inc": {"quantity": -1}}, 
                    session=session
                )
                if stock_result.modified_count == 0:
                    raise Exception("Insufficient stock available.")

                print("\nDistributed ordering process completed successfully! YAY!\n")

            except Exception as e:
                print(f"An error occurred during the distributed ordering process: {e}")
                print("Transaction aborted. Rolling back....")
                session.abort_transaction()