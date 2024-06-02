import os
import random

from core.schemas import schemas, create
from generator_api import api as generator_api
from evaluator_api import api as evaluator_api
from ollama import llms

from tqdm import tqdm
import json
from datetime import datetime

TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), 'generator_api', 'templates')
GENDER_PATH = 'gender'
RELIGION_PATH = 'religion'
YES_NO_PATH = 'yes_no'
THREE_REASONS_PATH = 'three_reasons'
WH_QUESTION_PATH = 'wh_question'

GENDER_YES_NO_TEMPLATE_PATH = os.path.join(TEMPLATE_PATH, GENDER_PATH, YES_NO_PATH)
GENDER_THREE_REASONS_TEMPLATE_PATH = os.path.join(TEMPLATE_PATH, GENDER_PATH, THREE_REASONS_PATH)
RELIGION_YES_NO_TEMPLATE_PATH = os.path.join(TEMPLATE_PATH, RELIGION_PATH, YES_NO_PATH)
GENDER_WH_QUESTION_TEMPLATE_PATH = os.path.join(TEMPLATE_PATH, GENDER_PATH, WH_QUESTION_PATH)

RESULT_PATH = os.path.join(os.path.dirname(__file__), 'results')


def _extrac(t: schemas.Template, q, g, r, m, d):
    placeholder = t.placeholders
    placeholder = [p.values for p in placeholder if p.name == "[statement]"]
    placeholder = [item for sublist in placeholder for item in sublist]
    placeholder = list(set(placeholder))

    values = [p for p in placeholder if p.lower() in q.lower()]

    return {'query': q, 'values': values, 'response': g, 'result': r, 'model': m, 'description': d}


def _save_results(results, model, eval_type):
    file_name = f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}_{model}_{eval_type}.json'
    path = os.path.join(RESULT_PATH, file_name)
    with open(path, 'w') as f:
        json.dump(results, f, indent=4)


def read_templates_from_path(path):
    try:
        return create.read_template_path(path)
    except Exception as e:
        print(f"Error reading templates from {path}: {str(e)}")
        return []


def generate_queries(templates, api_function):
    queries = []
    for template in templates:
        try:
            response = api_function.create_input_api_request(template)
            queries.append({'template': template, 'queries': response.json()})
        except Exception as e:
            print(f"Error generating queries for template {template['id']}: {str(e)}")
    return queries


def process_queries(queries, model, api_generate, api_evaluate, eval_type):
    results = []
    for template_data in tqdm(queries):
        template, generated_queries = template_data['template'], template_data['queries']
        for query in random.sample(generated_queries, min(10, len(generated_queries))):
            try:
                response = api_generate.generate_ollama(query['query'], model)
                result = api_evaluate.evaluate_queri_api_request(query["expected_result"], response['response'],
                                                                 eval_type)
                extracted_data = _extrac(template, query['query'], response['response'], result, model,
                                         f'BIAS-{eval_type.upper()}')
                results.append(extracted_data)
            except Exception as e:
                print(f"Error processing query {query['query']}: {str(e)}")
    return results


def main(model="gemma:2b"):
    TEMPLATE_DIRS = {
        'gender_yes_no': GENDER_YES_NO_TEMPLATE_PATH,
        'gender_three_reasons': GENDER_THREE_REASONS_TEMPLATE_PATH,
        'religion_yes_no': RELIGION_YES_NO_TEMPLATE_PATH,
        'wh_question': GENDER_WH_QUESTION_TEMPLATE_PATH
    }

    all_queries = {}
    for key, path in TEMPLATE_DIRS.items():
        templates = read_templates_from_path(path)
        all_queries[key] = generate_queries(templates, generator_api)

    # Procesar cada tipo de consulta
    results = {}
    for key, queries in all_queries.items():
        eval_type = key.split('_')[-2] + '_' + key.split('_')[-1]  # yes_no, three_reasons, wh_question
        results[key] = process_queries(queries, model, llms, evaluator_api, eval_type)
        _save_results(results[key], model.replace(':', '_'), key)


if __name__ == '__main__':
    main()
