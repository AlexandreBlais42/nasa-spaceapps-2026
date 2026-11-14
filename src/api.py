from datetime import datetime, timedelta
from requests import get
from base64 import b64encode
from typing import Tuple, Dict, Optional
import pandas as pd
import json

# URL format:
# https://api.meteomatics.com/validdatetime/parameters/locations/format?optionals

TIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
BASE_URL = "https://api.meteomatics.com/"

credentials = {
    "username": "hackathon_nasa_space_apps_bla_alex",
    "password": "25et0qbpQ3VLB156INhp",
}

def headers() -> Dict[str, str]:
    logins = f"{credentials["username"]}:{credentials["password"]}"
    authorization = f"Basic {b64encode(logins.encode()).decode()}"

    return {
        "Authorization": authorization,
    }


def get_data_range(start_time, delta, height_meters: int, coordinates: Tuple[float, float]):
    end_time = start_time + delta
    url = f"{BASE_URL}/{start_time.strftime(TIME_FORMAT)}--{end_time.strftime(TIME_FORMAT)}/t_{height_meters}m/{coordinates[0]},{coordinates[1]}/json"
    response = get(url, headers=headers())

    if not response.ok:
        print(response.text)
        raise EnvironmentError()

    data = json.loads(response.text)
    data = data["data"][0]["coordinates"][0]["dates"]

    for i in range(len(data)):
        date_str = data[i]["date"]
        time = datetime.strptime(date_str, TIME_FORMAT)
        data[i]["date"] = time

    return pd.DataFrame.from_dict(data)


if __name__ == "__main__":
    sherbrooke_coords = (45.40008, -71.89908)
    data = get_data_range(datetime.now(), timedelta(days=2), 2, sherbrooke_coords)
    print(data)
