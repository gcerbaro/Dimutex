from flask import Blueprint, request, jsonify
from state import state
from config import NODE_ID
from communication import send_reply, colors
from logger import logger

bp = Blueprint('routes', __name__)
def node_number(id):
    return int(id.replace("node", ""))


@bp.route("/request", methods=["POST"])
def on_request():
    data = request.get_json()
    sender_id = data["node_id"]
    sender_clock = data["clock"]

    state.increment_clock(sender_clock)

    logger.info(f"{colors.CYAN}[{NODE_ID}] Received REQUEST from {sender_id} with clock {sender_clock}")

    defer = False
    requesting, my_clock = state.get_request_state()
    if requesting:
        if (sender_clock < state.request_clock) or (sender_clock == state.request_clock and sender_id < NODE_ID):
            defer = True
    else:
        send_reply(sender_id + ":5000")



    if defer:
        state.deferred_replies.add(sender_id)
        logger.info(f"{colors.MAGENTA}[{NODE_ID}] Deferred reply to {sender_id}")
    else:
        send_reply(sender_id + ":5000")

    return jsonify({"ok": True})


@bp.route("/reply", methods=["POST"])
def on_reply():
    data = request.get_json()
    sender_id = data["node_id"]

    state.increment_clock()

    logger.info(f"{colors.CYAN}[{NODE_ID}] Received REPLY from {sender_id}")
    state.replies_received.add(sender_id)

    return jsonify({"ok": True})


@bp.route("/release", methods=["POST"])
def on_release():
    data = request.get_json()
    sender_id = data["node_id"]

    logger.info(f"{colors.GREEN}[{NODE_ID}] Received RELEASE from {sender_id}")

    if sender_id in state.deferred_replies:
        send_reply(sender_id + ":5000")
        state.deferred_replies.remove(sender_id)

    return jsonify({"ok": True})
