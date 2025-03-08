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

class BundleShortDesc():
    def __init__(self, _id, _resource_type, _name_given, _name_family):
        self.id = _id
        self.resource_type = _resource_type
        self.name_given = _name_given
        self.name_family = _name_family

def BundleShortDec_serializer(obj):
    if isinstance(obj, BundleShortDesc):
        return obj.__dict__
    raise TypeError("Object of type '%s' is not JSON serializable" % obj.__class__.__name__)


class ServerStatus():
    def __init__(self, _status, _server_obj):
        self.status = _status
        self.server_obj = _server_obj

def ServerStatus_serializer(obj):
    if isinstance(obj, ServerStatus):
        return obj.__dict__
    raise TypeError("Object of type '%s' is not JSON serializable" % obj.__class__.__name__)


def pretty_print(data):
    pretty_json = json.dumps(data, indent=4)
    print(pretty_json)
    return


@app.route('/ping')
def ping():
    return 'pong..'


@app.route('/')
def main_route():
    return render_template('index.html')


@app.route('/about')
def index_route():
    return render_template('about.html')


@app.route('/bundle')
def bundle_route():
    return render_template('bundle.html')


@app.route('/geturl')
def get_url():
    fhir_url = config.FHIR_ONLINE
    return fhir_url


@app.route('/getstatus')
def get_status():
    out_obj = []
    server_obj = []
    out_status = "down"
    full_url = config.FHIR_ONLINE + config.FHIR_GET_STATUS
    try:
        out_status = "up & running"
        response = requests.get(full_url)
        response.raise_for_status()
        data = response.json()
        server_obj = json.dumps(data)
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        server_obj = "request error"
    except Exception as e:
        print(f"An error occurred: {e}")
        server_obj = "error"

    out_obj = ServerStatus(out_status, server_obj)
    out_rec = json.dumps(out_obj, default=ServerStatus_serializer)   
    return out_rec

@app.route('/getbundle')
def get_bundle():
    out_array = []
    full_url = config.FHIR_ONLINE + config.FHIR_GET_ALL_PATIENTS
    try:
        response = requests.get(full_url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

    data = response.json()

    # Load the bundle data from a JSON file
    #with open('bundle.json', 'r') as f:
    #    bundle_data = json.load(f)

    # Parse the bundle data
    fhir_bundle = json.loads(response.text)
    #print (fhir_bundle)
    resourceType = fhir_bundle["resourceType"]

    # key text is causing problems with bundles
    '''
    key_to_drop = 'text'
    if key_to_drop in fhir_bundle:
        del fhir_bundle[key_to_drop]
    '''

    # walk thru all of the entries
    fr_entries = fhir_bundle["entry"]
    # if use for loop then the item number in the array is the same as the key
    for i,rec in enumerate(fr_entries):
        fr_id = ""
        fr_name_rec = ""
        fr_name_family = ""
        fr_name_given = ""
        fr_resource_type = ""

        try:
          fr_resource = rec["resource"]
        except KeyError:
            fr_resource = "no resource"
            fr_id = "no resource"
            fr_name_rec = "no resource"
            fr_name_family = "no resource"
            fr_name_given = "no resource"
            pass
        except json.JSONDecodeError:
            fr_resource = "bad json"
            fr_id = "bad json"
            fr_name_rec = "bad json"
            fr_name_family = "bad json"
            fr_name_given = "bad json"
            pass

        if fr_id == "":   # no error
            try: 
               fr_resource_type = fr_resource["resourceType"]
            except KeyError:
                fr_resource_type = "no resource type"
            except json.JSONDecodeError:
                fr_resource_type = "bad json - resourceType"
                pass

            try: 
                fr_id = fr_resource["id"]
            except KeyError:
                fr_id = "no id"
            except json.JSONDecodeError:
                fr_id = "bad json - id"
                pass

            try: 
                fr_name_rec = fr_resource["name"]
                #print("fr_name_rec")
                #pretty_print(fr_name_rec)
                for i,name in enumerate(fr_name_rec):
                    if i==0:  #grab the first name  
                        try: 
                            fr_name_family = fr_name_rec[0]["family"]
                        except KeyError:
                            fr_name_family = "no family"
                        except json.JSONDecodeError:
                            fr_name_family = "bad json - family"
                            pass

                        try: 
                            fr_name_given = fr_name_rec[0]["given"][0]
                        except KeyError:
                            fr_name_given = "no given"
                        except json.JSONDecodeError:
                            fr_name_given = "bad json - given"
                            pass
            except KeyError:
                fr_name_rec = "no name"
                fr_name_family = ""
                fr_name_given = ""
            except json.JSONDecodeError:
                fr_name_rec = "bad json - name"
                fr_name_family = ""
                fr_name_given = ""
                pass

        out_rec_obj = BundleShortDesc(fr_id, fr_resource_type, fr_name_given, fr_name_family)
        out_rec = json.dumps(out_rec_obj, default=BundleShortDec_serializer)

        out_array.append(out_rec)
    pass
    #bundle = Bundle.parse_obj(fhir_bundle)

    #return fhir_bundle
    return out_array

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


