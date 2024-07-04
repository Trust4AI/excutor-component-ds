from core.schemas import schemas
import json
import os


def create_template_json(template_path: str):
    with open(template_path, 'r') as f:
        template = json.load(f)
    if type(template) is list:
        return [schemas.Template(**t) for t in template]
    else:
        return schemas.Template(**template)

def read_template_path(template_path: str):
    list_dir = os.listdir(template_path)

    result = []

    for file in list_dir:
        if file.endswith('.json'):
            t = create_template_json(os.path.join(template_path, file))
            if type(t) is list:
                result.extend(t)
            else:
                result.append(t)

    return result


if __name__ == '__main__':
    rt = read_template_path("C:/Users/vicen/SCORE/executor/generator_api/templates/gender/yes_no")

    print(rt)
