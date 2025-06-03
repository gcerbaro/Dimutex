from flask import Blueprint, request, jsonify
from config import NODE_ID
from state import increment_clock, requesting_cs, request_clock, deferred_replies, replies_received
from communication import send_reply
from logger import logger

bp = Blueprint('routes', __name__)

@bp.route("/request", methods=["POST"])
def on_request():
    data = request.get_json()
    sender_id = data["node_id"]
    sender_clock = data["clock"]

    increment_clock(sender_clock)

    logger.info(f"[{NODE_ID}] Received REQUEST from {sender_id} with clock {sender_clock}")

    defer = False
    if requesting_cs:
        if (request_clock < sender_clock) or (request_clock == sender_clock and NODE_ID < sender_id):
            defer = True

    if defer:
        deferred_replies.add(sender_id)
        logger.info(f"[{NODE_ID}] Deferred reply to {sender_id}")
    else:
        send_reply(sender_id + ":5000")

    return jsonify({"ok": True})

@bp.route("/reply", methods=["POST"])
def on_reply():
    data = request.get_json()
    sender_id = data["node_id"]

    logger.info(f"[{NODE_ID}] Received REPLY from {sender_id}")
    replies_received.add(sender_id)

    return jsonify({"ok": True})

@bp.route("/release", methods=["POST"])
def on_release():
    from communication import send_reply
    data = request.get_json()
    sender_id = data["node_id"]

    logger.info(f"[{NODE_ID}] Received RELEASE from {sender_id}")

    if sender_id in deferred_replies:
        send_reply(sender_id + ":5000")
        deferred_replies.remove(sender_id)

    return jsonify({"ok": True})
