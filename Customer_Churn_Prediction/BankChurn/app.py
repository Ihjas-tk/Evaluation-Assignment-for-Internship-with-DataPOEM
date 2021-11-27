from flask import *
import requests
app = Flask(__name__)
app.secret_key='some'
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/back')
def back():
    return render_template('home.html')

@app.route('/go',methods=['POST','GET'])
def go():
    loc_ger=0
    loc_spa=0
    loc_frc=0
    id = int(request.form['id'])
    cred = int(request.form['credit'])
    loc = request.form['loc']
    gender = int(request.form['gender'])
    age = int(request.form['age'])
    ten = int(request.form['tenure'])
    bal = int(request.form['bal'])
    nop = int(request.form['nop'])
    card = int(request.form['card'])
    act = int(request.form['act'])
    sal = int(request.form['sal'])

    if loc == 'ger':
        loc_ger = 1
    elif loc == 'spa':
        loc_spa = 1
    elif loc == 'frn':
        loc_frc = 1
    array_of_input_fields = ["CreditScore", "Gender", "Age", "Tenure", "Balance", "NumOfProducts", "HasCrCard",
                             "IsActiveMember", "EstimatedSalary", "Germany", "France", "Spain"]
    print(array_of_input_fields)
    array_of_values_to_be_scored = [cred, gender, age, ten, bal, nop, card, act, sal, loc_ger, loc_frc, loc_spa]
    # # NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
    # API_KEY = "JLYX7arzplR8bZOU-WjFeqbvXLg5Bx2kI8OEFQeWywui"
    # token_response = requests.post('https://iam.eu-gb.bluemix.net/identity/token',
    #                                data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
    # mltoken = token_response.json()["access_token"]
    #
    # header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}
    #
    # # NOTE: manually define and pass the array(s) of values to be scored in the next line
    # payload_scoring = {"input_data": [{"fields": [array_of_input_fields], "values": [array_of_values_to_be_scored]}]}
    #
    # response_scoring = requests.post(
    #     'https://eu-gb.ml.cloud.ibm.com/ml/v4/deployments/efc928a5-87d3-41e7-9766-be07ea578486/predictions?version=2020-11-25',
    #     json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    # print("Scoring response")
    # NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
    API_KEY = "CJyHIYzdjhW6HSkZjmOaa7jPkBeIlb8lchMisT0PjJ06"
    token_response = requests.post('https://iam.eu-gb.bluemix.net/identity/token',
                                   data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
    mltoken = token_response.json()["access_token"]

    header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

    # NOTE: manually define and pass the array(s) of values to be scored in the next line
    payload_scoring = {"input_data": [{"fields": [array_of_input_fields],
                                       "values": [array_of_values_to_be_scored]}]}

    response_scoring = requests.post(
        'https://eu-gb.ml.cloud.ibm.com/ml/v4/deployments/3ec9fc3b-7eef-4612-b941-a9dbbd753ad5/predictions?version=2020-11-27',
        json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    print(response_scoring.json())
    var = response_scoring.json()
    if var['predictions'][0]['values'][0][0] == 0:
        out="The Customer Wont Exit"
    elif var['predictions'][0]['values'][0][0] == 1:
        out = "The Customer Will Exit"

    return render_template('home.html', out=out)


if __name__ == '__main__':
    app.run()
