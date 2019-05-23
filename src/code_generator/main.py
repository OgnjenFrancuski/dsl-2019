import os.path as osp

import jinja2
from textx import metamodel_from_file
from textx.metamodel import TextXMetaModel

from src.settings import GRAMMAR_FILE_PATH, OUTPUT_DIR, JINJA_DATA_TEMPLATE_DIR, \
    JINJA_MODEL_TEMPLATE_DIR, SUPPORTED_MODELS


def get_meta_model():
    """
    Builds and returns a meta-model for language.
    """
    mm = metamodel_from_file(file_name=GRAMMAR_FILE_PATH)
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

    with open(osp.join(OUTPUT_DIR, 'data_handler.py'), 'w') as f:
        f.write(import_tmpl.render())
        f.write('\n\n\n')
        if data_node.missing_values is not None:
            f.write(missing_values_tmpl.render(data=data_node))
            f.write('\n\n')
        if data_node.outlier is not None:
            f.write(outlier_removal_tmpl.render(data=data_node))
            f.write('\n\n\n')
        f.write(data_tmpl.render(data=data_node))


def generate_model_code(model_expressions):

    if not model_expressions:
        return

    jinja_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(JINJA_MODEL_TEMPLATE_DIR),
        trim_blocks=True,
        lstrip_blocks=True)

    import_tmpl = jinja_env.get_template('imports.template')
    base_model_tmpl = jinja_env.get_template('model.template')
    model_templates = []

    for model_node in model_expressions:
        if model_node.type in SUPPORTED_MODELS:
            model_templates.append(
                jinja_env.get_template(SUPPORTED_MODELS[model_node.type])
            )

    if not model_templates:
        return

    with open(osp.join(OUTPUT_DIR, 'models.py'), 'w') as f:
        f.write(import_tmpl.render())
        f.write('\n\n\n')
        f.write(base_model_tmpl.render())
        f.write('\n\n\n')
        for tmpl in model_templates:
            f.write(tmpl.render())
            f.write('\n\n')


def generate_run_conf_code(run_expressions):
    pass


def generate_code(mm: TextXMetaModel):
    """
    Generates code from given meta model using Jinja templates
    :param mm: TextXMetaModel
    :return:
    """
    generate_data_code(mm.data_expression)
    generate_model_code(mm.model_expressions)


def main(file_path):

    # Instantiate the Entity meta-model
    mm = get_meta_model()

    # # Create the output folder
    # if not osp.exists(OUTPUT_DIR):
    #     os.mkdir(OUTPUT_DIR)
    #
    # # Initialize the template engine.

    # Build a Person model from person.ent file
    model = mm.model_from_file(file_path)

    # # Generate Python code
    generate_code(model)


if __name__ == "__main__":
    main('/home/ognjen/Projects/Fax/DSL/dsl-2019/src/grammar/grammar_test.rbt')

