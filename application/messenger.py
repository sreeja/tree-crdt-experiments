import time


latency_config = {
    "paris": {
        "bangalore": 2,
        "newyork": 1
    },
    "bangalore": {
        "paris": 2,
        "newyork": 3,
    },
    "newyork": {
        "paris": 1,
        "bangalore": 3,
    }
}


def get_config():
    whoami = os.environ.get("WHOAMI")
    return latency_config.get(whoami, {})

def write(message):
    to = message.get("to", "")
    payload = message.get("payload", "")
    queue_name = f"{whoami}-{to}"
    time.sleep(config.get(to, 0))
    # write to the queue
