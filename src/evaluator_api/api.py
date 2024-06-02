from core.settings.env import env
import requests
import json
from core.schemas import schemas

EVALUATOR_API_URL = f'http://{env.get("EVALUATOR_HOST")}:{env.get("EVALUATOR_PORT")}/api/v{env.get("EVALUATOR_API_VERSION")}'


def evaluate_queri_api_request(expected_result: str, generated_result: str, eval_type: str):
    url = f'{EVALUATOR_API_URL}/evaluate?evaluation_type={eval_type}'

    data = schemas.Output(expected_result=expected_result, generated_result=generated_result)
    response = requests.post(url, data=json.dumps(data.dict()), headers={'Content-Type': 'application/json'})

    return response.text

