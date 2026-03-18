"""
Supabase orders access. Uses config for SUPABASE_URL and SUPABASE_ANON_KEY.
"""
from supabase import create_client

from config import SUPABASE_ANON_KEY, SUPABASE_URL


def get_orders(limit: int = 100):
    """Fetch the most recent orders from the database."""
    if not SUPABASE_URL or not SUPABASE_ANON_KEY:
        raise ValueError(
            "Set SUPABASE_URL and SUPABASE_ANON_KEY in .env or environment"
        )
    client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
    response = (
        client.table("orders")
        .select("id, created_at, latitude, longitude, accuracy, total")
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )
    return response.data
