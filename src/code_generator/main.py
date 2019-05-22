import os
import os.path as osp

import jinja2
from textx import metamodel_from_file
from textx.metamodel import TextXMetaModel

from src.settings import GRAMMAR_FILE_PATH, OUTPUT_DIR, JINJA_TEMPLATE_DIR, JINJA_DATA_TEMPLATE_DIR


class SimpleType(object):
    def __init__(self, parent, name):
        self.parent = parent
        self.name = name

    def __str__(self):
        return self.name


def get_meta_model():
    """
    Builds and returns a meta-model for language.
    """
    type_builtins = {
            'integer': SimpleType(None, 'integer'),
            'string': SimpleType(None, 'string')
    }
    mm = metamodel_from_file(file_name=GRAMMAR_FILE_PATH,
                             classes=[SimpleType],
                             builtins=type_builtins)

    return mm


def generate_data_code(data_node):

    jinja_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(JINJA_DATA_TEMPLATE_DIR),
        trim_blocks=True,
        lstrip_blocks=True)
    import_tmpl = jinja_env.get_template('imports.template')
    missing_values_tmpl = jinja_env.get_template('missing_values.template')
    outlier_removal_tmpl = jinja_env.get_template('outlier_removal.template')
    data_tmpl = jinja_env.get_template('data.template')

    with open(osp.join(OUTPUT_DIR, 'test.py'), 'w') as f:
        f.write(import_tmpl.render())
        f.write('\n\n\n')
        if data_node.missing_values is not None:
            f.write(missing_values_tmpl.render(data=data_node))
            f.write('\n\n')
        if data_node.outlier is not None:
            f.write(outlier_removal_tmpl.render(data=data_node))
            f.write('\n\n\n')
        f.write(data_tmpl.render(data=data_node))
    print()

def generate_code(mm: TextXMetaModel):
    """
    Generates code from given meta model using Jinja templates
    :param mm: TextXMetaModel
    :return:
    """
    generate_data_code(mm.data_expression)



def main(file_path):

    # Instantiate the Entity meta-model
    mm = get_meta_model()

    # Create the output folder
    if not osp.exists(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)

    # Initialize the template engine.


    # Build a Person model from person.ent file
    model = mm.model_from_file(file_path)

    # Generate Python code
    generate_code(model)


if __name__ == "__main__":
    main('/home/ognjen/Projects/Fax/DSL/dsl-2019/src/grammar/grammar_test.rbt')

