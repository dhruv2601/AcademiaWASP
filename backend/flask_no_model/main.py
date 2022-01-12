from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException
import os
import json

app = Flask(__name__)


class InvalidAPIUsage(Exception):
    """
    Custom Exception class for invalid api usage from:
    https://flask.palletsprojects.com/en/2.0.x/errorhandling/#returning-api-errors-as-json
    """
    status_code = 400

    def __init__(self, message, status_code=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        return {
            "code": self.status_code,
            "name": "InvalidAPIUsage",
            "description":  self.message
        }

@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(e):
    """
    Error handler for above class
    https://flask.palletsprojects.com/en/2.0.x/errorhandling/#returning-api-errors-as-json
    """
    return jsonify(e.to_dict())

@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response


@app.before_first_request
def before_first_request():
    print("before first print - update")


@app.route("/ping")
def ping():
    """Health and reachability checks"""
    return "pong"


@app.route("/style")
def style():
    """Transfering style of given sentence"""
    sentence = request.args.get('sentence')
    n_output = request.args.get('n_output')

    if not sentence:
        raise InvalidAPIUsage("No sentence provided! ?sentence=")
    
    if not n_output:
        raise InvalidAPIUsage("No number of output sentences provided! ?n_output=")
    
    try:
        n_output = int(n_output)
    except ValueError:
        raise InvalidAPIUsage("n_output has to be an integer")

    output = (infer_scientific(42, n_output, sentence))

    obj = {}
    obj["output"] = output
    return jsonify(obj)


def infer_scientific(model, n_sentences, sentence):
    """Actual scientific inference"""
    return [sentence]*n_sentences



if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))