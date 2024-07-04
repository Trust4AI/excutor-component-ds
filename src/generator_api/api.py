from core.schemas import schemas
from core.settings.env import env
import requests
import json

GENERATOR_API_URL = f'http://{env.get("GENERATOR_HOST")}:{env.get("GENERATOR_PORT")}/api/v{env.get("GENERATOR_API_VERSION")}'


def create_input_api_request(template: schemas.Template, mode='random', n=5):
    url = f'{GENERATOR_API_URL}/input/generateWithTemplate?mode={mode}&n={n}'

    body = template

    response = requests.post(url, data=json.dumps(body.dict()), headers={'Content-Type': 'application/json'})

    return response
