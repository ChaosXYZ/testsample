# app.py

from flask import Flask, render_template, request, jsonify
from validate import validate_query

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/validate', methods=['POST'])
def validate():
    query = request.form['query']
    result = validate_query(query)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)