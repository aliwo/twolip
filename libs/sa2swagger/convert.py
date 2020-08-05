import re
from libs.sa2swagger.utils import map_model, to_yaml

def to_snake_case(name):
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()


def convert(model, filepath, template=None):
    model_name = to_snake_case(model.__name__)

    if template is None:
        template = {model_name: {'description': '', 'properties': {}}}

    map = map_model(model)
    for key, val in map.items():
        if key in template[model_name]['properties']:
            template[model_name]['properties'][key]['type'] = val['type']
            continue

        template[model_name]['properties'][key] = {
            'type': val['type']
        }

    for key in template[model_name].get('hidden', {}):
        del template[model_name]['properties'][key]

    if 'hidden' in template[model_name]:
        del template[model_name]['hidden']

    to_yaml(template, filepath)
    return template
