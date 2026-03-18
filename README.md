# Drone Order Delivery

Polls Supabase for new orders and triggers MAVProxy drone missions to fly to order coordinates (takeoff → guided goto → RTL).

---

## Quick start (for instructors / evaluators)

This repo is set up so you can download it and follow through in order:

1. **Download or clone** the project and open a terminal in `Drone-Final_code`.
2. **Create a venv and install deps:**  
   `python -m venv venv` → activate it → `pip install -r requirements.txt`
3. **Copy** `.env.example` to `.env` and fill in your Supabase URL and anon key (and `MASTER` if you will run drone missions).
4. **Create the database:** In [Supabase](https://supabase.com) → SQL Editor, run the contents of `schema/orders.sql`.
5. **Test without hardware:**  
   `python get_orders.py` — polls orders every 5 seconds and prints new ones’ coordinates.
6. **Test with SITL/drone (optional):**  
   Start MAVProxy or SITL, then run `python fetchandfly.py` to run a full mission for each new order.

All config lives in `config.py`; DB access in `db.py`; flight logic in `mission.py`. Entry points are `get_orders.py` (orders only) and `fetchandfly.py` (orders + missions).

---

## Requirements

- Python 3.8+
- [MAVProxy](https://ardupilot.org/mavproxy/) (for drone control)
- Supabase project with an `orders` table

## Setup

1. **Clone and enter the repo**
   ```bash
   cd Drone-Final_code
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/macOS
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and set:
   - `SUPABASE_URL` – your Supabase project URL
   - `SUPABASE_ANON_KEY` – your Supabase anon/public key
   - `MASTER` – MAVProxy connection (see below)

## MAVProxy connection (`MASTER`)

- **Hardware (e.g. Raspberry Pi):** `MASTER=/dev/serial0,57600`
- **SITL / Mission Planner:** `MASTER=tcp:127.0.0.1:5762` (or `5763` if 5762 fails)
- **Remote Pi over SSH/network:** `MASTER=tcp:192.168.x.x:5760`

## Supabase: `orders` table

Run the schema in the Supabase SQL editor. Use the file in this repo:

- **`schema/orders.sql`** – creates `orders` table, RLS, and policies (anon insert + anon read for polling).

## Usage

- **Poll orders and print coordinates only (no drone):**
  ```bash
  python get_orders.py
  ```

- **Poll orders and run drone missions for new orders:**
  ```bash
  python fetchandfly.py
  ```

Ensure MAVProxy can reach your autopilot (SITL or real) before running `fetchandfly.py`.

## Project structure

| Path | Purpose |
|------|--------|
| `config.py` | Loads `.env` and exposes `SUPABASE_*`, `MASTER`, and flight constants |
| `db.py` | Supabase client and `get_orders()` |
| `mission.py` | MAVProxy mission: takeoff → guided goto → RTL |
| `get_orders.py` | CLI: poll orders and print coordinates |
| `fetchandfly.py` | CLI: poll orders and run a drone mission per new order |
| `schema/orders.sql` | Supabase DDL for `orders` table and RLS policies |

## License

Use as needed for your project.
