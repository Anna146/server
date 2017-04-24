from flask import Flask, jsonify, request, send_from_directory

import os
import pandas
import numpy as np
#from document_recognition.learning.ModelTester import ModelTester

app = Flask(__name__)

MODELS_PATH = os.path.join('/', 'osm', 'aurebu', 'document_recognition', 'document_recognition', 'out', 'results')
DEBUG_MODELS_PATH = 'E:\\unstruct_labelling_data\\features_test\\results\\'
CSV_CONTENT_DTYPES = {0: np.int16, 1: np.int16, 2: np.int16, 3: np.int16, 4: np.int16, 7: object}


class Tester:

    def __init__(self):
        self.model_tester = None
        self.model_path = None

    def test(self, model_path, data):
        if self.model_path == None:
            self.model_path = model_path
        if self.model_path != model_path:
            self.model_path = model_path
            self.model_tester = ModelTester(model_path)
        data['label'] = self.model_tester.apply_json(data)
        return data

tester = Tester()

@app.route("/hello/<path:path>")
def start(path):
	return send_from_directory('static', path)


@app.route("/models", methods=['GET'])
def get_model_list():
    print(os.listdir(MODELS_PATH))
    response = jsonify({'models': os.listdir(DEBUG_MODELS_PATH)})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route("/test_files", methods=['GET'])
def get_test_files():
	return jsonify({'files': ['hier', 'koennte', 'ihre', 'liste', 'stehen']})


@app.route("/recognize", methods=['POST'])
def recognize():
	data = request.json
	pd = convert_json(data)
	res = tester.test(pd, data['model'])
	return res.to_csv(index=None, sep=' ')

def convert_json(data):
	pd = pandas.DataFrame()
	for page in data['document']['result']:
		tmp = pandas.DataFrame(page['words'])
		tmp['page'] = np.ones(len(tmp), dtype=int)*page['page']
		pd = pd.append(tmp)

	pd.columns = ['text', 'left', 'top', 'right', 'bottom', 'page']
	
	return pd[['left', 'top', 'right', 'bottom', 'page', 'text']]


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
