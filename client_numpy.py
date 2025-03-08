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
