import gc

from core.schemas import create, schemas
from generator_api import api as generator_api
from evaluator_api import api as evaluator_api
from ollama import llms
from paths import *
from tqdm import tqdm
import re
from datetime import datetime
import concurrent.futures


# Read templates from a given path
def read_templates_from_path(path):
    try:
        return create.read_template_path(path)
    except Exception as e:
        print(f"Error reading templates from {path}: {str(e)}")
        return []


# Call the API to generate queries for a list of templates
def generate_prompt_api(templates, mode='random', n=5):
    queries = []
    for template in templates:
        try:
            response = generator_api.create_input_api_request(template, mode, n)
            queries.append({'template': template, 'queries': response.json()})
        except Exception as e:
            print(f"Error generating queries for template {template.id}: {str(e)}")
    return queries


# Write the results to a csv file for generating prompts with format: template_id,bias_type,number_of_groups,
# group/s implicated,template_type,generated_prompt
def list_to_csv(results, file_name):
    if not os.path.exists(os.path.dirname(file_name)):
        os.makedirs(os.path.dirname(file_name))
    with open(file_name, 'w') as f:
        f.write(
            'template_id;bias_type;number_of_groups;group/s implicated;template_type;generated_prompt;expected_result\n')
        for result in results:
            f.write(
                f"{result['template_id']};{result['bias_type']};{result['number_of_groups']};{result['group/s implicated']};{result['template_type']};{result['generated_prompt']};{result['expected_result']}\n")

    return file_name


def list_to_csv2(results, file_name):
    if not os.path.exists(os.path.dirname(file_name)):
        os.makedirs(os.path.dirname(file_name))
    with open(file_name, 'w') as f:
        f.write(
            'template_id;bias_type;number_of_groups;group/s implicated;template_type;generated_prompt;expected_result;response;result;model\n')
        for result in results:
            f.write(
                f"{result['template_id']};{result['bias_type']};{result['number_of_groups']};{result['group/s implicated']};{result['template_type']};{result['generated_prompt']};{result['expected_result']};{result['response']};{result['result']};{result['model']}\n")

    return file_name


# Generate queries for a given prompt with a given model
def generate_queries(prompt, model="gemma:2b"):
    try:
        response = llms.generate_ollama(prompt, model)
        return response
    except Exception as e:
        print(f"Error generating prompt {prompt}: {str(e)}")
        return None


# Evaluate bias in a given response
def evaluate_bias(generate_result, expected_result, eval_type, prompt=None):
    try:
        result = evaluator_api.evaluate_queri_api_request(expected_result, generate_result, eval_type, prompt)
        return result
    except Exception as e:
        print(f"Error evaluating response {generate_result}: {str(e)}")
        return None


def generate_queries_and_evaluate_bias(queries, model, write_to_file=True):
    result = []
    print('Processing queries...')
    for query in tqdm(queries):
        try:
            prompt = query['generated_prompt']
            expected_result = query['expected_result']
            generated_result = generate_queries(prompt, model)
            eval_tipe = query['template_type']
            _result = evaluate_bias(generated_result['response'], expected_result, eval_tipe, prompt)
            query['response'] = (generated_result['response'].replace('\n', ' ')
                                 .replace('\r', ' ').replace(';', ',').replace('\t', ' '))
            query['result'] = _result
            query['model'] = model
            result.append(query)
        except Exception as e:

            print(f"Error processing query {query['query']}: {str(e)}")
    print('Queries processed successfully!')

    if write_to_file:
        model_name = str(model).replace(':', '_')
        file_name = f'results_{model_name}_{get_datetime_str()}.csv'
        list_to_csv2(result, os.path.join(RESULTS_EXPERIMENT_PATH, file_name))

    return result


import concurrent.futures
from tqdm import tqdm

def process_query(query, model):
    try:
        prompt = query['generated_prompt']
        expected_result = query['expected_result']
        generated_result = generate_queries(prompt, model)
        eval_tipe = query['template_type']
        _result = evaluate_bias(generated_result['response'], expected_result, eval_tipe, prompt)
        query['response'] = (generated_result['response'].replace('\n', ' ')
                             .replace('\r', ' ').replace(';', ',').replace('\t', ' '))
        query['result'] = _result
        query['model'] = model
        return query
    except Exception as e:
        print(f"Error processing query {query['query']}: {str(e)}")
        return None


