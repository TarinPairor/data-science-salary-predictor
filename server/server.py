from flask import Flask, request, jsonify, abort
from flask_cors import CORS
import util

app = Flask(__name__)
CORS(app)

util.load_saved_artifacts()

@app.route('/hello')
def hello():
    return "Hi"

@app.route('/map')
def get_map():
    map = util.get_vars()
    response = jsonify(map)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/keys')
def get_keys():
    keys = util.get_vars().keys
    response = jsonify(keys)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/get_vars/<var>')
def get_specific_vars(var):
    result_map = util.get_vars()

    if var in result_map:
        response = jsonify(result_map[var])
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    else:
        abort(404, description="Invalid URL")


@app.route('/predict', methods=['POST'])
def predict_salary():
    try:
        data = request.get_json()
        print("Received data:", data)
        
        # Extract data from the JSON payload
        work_year = int(data['work_year'])
        job_category = data['job_category']
        employee_residence = data['employee_residence']
        experience_level = data['experience_level']
        work_setting = data['work_setting']
        company_location = data['company_location']
        company_size = data['company_size']

        # Call the get_salary function
        estimated_price = util.get_salary(
            work_year, job_category, employee_residence,
            experience_level, work_setting, company_location, company_size
        )

        response = jsonify({'estimated_salary': estimated_price})
        response.headers.add('Access-Control-Allow-Origin', '*')

        return response

    except Exception as e:
        print("Error:", str(e))
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == "__main__":
    print("Starting Flask Server")
    app.run()
