from flask import Flask, render_template, request, jsonify
from genTestCases import generate_test_cases  # Import your function
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/generate_testcases', methods=['POST'])
def generate_testcases():

    data = request.get_json()   
    context = data.get('context')
    requirements = data.get('requirements')
    acceptance_criteria = data.get('acceptance_criteria')


    data = generate_test_cases(context, requirements, acceptance_criteria,isregenerate=False)
    response = jsonify(data)
    response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
    return response


@app.route('/regenerate_testcases', methods=['POST'])
def regenerate_testcases():

    data = request.get_json()   
    context = data.get('context')
    data = generate_test_cases(context,requirements="",acceptance_criteria="",isregenerate=True)
    response = jsonify(data)
    response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
    return response


if __name__ == '__main__':
    app.run(debug=True)
