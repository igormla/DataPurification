import requests
from utilities import TransformText

# URLs stored for the GET and POST requests to a Flask app
get_url = "http://localhost:5000/companies"
post_url = "http://localhost:5000/companies"

# Receiving the response of a GET request to the "get_url" of a Flask app
response = requests.get(get_url)

# Getting the json version of the processed data which was received with the response
companies = response.json()

# Cleaning the names of the companies from the received data
companies = TransformText.clean_text_data(companies)

# Sending the process data with a POST request to the "post_url" of a Flask app
post_process_data = requests.post(post_url, json=companies)

# Status message in terminal about the success of script completion
print("Script executed successfully.")
