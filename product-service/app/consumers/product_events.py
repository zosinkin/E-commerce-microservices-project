import json 


async def handle_product_created(payload: dict) -> None:
    print("=== PRODUCT CREATED EVENT RECEIVED ===")
    print(payload)