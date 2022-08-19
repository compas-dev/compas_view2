from flask import Flask
from flask import request
from threading import Thread
import sys
from io import StringIO
import contextlib

@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old

def start_server(app):
    kwargs = {'host': '127.0.0.1', 'port': 5000, 'threaded': True, 'use_reloader': False, 'debug': False}
    flask_app = Flask(__name__)
    @flask_app.route("/run", methods = ['POST'])
    def run():
        print(app)
        script = request.json["script"]
        print(">>>", script)
        with stdoutIO() as s:
            try:
                exec(script)
            except Exception as e:
                return str(e)
        return s.getvalue()
    flaskThread = Thread(target=flask_app.run, daemon=True, kwargs=kwargs).start()
