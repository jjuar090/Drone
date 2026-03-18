import subprocess
import time

MASTER = "tcp:127.0.0.1:5762" 

TAKEOFF_M = 3.0
TRAVEL_ALT_M = 3.0          # altitude to use for guided goto
ARM_WAIT_SEC = 2.0          # arm for a moment before takeoff
CLIMB_WAIT_SEC = 6.0        # time to reach takeoff altitude (tune)
ARRIVE_WAIT_SEC = 12.0      # time to travel to target (tune)
HOLD_AT_TARGET_SEC = 2.0    # brief pause
RTL_WAIT_SEC = 2.0          # let RTL engage


def main():
    # Get coordinates from user
    lat = float(input("Target latitude (e.g., 33.9769826): ").strip())
    lon = float(input("Target longitude (e.g., -117.3284603): ").strip())

    # Launch MAVProxy in the background
    p = subprocess.Popen(
        ["mavproxy.py", f"--master={MASTER}"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )

    def send(cmd: str, delay: float = 0.25):
        p.stdin.write(cmd + "\n")
        p.stdin.flush()
        time.sleep(delay)

    # Let MAVProxy connect / get heartbeat
    time.sleep(5)

    # 1) Arm + takeoff
    send("mode GUIDED")
    send("arm throttle")
    time.sleep(ARM_WAIT_SEC)
    send(f"takeoff {TAKEOFF_M}")

    time.sleep(CLIMB_WAIT_SEC)

    # 2) Fly to coordinates
    send(f"guided {lat:.7f} {lon:.7f} {TRAVEL_ALT_M:.1f}")

    time.sleep(ARRIVE_WAIT_SEC)
    time.sleep(HOLD_AT_TARGET_SEC)

    # 3) Return to original/home position (RTL)
    send("mode RTL")
    time.sleep(RTL_WAIT_SEC)

    # Exit
    time.sleep(1)
    send("exit", delay=0.1)

    try:
        out, _ = p.communicate(timeout=35)
    except subprocess.TimeoutExpired:
        p.kill()
        out, _ = p.communicate()

    print(out)

if __name__ == "__main__":
    main()