from flask import Flask, request, jsonify
from flask_cors import CORS
import torch
import numpy as np
from catboost import CatBoostClassifier
from utils.model_bert import Model
from utils.data import tokenize_function, TextDataset, collate_fn, get_embeddings

app = Flask(__name__)
CORS(app)

# Load the model
model_bert = Model()
model_bert.load_state_dict(torch.load('weights/model.pth'))

cb = CatBoostClassifier()
cb.load_model('weights/catboost_model.cbm')

# route http posts to this method
@app.route('/api/test', methods=['POST'])
def test():
    r = request

    nparr = np.fromstring(r.data, np.uint8)

    tokens = tokenize_function(nparr)

    embeddings_test = get_embeddings(model_bert, tokens)

    results = cb.predict(embeddings_test)

    return jsonify(results)

if __name__ == '__main__':
    app.run(port=11111)
