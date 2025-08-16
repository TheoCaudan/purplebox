import os, time, subprocess, requests

API = os.environ.get("PURPLEBOX_API", "http://purplebox-web:5000")
BLUEBOX_COMPOSE = os.environ.get("BLUEBOX_COMPOSE", "../bluebox/docker-compose.yml")
REDBOX_COMPOSE = os.environ.get("REDBOX_COMPOSE", "../redbox/docker-compose.yml")

def post_event(source, event_type, target, details):
    payload = {
        "source": source,
        "event_type": event_type,
        "attack_id": "",   # pas une attaque ici
        "target": target,
        "timestamp": time.time(),
        "details": details
    }
    try:
        r = requests.post(f"{API}/api/event", json=payload, timeout=5)
        print(f"[orchestrator] POST /api/event ({target}) =>", r.status_code)
    except Exception as e:
        print("[orchestrator] failed to post event:", e)

def start_stack(name, compose_file):
    print(f"[orchestrator] Starting {name}...")
    result = subprocess.run(
        ["docker", "compose", "-f", compose_file, "up", "-d"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"[orchestrator] Failed to start {name}:", result.stderr)
        post_event("orchestrator", "stack_error", name, f"Failed to start {name}: {result.stderr}")
        return False
    print(f"[orchestrator] {name} started.")
    post_event("orchestrator", "stack_start", name, f"{name} stack started")
    return True

def wait_for_service(name, url, timeout=120):
    """Attendre qu’un service HTTP réponde"""
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            r = requests.get(url, timeout=3)
            if r.status_code == 200:
                print(f"[orchestrator] {name} is up")
                post_event("orchestrator", "stack_ready", name, f"{name} is ready at {url}")
                return True
        except Exception:
            pass
        time.sleep(5)
    print(f"[orchestrator] {name} did not start in time")
    post_event("orchestrator", "stack_timeout", name, f"{name} did not start in time")
    return False

if __name__ == "__main__":
    time.sleep(5)

    # Démarrage Bluebox
    if start_stack("bluebox", BLUEBOX_COMPOSE):
        wait_for_service("elasticsearch", "http://elasticsearch:9200")
        wait_for_service("kibana", "http://kibana:5601")

    # Démarrage Redbox
    if start_stack("redbox", REDBOX_COMPOSE):
        # Ici pas de HTTP, juste un healthcheck container
        post_event("orchestrator", "stack_ready", "redbox", "Redbox container running")

    # Vérification API Purplebox
    try:
        health = requests.get(f"{API}/api/health", timeout=3).json()
        print("[orchestrator] Purplebox Web Health:", health)
        post_event("orchestrator", "healthcheck", "purplebox-web", f"Health OK at {health['time']}")
    except Exception as e:
        print("[orchestrator] Purplebox Web health check failed:", e)
        post_event("orchestrator", "healthcheck_failed", "purplebox-web", str(e))

    print("[orchestrator] Bootstrap done.")
