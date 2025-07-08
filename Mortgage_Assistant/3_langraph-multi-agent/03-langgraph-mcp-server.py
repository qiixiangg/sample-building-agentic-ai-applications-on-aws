import random
from datetime import datetime, timedelta
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Mortgage Tools")

@mcp.tool()
async def get_mortgage_details(customer_id: str):
    """
Retrieves the mortgage status for a given customer ID. Returns an object containing 
details like the account number, 
outstanding principal, interest rate, maturity date, number of payments remaining, due date of next payment, 
and amount of next payment."""
    return {
        "account_number": customer_id,
        "outstanding_principal": 150599.25,
        "interest_rate": 8.5,
        "maturity_date": "2030-06-30",
        "original_issue_date": "2021-05-30",
        "payments_remaining": 72,
        "last_payment_date": str(datetime.today() - timedelta(days=14)).split(' ')[0],
        "next_payment_due": str(datetime.today() + timedelta(days=14)).split(' ')[0],
        "next_payment_amount": 1579.63
    }

@mcp.tool()
async def get_application_details(customer_id: str):
    """Retrieves the details about an application for a new mortgage. The function takes a customer ID, but it is purely optional. 
    The function implementation can retrieve it from session state instead. 
    Details include the application ID, application date, application status, application type, application amount, application tentative rate, and application term in years."""
    return {
        "customer_id": customer_id,
        "application_id": "998776",
        "application_date": datetime.today() - timedelta(days=35), # simulate app started 35 days ago
        "application_status": "IN_PROGRESS",
        "application_type": "NEW_MORTGAGE",
        "application_amount": 750000,
        "application_tentative_rate": 5.5,
        "application_term_years": 30,
        "application_rate_type": "fixed"
    }

@mcp.tool()
async def get_mortgage_rate_history(day_count: int=30, type: str="15-year-fixed"):
    """Retrieves the history of mortgage interest rates going back a given number of days, defaults to 30. History is returned as a list of objects, where each object contains the date and the interest rate to 2 decimal places."""
    BASE_RATE=6.00

    RATE_MIN_15=38
    RATE_MAX_15=48

    RATE_MIN_30=RATE_MIN_15 + 80
    RATE_MAX_30=RATE_MAX_15 + 80
    
    print(f"getting rate history for: {day_count} days, for type: {type}...")
    # generate the last 7 working day dates starting with yesterday
    today = datetime.today()
    history_count = 0
    rate_history = []

    if type == "30-year-fixed":
        RATE_MIN = RATE_MIN_30
        RATE_MAX = RATE_MAX_30
    else:
        RATE_MIN = RATE_MIN_15
        RATE_MAX = RATE_MAX_15

    for i in range(int(day_count*1.4)):
        if history_count >= day_count:
            break
        else:
            day = today - timedelta(days=i+1)
            which_day_of_week = day.weekday()
            if which_day_of_week < 5:
                history_count += 1
                _date = str(day.strftime("%Y-%m-%d"))
                _rate = f"{BASE_RATE + ((random.randrange(RATE_MIN, RATE_MAX))/100):.2f}"
                rate_history.append({"date": _date, "rate": _rate})

    return rate_history

@mcp.tool()
async def get_mortgage_app_doc_status(customer_id: str):
    """
    Retrieves the list of required documents for a mortgage application in process, along with their respectiv statuses (COMPLETED or MISSING).
    The function takes a customer ID, but it is purely optional. The funciton implementation can retrieve it from session state instead. 
    This function returns a list of objects, where each object represents a required document type. 
    The required document types for a mortgage application are: proof of income, employment information, proof of assets, and credit information. Each object in the returned list contains the type of the required document and its corresponding status."""
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

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
