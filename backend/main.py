from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException
from transformers import T5ForConditionalGeneration,T5Tokenizer
import torch
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
    dirname = os.path.dirname(__file__)
    # MODEL_PATH = Path("/Users/dhruvrathi/narnia/masters/RPG1/conf/website/flask/model/")
    MODEL_PATH = os.path.join(dirname, 't5_model/')
    print(f"model path: {MODEL_PATH}")

    print("py: model")
    global model
    model = T5ForConditionalGeneration.from_pretrained(MODEL_PATH)

    print("py: tokenizer")
    global tokenizer
    tokenizer = T5Tokenizer.from_pretrained('t5-large')

    print("py: device")
    global device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    print("py: model.to")
    model = model.to(device)


@app.route("/ping")
def ping():
    """Health and reachability checks"""
    return "pong"


@app.route("/style")
def style():
    """Transfering style of given sentence"""
    sentence = request.args.get('sentence')
    n_output = request.args.get('n_output')
    max_len = request.args.get('max_len')

    if not sentence:
        raise InvalidAPIUsage("No sentence provided! ?sentence=")
    
    if not n_output:
        raise InvalidAPIUsage("No number of output sentences provided! ?n_output=")

    try:
        n_output = int(n_output)
    except ValueError:
        raise InvalidAPIUsage("n_output has to be an integer")
    
    if max_len:
        try:
            max_len = int(max_len)
        except ValueError:
            raise InvalidAPIUsage("max_len was provided and has to be an integer")    
    

    output = (infer_scientific(model, n_output, sentence, max_len))

    obj = {}
    obj["output"] = output
    return jsonify(obj)


def infer_scientific(model, n_sentences, sentence, max_len=256):
    """Actual scientific inference"""
    text = "paraphrase: " + sentence + " </s>"

    encoding = tokenizer.encode_plus(text,pad_to_max_length=True, return_tensors="pt")
    input_ids, attention_masks = encoding["input_ids"].to(device), encoding["attention_mask"].to(device)

    beam_outputs = model.generate(
      input_ids=input_ids, attention_mask=attention_masks,
      do_sample=True,
      max_length=max_len,
      top_k=120,
      top_p=0.95,
      early_stopping=True,
      num_return_sequences=n_sentences
    )
    
    final_outputs =[]
    for beam_output in beam_outputs:
        sent = tokenizer.decode(beam_output, skip_special_tokens=True,clean_up_tokenization_spaces=True)
        if sent.lower() != sentence.lower() and sent not in final_outputs:
            final_outputs.append(sent)
    return final_outputs


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))