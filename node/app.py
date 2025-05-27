from flask import Flask, request, jsonify
import threading
import time
import requests
import os

app = Flask(__name__)

# ========================
# Configuração do Node
# ========================
NODE_ID = os.environ.get("NODE_ID")
PORT = int(os.environ.get("PORT", 5000))

NODES = [
    "node1:5000",
    "node2:5000",
    "node3:5000",
    "node4:5000",
    "node5:5000",
]
OTHER_NODES = [n for n in NODES if not n.startswith(NODE_ID)]

# ========================
# Estado
# ========================
clock = 0
request_clock = None
requesting_cs = False
replies_received = set()
deferred_replies = set()

lock = threading.Lock()

# ========================
# Funções auxiliares
# ========================
def increment_clock(received_clock=None):
    global clock
    with lock:
        if received_clock is not None:
            clock = max(clock, received_clock) + 1
        else:
            clock += 1
        return clock

def send_request_to_all():
    increment_clock()
    global request_clock
    request_clock = clock
    print(f"[{NODE_ID}] Requesting critical section at clock {clock}")
    for node in OTHER_NODES:
        try:
            requests.post(
                f"http://{node}/request",
                json={"node_id": NODE_ID, "clock": request_clock},
                timeout=2,
            )
        except Exception as e:
            print(f"[{NODE_ID}] Failed to send request to {node}: {e}")

def send_reply(node):
    try:
        requests.post(
            f"http://{node}/reply",
            json={"node_id": NODE_ID},
            timeout=2,
        )
        print(f"[{NODE_ID}] Sent reply to {node}")
    except Exception as e:
        print(f"[{NODE_ID}] Failed to send reply to {node}: {e}")

# ========================
# Rotas HTTP
# ========================
@app.route("/request", methods=["POST"])
def on_request():
    global requesting_cs
    data = request.get_json()
    sender_id = data["node_id"]
    sender_clock = data["clock"]

    increment_clock(sender_clock)

    print(f"[{NODE_ID}] Received REQUEST from {sender_id} with clock {sender_clock}")

    defer = False
    if requesting_cs:
        if (request_clock < sender_clock) or (request_clock == sender_clock and NODE_ID < sender_id):
            defer = True

    if defer:
        deferred_replies.add(sender_id)
        print(f"[{NODE_ID}] Deferred reply to {sender_id}")
    else:
        send_reply(sender_id + ":5000")

    return jsonify({"ok": True})

@app.route("/reply", methods=["POST"])
def on_reply():
    data = request.get_json()
    sender_id = data["node_id"]

    print(f"[{NODE_ID}] Received REPLY from {sender_id}")
    replies_received.add(sender_id)

    return jsonify({"ok": True})

@app.route("/release", methods=["POST"])
def on_release():
    data = request.get_json()
    sender_id = data["node_id"]

    print(f"[{NODE_ID}] Received RELEASE from {sender_id}")

    if sender_id in deferred_replies:
        send_reply(sender_id + ":5000")
        deferred_replies.remove(sender_id)

    return jsonify({"ok": True})

# ========================
# Seção crítica simulada
# ========================
def critical_section_loop():
    while True:
        time.sleep(10 + int(NODE_ID[-1]))  # Intervalo variável por node

        print(f"[{NODE_ID}] Trying to enter critical section...")
        global requesting_cs
        requesting_cs = True
        replies_received.clear()

        send_request_to_all()

        while len(replies_received) < len(OTHER_NODES):
            time.sleep(0.5)

        print(f"[{NODE_ID}] >>> ENTERING CRITICAL SECTION <<<")
        time.sleep(5)  # Simula operação na seção crítica
        print(f"[{NODE_ID}] <<< LEAVING CRITICAL SECTION >>>")

        requesting_cs = False
        request_clock = None

        for node in OTHER_NODES:
            try:
                requests.post(
                    f"http://{node}/release",
                    json={"node_id": NODE_ID},
                    timeout=2,
                )
            except Exception as e:
                print(f"[{NODE_ID}] Failed to send release to {node}: {e}")

if __name__ == "__main__":
    threading.Thread(target=critical_section_loop, daemon=True).start()
    app.run(host="0.0.0.0", port=PORT)
