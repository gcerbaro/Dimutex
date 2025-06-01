import os

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