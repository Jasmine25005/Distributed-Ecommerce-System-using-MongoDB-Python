from concurrent.futures import ThreadPoolExecutor, as_completed

from inventory import (
    add_inventory,
    get_available_quantity,
    purchase_stock,
)


INVENTORY_ID = "I-CONCURRENCY-001"
PRODUCT_ID = "P-CONCURRENCY-001"
WAREHOUSE_ID = "W-TEST-001"
REGION = "EGYPT"


def run_purchase(customer_name):
    result = purchase_stock(
        INVENTORY_ID,
        REGION,
        1
    )

    return {
        "customer": customer_name,
        **result
    }


def main():
    print("=" * 60)
    print("CONCURRENCY CONTROL TEST")
    print("=" * 60)

    # Make sure the test inventory does not already exist
    from database import db

    inventory = db["inventory"]

    inventory.delete_one({
        "inventoryId": INVENTORY_ID,
        "region": REGION
    })

    # Create inventory with only ONE item available
    add_inventory(
        INVENTORY_ID,
        PRODUCT_ID,
        WAREHOUSE_ID,
        REGION,
        quantity=1
    )

    print("\nInitial stock:")
    print(get_available_quantity(PRODUCT_ID, WAREHOUSE_ID))

    print("\nTwo customers are trying to buy 1 item simultaneously...\n")

    results = []

    # Simulate two customers purchasing at the same time
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = [
            executor.submit(run_purchase, "Customer 1"),
            executor.submit(run_purchase, "Customer 2"),
        ]

        for future in as_completed(futures):
            results.append(future.result())

    # Display results
    for result in results:
        print(
            f"{result['customer']}: "
            f"{'SUCCESS' if result['success'] else 'FAILED'}"
        )
        print(f"  Message: {result['message']}")

        if result["success"]:
            print(
                f"  Remaining quantity: "
                f"{result['remainingQuantity']}"
            )

    final_stock = get_available_quantity(
        PRODUCT_ID,
        WAREHOUSE_ID
    )

    print("\nFinal stock:")
    print(final_stock)

    # Verify consistency
    successful_purchases = sum(
        1 for result in results
        if result["success"]
    )

    failed_purchases = sum(
        1 for result in results
        if not result["success"]
    )

    print("\n" + "=" * 60)
    print("TEST RESULT")
    print("=" * 60)

    print(f"Successful purchases: {successful_purchases}")
    print(f"Failed purchases: {failed_purchases}")
    print(f"Final stock: {final_stock}")

    if (
        successful_purchases == 1
        and failed_purchases == 1
        and final_stock == 0
    ):
        print("\nPASS: Concurrency control works correctly.")
        print("No overselling occurred.")
    else:
        print("\nFAIL: Unexpected concurrency result.")


if __name__ == "__main__":
    main()