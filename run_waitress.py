import os
from waitress import serve
import app.app as app

port = int(os.environ.get("PORT", 5000))
serve(app, host="0.0.0.0", port=port)