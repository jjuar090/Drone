"""
Poll for new orders every 5 seconds and print their geo coordinates.
Uses Supabase via db module. Set SUPABASE_URL and SUPABASE_ANON_KEY in .env or environment.
"""
import time

from db import get_orders


def print_order(order):
    """Print a single order's geo coordinates."""
    lat = order.get("latitude")
    lon = order.get("longitude")
    accuracy = order.get("accuracy", 0)
    order_id = order.get("id", "N/A")
    created = order.get("created_at", "N/A")
    print(f"Order {order_id}")
    print(f"  Created: {created}")
    print(f"  Coordinates: ({lat}, {lon})")
    print(f"  Latitude:  {lat}")
    print(f"  Longitude: {lon}")
    print(f"  Accuracy:  {accuracy}m")
    print()


def main():
    seen_ids = set()

    try:
        for order in get_orders():
            seen_ids.add(order.get("id"))
    except Exception as e:
        print(f"Initial fetch failed: {e}")

    print("Watching for new orders (checking every 5 seconds)...\n")

    while True:
        time.sleep(5)
        try:
            for order in get_orders():
                order_id = order.get("id")
                if order_id not in seen_ids:
                    seen_ids.add(order_id)
                    print_order(order)
        except Exception as e:
            print(f"Error in loop: {e}")


if __name__ == "__main__":
    main()
