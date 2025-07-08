import json
from datetime import datetime, timedelta
import random

NO_CUSTOMER_MESSAGE = "Invalid function call, since no customer ID was provided as a parameter, and it was not passed in session state."

def get_named_parameter(event, name):
    if 'parameters' in event:
        if event['parameters']:
            for item in event['parameters']:
                if item['name'] == name:
                    return item['value']
        return None
    else:
        return None
    
def populate_function_response(event, response_body):
    return {'response': {'actionGroup': event['actionGroup'], 'function': event['function'],
                'functionResponse': {'responseBody': {'TEXT': {'body': str(response_body)}}}}}

def get_mortgage_app_doc_status(customer_id):
    # TODO: Implement the actual logic to retrieve the document status for the given customer ID
    return [
        {
            "type": "proof_of_income",
            "status": "COMPLETED"
        },
        {
            "type": "employment_information",
            "status": "MISSING"
        },
        {
            "type": "proof_of_assets",
            "status": "COMPLETED"
        },
        {
            "type": "credit_information",
            "status": "COMPLETED"
        }
    ]


def get_application_details(customer_id):
    return {
        "customer_id": customer_id,
        "application_id": "998776",
        "application_date": datetime.today() - timedelta(days=35), # simulate app started 35 days ago
        "application_status": "IN_PROGRESS",
        "application_type": "NEW_MORTGAGE",
        "name" : "Mithil"
    }

def create_customer_id():
    return "123456"

def create_loan_application(customer_id, name, age, annual_income, annual_expense):
    print(f"creating loan application for customer: {customer_id}...")
    print(f"customer name: {name}")
    print(f"customer age: {age}")
    print(f"customer annual income: {annual_income}")
    print(f"customer annual expense: {annual_expense}")

    
def lambda_handler(event, context):
    print(event)
    function = event['function']

    if function == 'get_mortgage_app_doc_status':
        customer_id = get_named_parameter(event, 'customer_id')
        if not customer_id:
            # pull customer_id from session state variables if it was not supplied
            session_state = event['sessionAttributes']
            if session_state is None:
                return NO_CUSTOMER_MESSAGE
            else:
                if 'customer_id' in session_state:
                    customer_id = session_state['customer_id']
                else:
                    # return NO_CUSTOMER_MESSAGE
                    # for now, graceully just default, since this is just a toy example
                    customer_id = "123456"
            print(f"customer_id was pulled from session state variable = {customer_id}")
        result = get_mortgage_app_doc_status(customer_id)

    elif function == 'get_application_details':
        customer_id = get_named_parameter(event, 'customer_id')
        if not customer_id:
            # pull customer_id from session state variables if it was not supplied
            session_state = event['sessionAttributes']
            if session_state is None:
                return NO_CUSTOMER_MESSAGE
            else:
                if 'customer_id' in session_state:
                    customer_id = session_state['customer_id']
                else:
                    # return NO_CUSTOMER_MESSAGE
                    # for now, graceully just default, since this is just a toy example
                    customer_id = "123456"
            print(f"customer_id was pulled from session state variable = {customer_id}")
        result = get_application_details(customer_id)
    elif function == 'create_customer_id':
        result = create_customer_id()

    elif function == 'create_loan_application':
        customer_id = get_named_parameter(event, 'customer_id')
        if not customer_id:
            # pull customer_id from session state variables if it was not supplied
            session_state = event['sessionAttributes']
            if session_state is None:
                return NO_CUSTOMER_MESSAGE
            else:
                if 'customer_id' in session_state:
                    customer_id = session_state['customer_id']
                else:
                    # return NO_CUSTOMER_MESSAGE
                    # for now, graceully just default, since this is just a toy example
                    customer_id = "XXXXXX"
            print(f"customer_id was pulled from session state variable = {customer_id}")
        name = get_named_parameter(event, 'name')
        age = get_named_parameter(event, 'age')
        annual_income = get_named_parameter(event, 'annual_income')
        annual_expense = get_named_parameter(event, 'annual_expense')
       
        result = create_loan_application(customer_id, name, age, annual_income, annual_expense)
    else:
        raise Exception(f"Unrecognized function: {function}")


    response = populate_function_response(event, result)
    print(response)
    return response
