"""
MAVProxy drone mission: takeoff -> guided goto (lat, lon) -> RTL.
Uses config for MASTER and flight timing/altitude.
"""
import subprocess
import time

from config import (
    ARM_WAIT_SEC,
    ARRIVE_WAIT_SEC,
    CLIMB_WAIT_SEC,
    HOLD_AT_TARGET_SEC,
    MASTER,
    RTL_WAIT_SEC,
    TAKEOFF_M,
    TRAVEL_ALT_M,
)


def run_drone_mission(lat: float, lon: float) -> None:
    """Run full mission: arm, takeoff, fly to (lat, lon), then RTL and exit MAVProxy."""
    p = subprocess.Popen(
        ["mavproxy.py", f"--master={MASTER}"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )

    def send(cmd: str, delay: float = 0.25) -> None:
        p.stdin.write(cmd + "\n")
        p.stdin.flush()
        time.sleep(delay)

    time.sleep(5)

    send("mode GUIDED")
    send("arm throttle")
    time.sleep(ARM_WAIT_SEC)
    send(f"takeoff {TAKEOFF_M}")
    time.sleep(CLIMB_WAIT_SEC)

    send(f"guided {lat:.7f} {lon:.7f} {TRAVEL_ALT_M:.1f}")
    time.sleep(ARRIVE_WAIT_SEC)
    time.sleep(HOLD_AT_TARGET_SEC)

    send("mode RTL")
    time.sleep(RTL_WAIT_SEC)

    time.sleep(1)
    send("exit", delay=0.1)

    try:
        out, _ = p.communicate(timeout=35)
    except subprocess.TimeoutExpired:
        p.kill()
        out, _ = p.communicate()

    print(out)
