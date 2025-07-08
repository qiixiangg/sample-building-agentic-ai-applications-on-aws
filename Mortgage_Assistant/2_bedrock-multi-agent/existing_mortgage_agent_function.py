import json

def get_named_parameter(event, name):
    return next(item for item in event['parameters'] if item['name'] == name)['value']
    
def populate_function_response(event, response_body):
    return {'response': {'actionGroup': event['actionGroup'], 'function': event['function'],
                'functionResponse': {'responseBody': {'TEXT': {'body': str(response_body)}}}}}

def get_mortgage_details(customer_id):
    # TODO: Implement real business logic to retrieve mortgage status
    return {
        "account_number": customer_id,
        "outstanding_principal": 150000.0,
        "interest_rate": 4.5,
        "maturity_date": "2030-06-30",
        "payments_remaining": 72,
        "last_payment_date": "2024-06-01",
        "next_payment_due": "2024-07-01",
        "next_payment_amount": 1250.0
    }

def lambda_handler(event, context):
    print(event)
    function = event['function']
    if function == 'get_mortgage_details':
        customer_id = get_named_parameter(event, 'customer_id')
        if not customer_id:
            raise Exception("Missing mandatory parameter: customer_id")
        result = get_mortgage_details(customer_id)
    else:
        result = f"Error, function '{function}' not recognized"

    response = populate_function_response(event, result)
    print(response)
    return response
