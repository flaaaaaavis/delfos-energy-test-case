from datetime import datetime
import httpx

def extract(date: str, base_url: str):
    dt = datetime.strptime(date, "%Y-%m-%d")

    params = {
        "start": dt.strftime("%Y-%m-%dT00:00:00"),
        "end": dt.strftime("%Y-%m-%dT23:59:59"),
        "variables": ["wind_speed", "power"]
    }

    response = httpx.get(f"{base_url}/data", params=params)
    response.raise_for_status()

    return response.json()
