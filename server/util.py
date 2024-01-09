import os 
import json
import pickle
import numpy as np

__data_columns = None
__model = None
job_category = None
employee_residence = None
experience_level = None
work_setting = None
company_location = None
company_size = None

def get_vars():
    map = {
        'job_category': job_category,
        'employee_residence':employee_residence,
        'experience_level': experience_level,
        'work_setting': work_setting,
        'company_location': company_location,
        'company_size': company_size
    }
    return map

def find_column_range(json_data, start_string):
    data_columns = json_data or []  # Ensure data_columns is a list
    start_index = None
    end_index = None

    for i, column in enumerate(data_columns):
        if column.startswith(start_string):
            if start_index is None:
                start_index = i
            end_index = i

    if start_index is not None and end_index is not None:
        return data_columns[start_index:end_index + 1]
    else:
        return []


def get_salary(work_year, job_category, employee_residence, experience_level, work_setting, company_location, company_size):
    try:
        job_category_index = __data_columns.index(job_category.lower())
    except ValueError:
        job_category_index = -1
    
    try:
        employee_residence_index = __data_columns.index(employee_residence.lower())
    except ValueError:
        employee_residence_index = -1
    
    try:
        experience_level_index = __data_columns.index(experience_level.lower())
    except ValueError:
        experience_level_index = -1
    
    try:
        work_setting_index = __data_columns.index(work_setting.lower())
    except ValueError:
        work_setting_index = -1
    
    try:
        company_location_index = __data_columns.index(company_location.lower())
    except ValueError:
        company_location_index = -1
    
    try:
        company_size_index = __data_columns.index(company_size.lower())
    except ValueError:
        company_size_index = -1
    
    x = np.zeros(len(__data_columns))
    x[0] = work_year
    
    if job_category_index >= 0:
        x[job_category_index] = 1
    
    if employee_residence_index >= 0:
        x[employee_residence_index] = 1
    
    if experience_level_index >= 0:
        x[experience_level_index] = 1
    
    if work_setting_index >= 0:
        x[work_setting_index] = 1
    
    if company_location_index >= 0:
        x[company_location_index] = 1
    
    if company_size_index >= 0:
        x[company_size_index] = 1

    return __model.predict([x])[0]

def load_saved_artifacts():
    print("Starting artifacts loading process")
    global __data_columns
    global __model
    global job_category, employee_residence, experience_level, work_setting, company_location, company_size
    print("Current Working Directory:", os.getcwd())

    # Specify absolute paths
    columns_path = './artifacts/data_columns.json'
    model_path = './artifacts/data_science_model.pickle'

    with open(columns_path, "r") as f:
        __data_columns = json.load(f)['data_columns']
        job_category = find_column_range(__data_columns, 'job_category')
        employee_residence = find_column_range(__data_columns, 'employee_residence')
        experience_level = find_column_range(__data_columns, 'experience_level')
        work_setting = find_column_range(__data_columns, 'work_setting')
        company_location = find_column_range(__data_columns, 'company_location')
        company_size = find_column_range(__data_columns, 'company_size')

    with open(model_path, 'rb') as f:
        __model = pickle.load(f)

    res = get_salary(2023, 'job_category_Cloud and Database',"employee_residence_Germany", "experience_level_Senior", "work_setting_Hybrid", "company_location_United States","company_size_M")
    print(f'Test predict is {res}')
    print("Loading saved artifacts...done")
if __name__ == "__main__":
    load_saved_artifacts()