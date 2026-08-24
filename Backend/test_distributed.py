from distributed_transaction import Ordering

def run_test():
    print("Starting Distributed Transaction Test...\n")
    
    Ordering(
        orderId="O-TEST-999",
        customerId="C-EU-001",
        customer_region="EUROPE",  
        warehouse_region="EGYPT",  
        inventory_id="I-EG-020",   
        amount=1500
    )

if __name__ == "__main__":
    run_test()