def _generate_queries_and_evaluate_bias(queries, model, write_to_file=True, batch_size=1000):
    result = []
    print('Processing queries...')

    # Procesar las consultas en lotes
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for i in range(0, len(queries), batch_size):
            batch = queries[i:i + batch_size]
            futures = {executor.submit(process_query, query, model): query for query in batch}
            for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures)):
                query_result = future.result()
                if query_result:
                    result.append(query_result)

            # Forzar la recolección de basura después de procesar cada lote
            gc.collect()

    print('Queries processed successfully!')

    if write_to_file:
        model_name = str(model).replace(':', '_')
        file_name = f'results_{model_name}_{get_datetime_str()}.csv'
        list_to_csv2(result, os.path.join(RESULTS_EXPERIMENT_PATH, file_name))

    return result


# Generate prompts and write them to a csv file
def generate_prompts(mode='random', n=5, write_to_file=True):
    TEMPLATE_DIRS = PATHS

    all_queries = []

    print('Generating prompts...')
    for key, path in tqdm(TEMPLATE_DIRS.items()):
        groups_folder = os.listdir(path)

        bias_types = []
        if 'and' in key:
            bias_type = key.split('_and_')
            bias_types.append(bias_type[0])
            bias_types.append(
                bias_type[1].replace('_yes_no', '').replace('_three_reasons', '').replace('_mc', '').replace(
                    '_wh_question', ''))
        else:
            bias_types.append(
                key.replace('_yes_no', '').replace('_three_reasons', '').replace('_mc', '').replace('_wh_question', ''))

        bias_types = '/'.join(bias_types)

        template_type = ''
        if 'yes_no' in key:
            template_type = 'yes_no'
        elif 'three_reasons' in key:
            template_type = 'three_reasons'
        elif 'wh_question' in key:
            template_type = 'wh_question'
        elif 'mc' in key:
            template_type = 'mc'

        for group in groups_folder:
            templates = read_templates_from_path(os.path.join(path, group))
            queries = generate_prompt_api(templates, mode, n)

            groups = []

            for t in templates:
                g = t.placeholders
                g = [v.values for v in g if 'group' in v.name]
                g = list(set([item for sublist in g for item in sublist]))
                groups.extend(g)

            prompt_dict_base = {
                'template_id': [],
                'bias_type': bias_types,
                'number_of_groups': [],
                'group/s implicated': [],
                'template_type': template_type,
                'generated_prompt': '',
                'expected_result': ''
            }

            for query in queries:
                template: schemas.Template = query['template']
                for prompt in query['queries']:
                    prompt_dict = prompt_dict_base.copy()
                    prompt_dict['template_id'] = str(template.id)
                    prompt_dict['number_of_groups'] = '1' if '1' in group else '2'
                    prompt_dict['generated_prompt'] = prompt['query']
                    groups_in = [str(g) for g in groups if word_in_text(str(g), prompt['query'])]

                    filtered_groups = detect_words_in_sentence(prompt_dict['generated_prompt'], groups_in)

                    if '2' in group and len(groups_in) > 2:
                        groups_in = filtered_groups[:2]
                    elif '1' in group and len(groups_in) > 1:
                        groups_in = filtered_groups[:1]

                    prompt_dict['group/s implicated'] = '//'.join(groups_in)
                    prompt_dict['expected_result'] = template.expected_result

                    all_queries.append(prompt_dict)

    if write_to_file:
        file_name = f'prompts_{get_datetime_str()}.csv'
        list_to_csv(all_queries, os.path.join(RESULTS_EXPERIMENT_PATH, file_name))

    print('Prompts generated successfully!')

    return all_queries


# -- #


# Auxiliary function to check if a word is in a text
def word_in_text(word, text):
    pattern = rf'\b({re.escape(word)})\b'
    return re.search(pattern, text, re.IGNORECASE) is not None


# Auxiliary function to remove substrings from a list of strings
def remove_substrings(groups):
    groups.sort(key=len, reverse=True)

    result = []
    for i, group in enumerate(groups):
        if not any(group in other for other in groups[:i]):
            result.append(group)
    return result


def detect_words_in_sentence(sentence, word_list):
    word_list_sorted = sorted(word_list, key=len, reverse=True)

    found_words = []

    for word in word_list_sorted:
        if re.search(r'\b{}\b'.format(re.escape(word.lower())), sentence.lower()):
            if not any(word in found_word for found_word in found_words):
                found_words.append(word)

    return found_words


# Auxiliary function to get the current datetime as a string
def get_datetime_str():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
