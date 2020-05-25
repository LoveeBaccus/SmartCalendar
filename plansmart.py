from wtforms import StringField
import urllib.request
import json

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, StringField):
            return str(o.raw_data[0])
        return json.JSONEncoder.default(self, o)

def input_to_formatted_data(subject, num_problems, q_type, difficulty):
    return {
        "Inputs": {
                "input1": [
                    {
                            "Subject": subject,   
                            "Number of Problems": num_problems,   
                            "Type of Questions": q_type,   
                            "Difficulty": difficulty,   
                            "Time (min)": "0",  
                    }, 
                ],
        },
        "GlobalParameters":  {
    }
}


def get_data_from_azure(input):
    body = str.encode(JSONEncoder().encode(input))

    url = 'https://ussouthcentral.services.azureml.net/workspaces/7ea34294c35d43aea92d4d068327a9ff/services/2c76d2371edd4750b9c382a4381932fc/execute?api-version=2.0&format=swagger'
    api_key = 'DsQm5diU2DoRwx8UuE6de09jE5X+q2NgZP0kf8YgXrjG5BSuiXcNvITtGwiDfEJaEBRNZqSP4zDfARfdlSIWJA==' # Replace this with the API key for the web service
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)
        result = response.read()

        return json.loads(result)['Results']['output1'][0]['Scored Labels']
    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))
        print(error.info())
        print(json.loads(error.read().decode("utf8", 'ignore')))

def main():
    data["Inputs"]["input1"][0]["Subject"]             = input("Enter the subject\n~> ")  
    data["Inputs"]["input1"][0]["Number of Problems"]  = input("Enter the Number of Problems\n~> ")
    data["Inputs"]["input1"][0]["Type of Questions"]   = input("Enter the Type of Questions\n~> ")
    data["Inputs"]["input1"][0]["Difficulty"]          = input("Enter the Difficulty\n~> ")
    data["Inputs"]["input1"][0]["Time (min)"]          = 0 #input("Enter Time in minutes\n~> ")

    print("Your homework will take you {} minutes... ".format(get_data_from_azure(data)))
