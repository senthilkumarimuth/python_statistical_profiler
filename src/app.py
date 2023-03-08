from flask import Flask, g, make_response, request
from pyinstrument import Profiler
import time
app = Flask(__name__)


def sleeper():
    "sleeping for 10 seconds"
    time.sleep(10)
    return

@app.before_request
def before_request():
    if "profile" in request.args:
        g.profiler = Profiler()
        g.profiler.start()

@app.route("/")
def greeting():
    sleeper()
    return 'hello world'

@app.after_request
def after_request(response):
    if not hasattr(g, "profiler"):
        return response
    g.profiler.stop()
    output_html = g.profiler.output_html()
    return make_response(output_html)

app.run(debug=True)