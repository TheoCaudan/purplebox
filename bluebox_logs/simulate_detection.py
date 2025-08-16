import time, os, requests, json

API = os.environ.get("PURPLEBOX_API", "http://purplebox-web:5000")

# Wait for orchestrator to run attacks
time.sleep(12)

now = int(time.time())
events = [
    (now, "attack1", "dmz-gateway", "portscan_detected", "Simulated IDS: Port scan to HMI via DMZ"),
    (now+2, "attack2", "dmz-gateway", "modbus_write_detected", "Simulated IDS: Modbus activity to PLC via DMZ")
]

with open("/bluebox_logs/detection.log","w") as f:
    for ts, aid, tgt, evt, details in events:
        f.write(f"{ts},{aid},{tgt},{evt}\n")
        try:
            r = requests.post(f"{API}/api/event", json={
                "source": "bluebox",
                "event_type": "detection",
                "attack_id": aid,
                "target": tgt,
                "timestamp": ts,
                "details": details
            }, timeout=5)
            print("[bluebox-sim] posted", aid, r.status_code)
        except Exception as e:
            print("[bluebox-sim] post failed:", e)
