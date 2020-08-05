import yaml
from sqlalchemy.sql import sqltypes


def map_sqltypes(column_types):
    if isinstance(column_types, sqltypes.Integer):
        return 'integer'
    elif isinstance(column_types, sqltypes.SmallInteger) or isinstance(column_types, sqltypes.Boolean):
        return 'boolean'
    elif isinstance(column_types, sqltypes.String):
        return 'string'
    elif isinstance(column_types, sqltypes.DateTime):
        return 'string'
    elif isinstance(column_types, sqltypes.Date):
        return 'string'
    elif isinstance(column_types, sqltypes.Time):
        return 'string'
    elif isinstance(column_types, sqltypes.DECIMAL):
        return 'float'
    else:
        raise TypeError(f'Mapping fail: Unknown Column Type: {column_types}')


def map_model(sa_model):
    mapped_fields = {}

    for column in sa_model.__table__.columns:
        mapped_fields[column.name] = {
            'type': map_sqltypes(column.type),
            'auto_increment': str(column.autoincrement) == 'True',
            'nullable': bool(column.nullable),
            'default': bool(column.default),
        }

    return mapped_fields


def to_yaml(map, filepath):
    with open(filepath, 'w+') as outfile:
        yaml.dump(map, outfile, default_flow_style=False, allow_unicode=True)

