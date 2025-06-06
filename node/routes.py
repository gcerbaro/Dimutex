from flask import Blueprint, request, jsonify
from state import NodeState
from config import NODE_ID
from communication import send_reply
from logger import logger

bp = Blueprint('routes', __name__)
def node_number(id):
    return int(id.replace("node", ""))


@bp.route("/request", methods=["POST"])
def on_request():
    data = request.get_json()
    sender_id = data["node_id"]
    sender_clock = data["clock"]

    NodeState.increment_clock(sender_clock)

    logger.info(f"[{NODE_ID}] Received REQUEST from {sender_id} with clock {sender_clock}")

    defer = False
    requesting, my_clock = NodeState.get_request_state()
    if requesting:
        if (my_clock < sender_clock) or (my_clock == sender_clock and node_number(NODE_ID) < node_number(sender_id)):
            defer = True


    if defer:
        NodeState.deferred_replies.add(sender_id)
        logger.info(f"[{NODE_ID}] Deferred reply to {sender_id}")
    else:
        send_reply(sender_id + ":5000")

    return jsonify({"ok": True})


@bp.route("/reply", methods=["POST"])
def on_reply():
    data = request.get_json()
    sender_id = data["node_id"]

    NodeState.increment_clock()

    logger.info(f"[{NODE_ID}] Received REPLY from {sender_id}")
    NodeState.replies_received.add(sender_id)

    return jsonify({"ok": True})


@bp.route("/release", methods=["POST"])
def on_release():
    data = request.get_json()
    sender_id = data["node_id"]

    logger.info(f"[{NODE_ID}] Received RELEASE from {sender_id}")

    if sender_id in NodeState.deferred_replies:
        send_reply(sender_id + ":5000")
        NodeState.deferred_replies.remove(sender_id)

    return jsonify({"ok": True})
