import requests
from flask import current_app

def execute_query(query, values=None):
    """Calls the HBO-ICT.cloud API to execute a query."""
    url = current_app.config["API_URL"] + "/db"
    api_key = current_app.config["API_KEY"]
    database = current_app.config["DATABASE"]

    try:
        r = requests.post(
            url=url,
            json={"query": query, "values": values, "database": database},
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=10,
        )
        r.raise_for_status()  # HTTP errors gooien exception
        try:
            return r.json()
        except ValueError:
            print("JSONDecodeError! Response is geen JSON:", r.text)
            return []
    except requests.exceptions.RequestException as e:
        print("Request error:", e)
        return []   