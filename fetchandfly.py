"""
Poll Supabase for new orders and run MAVProxy missions to each order's coordinates.
Requires SUPABASE_URL, SUPABASE_ANON_KEY (and optionally MASTER) in .env or environment.
"""
import time

from db import get_orders
from mission import run_drone_mission


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
                    lat = float(order.get("latitude"))
                    lon = float(order.get("longitude"))
                    print(f"New Order Detected: {order_id}. Launching Drone to {lat}, {lon}")
                    run_drone_mission(lat, lon)
        except Exception as e:
            print(f"Error in loop: {e}")


if __name__ == "__main__":
    main()
