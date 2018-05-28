from keras.models import load_model
import json

# Load the model.save()'d keras model here
model = load_model('your_model_here.h5')

# This is an example handler, set up to integrate with API gateway
def handle(event, context):
    # Pull data from the event request
    data_in = event['some_request_arg']
    
    # Run the model
    data_out = model.predict(data_in)

    # And return a response (formatted the way API gateway expects)
    return {
        'statusCode': 200,
        'headers': {
            # This header will allow another site to hit your endpoint.
            # If you want to keep things private, make sure to remove it.
            'Access-Control-Allow-Origin': '*',
        },
        # Response data: figure out how to get your data_out into a clean JSON 
        # response, and send it here
        'body': json.dumps({
            'data_out': data_out,
        }),
        'isBase64Encoded': False,
    }
