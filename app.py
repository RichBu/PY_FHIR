from flask import Flask, render_template
from fhir.resources.bundle import Bundle
#from fhir.resources.patient import Patient
#from fhir.resources.observation import Observation
#from fhirpy import FHIRClient
#import fhir_pyrate.pyrate as pyrate
import pandas as pd
import json
import requests
import config

app = Flask(__name__)

@app.route('/ping')
def ping():
    return 'pong..'

@app.route('/')
def main_route():
    return render_template('index.html')

@app.route('/geturl')
def get_url():
    fhir_url = config.FHIR_ONLINE
    return fhir_url

@app.route('/getbundle')
def get_bundle():
    full_url = config.FHIR_ONLINE + config.FHIR_GET_ALL_PATIENTS
    try:
        response = requests.get(full_url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

    print( response )
    print("print the url")
    print(response.url)
    print("response status")
    print(response.status_code)
    data = response.json()
    print("data")
    print(data)

    # Load the bundle data from a JSON file
    #with open('bundle.json', 'r') as f:
    #    bundle_data = json.load(f)

    # Parse the bundle data
    fhir_bundle = json.loads(response.text)

    #bundle = Bundle.parse_obj(fhir_bundle)

    '''
    # if using numpy
    # need to intialize the client
    client = FHIRClient(
        api_base=None,  #just local right now
        extra_settings={'app_id': 'app.py'}
    )

    fhir_py = client.server
    resource_type = fhir_data['resourceType']
    resource_id = fhir_data['id']
    
    # Assuming you want to "get" a resource, you could simulate it like this:
    resource = fhir_py.resource(resource_type, **fhir_data)

    # Now you can work with the resource object
    print(resource.id)
    print(resource.resource_type)
    '''
    

    '''
    bundle = Bundle.parse_obj(data)
    # Process each entry in the bundle
    for entry in bundle.entry:
        resource = entry.resource
        if resource.resource_type == 'Patient':
            patient = Patient.parse_obj(resource.dict())
            print(f"Patient: {patient.name[0].given[0]} {patient.name[0].family}")
        elif resource.resource_type == 'Observation':
            observation = Observation.parse_obj(resource.dict())
            print(f"Observation: {observation.code.text} - {observation.valueQuantity.value} {observation.valueQuantity.unit}")
        # Handle other resource types as needed
    '''
    return data

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


