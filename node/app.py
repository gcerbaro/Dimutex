from flask import Flask
from routes import bp as routes_bp
from config import PORT
from critical_section import critical_section_loop
import threading

app = Flask(__name__)
app.register_blueprint(routes_bp)

if __name__ == "__main__":
    threading.Thread(target=critical_section_loop, daemon=True).start()
    app.run(host="0.0.0.0", port=PORT)
