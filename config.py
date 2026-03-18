"""
Load environment and expose config used by get_orders, fetchandfly, and mission.
Set SUPABASE_URL, SUPABASE_ANON_KEY (and optionally MASTER) in .env or environment.
"""
import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

# MAVProxy connection (for fetchandfly / mission)
MASTER = os.getenv("MASTER", "tcp:127.0.0.1:5762")

# Flight parameters
TAKEOFF_M = 3.0
TRAVEL_ALT_M = 3.0
ARM_WAIT_SEC = 2.0
CLIMB_WAIT_SEC = 6.0
ARRIVE_WAIT_SEC = 12.0
HOLD_AT_TARGET_SEC = 2.0
RTL_WAIT_SEC = 2.0
