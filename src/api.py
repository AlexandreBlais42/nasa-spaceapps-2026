from datetime import datetime as dt
from requests import get
from base64 import b64encode
from typing import Tuple, Dict
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


def get_data(date, height_meters: int, coordinates: Tuple[float, float]):
    url = f"{BASE_URL}/{date.strftime(TIME_FORMAT)}/t_{height_meters}m/{coordinates[0]},{coordinates[1]}/json"
    response = get(url, headers=headers())

    response.ok
    if not response.ok:
        print(response.text)
        raise EnvironmentError()
    return json.loads(response.text)


if __name__ == "__main__":
    sherbrooke_coords = (45.40008, -71.89908)
    data = get_data(dt.now(), 2, sherbrooke_coords)
    print(data)
