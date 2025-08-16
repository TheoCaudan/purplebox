import os, time, subprocess, requests

API = os.environ.get("PURPLEBOX_API", "http://purplebox-web:5000")
REDBOX_CONTAINER = os.environ.get("REDBOX_CONTAINER", "redbox")
ATTACKS = {
    "1": "attack1.sh",
    "2": "attack2_modbus.sh"
}

def post_event(event_type, attack_id, details):
    payload = {
        "source": "redbox",
        "event_type": event_type,
        "attack_id": attack_id,
        "target": "dmz-gateway",
        "timestamp": time.time(),
        "details": details
    }
    try:
        r = requests.post(f"{API}/api/event", json=payload, timeout=5)
        print(f"[attacks] POST /api/event ({attack_id}, {event_type}) =>", r.status_code)
    except Exception as e:
        print("[attacks] failed to post event:", e)

def run_attack(attack_key):
    if attack_key not in ATTACKS:
        print(f"[attacks] Unknown attack: {attack_key}")
        return False

    script_name = ATTACKS[attack_key]
    print(f"[attacks] Launching {script_name} in {REDBOX_CONTAINER}")

    # annonce le début
    post_event("attack_start", script_name, f"Launching {script_name}")

    # exécute le script dans Redbox
    cmd = ["docker","exec",REDBOX_CONTAINER,"bash",f"/attack_scripts/{script_name}"]
    result = subprocess.run(cmd, capture_output=True, text=True)

    print("[attacks] stdout:", result.stdout)
    if result.stderr:
        print("[attacks] stderr:", result.stderr)

    # annonce la fin
    post_event("attack_end", script_name, f"Completed {script_name}")
    return result.returncode == 0

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python orchestrate_attacks.py <attack_number>")
        print("Available:", ", ".join(ATTACKS.keys()))
        sys.exit(1)

    attack_number = sys.argv[1]
    success = run_attack(attack_number)

    if success:
        print(f"[attacks] Attack {attack_number} completed successfully.")
    else:
        print(f"[attacks] Attack {attack_number} failed.")
