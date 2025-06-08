from flask import Blueprint, request, jsonify
from state import state
from config import NODE_ID
from communication import send_reply
from logger import logger, Colors

bp = Blueprint('routes', __name__)


@bp.route("/request", methods=["POST"])
def on_request():
    data = request.get_json()
    sender_id = data["node_id"]
    sender_clock = data["clock"]

    state.increment_clock(sender_clock)
    logger.info(f"{Colors.YELLOW}[{NODE_ID}] Received REQUEST from {sender_id} with clock {sender_clock}")

    defer = False
    with state.lock:
        if state.in_cs or state.requesting_cs:
            if (
                (state.request_clock < sender_clock)
                or (state.request_clock == sender_clock and NODE_ID < sender_id)
            ):
                defer = True
            else:
                defer = False
        else:
            defer = False

    if defer:
        logger.info(f"{Colors.MAGENTA}[{NODE_ID}] Deferred reply to {sender_id}")
        state.deferred_replies.add(sender_id)
    else:
        send_reply(sender_id + ":5000")

    return jsonify({"ok": True})



@bp.route("/reply", methods=["POST"])
def on_reply():
    data = request.get_json()
    sender_id = data["node_id"]

    state.increment_clock()

    logger.info(f"{Colors.CYAN}[{NODE_ID}] Received REPLY from {sender_id}")
    state.replies_received.add(sender_id)

    return jsonify({"ok": True})
