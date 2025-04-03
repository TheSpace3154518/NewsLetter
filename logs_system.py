from datetime import datetime
import uuid

# ? ============= Log Format ==================
# ? date | uuid | url | error_type | error_generated
# ? ===========================================


def generate_logs(*args):
    name = f"Log-{datetime.now().strftime("%Y-%m-%d")}.log"
    complete_log = ["> ", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), uuid.uuid4()]
    complete_log.extend(args)
    complete_log = [str(log) for log in complete_log]
    with open(f"./Logs/{name}", "a") as f:
        f.write(" | ".join(complete_log) + "\n")