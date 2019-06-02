import os
import os.path as osp

import jinja2

from src.settings import JINJA_DATA_TEMPLATE_DIR, OUTPUT_DIR, JINJA_MODEL_TEMPLATE_DIR, SUPPORTED_MODELS, \
    JINJA_RUN_TEMPLATE_DIR, JINJA_REQUIREMENTS_TEMPLATE_DIR


def generate_requirements_code():
    jinja_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(JINJA_REQUIREMENTS_TEMPLATE_DIR),
        trim_blocks=True,
        lstrip_blocks=True)

    tmpl = jinja_env.get_template('requirements.template')
    with open(osp.join(OUTPUT_DIR, 'requirements.txt'), 'w') as f:
        f.write(tmpl.render())


def generate_data_code(data):

    jinja_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(JINJA_DATA_TEMPLATE_DIR),
        trim_blocks=True,
        lstrip_blocks=True)

    import_tmpl = jinja_env.get_template('imports.template')
    missing_values_tmpl = jinja_env.get_template('missing_values.template')
    outlier_removal_tmpl = jinja_env.get_template('outlier_removal.template')
    data_tmpl = jinja_env.get_template('data.template')

    outlier_methods = set()
    missing_values_methods = set()

    for data_node in data:
        outlier_methods.add(data_node.outlier)
        missing_values_methods.add(data_node.missing_values)

    with open(osp.join(OUTPUT_DIR, 'data_handler.py'), 'w') as f:
        f.write(import_tmpl.render())
        f.write('\n\n\n')
        if missing_values_methods:
            f.write(missing_values_tmpl.render(missing_values=missing_values_methods))
            f.write('\n\n\n')
        if outlier_methods:
            f.write(outlier_removal_tmpl.render(outliers=outlier_methods))
            f.write('\n\n\n')
        for d in data:
            f.write(data_tmpl.render(data=d))
            f.write('\n\n\n')


def generate_model_code(models):

    if not models:
        return

    jinja_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(JINJA_MODEL_TEMPLATE_DIR),
        trim_blocks=True,
        lstrip_blocks=True)

    import_tmpl = jinja_env.get_template('imports.template')
    base_model_tmpl = jinja_env.get_template('model.template')
    model_templates = set()

    for model_node in models:
        if model_node.type in SUPPORTED_MODELS:
            model_templates.add(
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


def generate_wrapper_code(wrappers):

    if not wrappers:
        return

    jinja_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(JINJA_MODEL_TEMPLATE_DIR),
        trim_blocks=True,
        lstrip_blocks=True)

    import_tmpl = jinja_env.get_template('imports.template')
    wrapper_tmpl = jinja_env.get_template('wrapper.template')

    # outputs for all wrappers
    outputs = set(map(lambda w: w.output, wrappers))

    with open(osp.join(OUTPUT_DIR, 'wrapper.py'), 'w') as f:
        f.write(import_tmpl.render())
        f.write('\n\n\n')
        f.write(wrapper_tmpl.render(outputs=outputs))


def generate_stacking_code(stacking_expressions):
    if not stacking_expressions:
        return

    jinja_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(JINJA_MODEL_TEMPLATE_DIR),
        trim_blocks=True,
        lstrip_blocks=True)

    import_tmpl = jinja_env.get_template('imports.template')
    stacking_tmpl = jinja_env.get_template('stacking.template')

    with open(osp.join(OUTPUT_DIR, 'stacking.py'), 'w') as f:
        f.write(import_tmpl.render())
        f.write('\n\n\n')
        f.write(stacking_tmpl.render())


def generate_run_conf_code(models, stackings, wrappers, train_confs, test_confs, data):
    if not (train_confs and (models or stackings)):
        return

    jinja_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(JINJA_RUN_TEMPLATE_DIR),
        trim_blocks=True,
        lstrip_blocks=True)

    import_tmpl = jinja_env.get_template('imports.template')
    train_tmpl = jinja_env.get_template('run.template')

    with open(osp.join(OUTPUT_DIR, 'run.py'), 'w') as f:
        f.write(import_tmpl.render())
        f.write('\n\n\n')
        f.write(train_tmpl.render(models=models, stackings=stackings, train_confs=train_confs,
                                  test_confs=test_confs, data=data, wrappers=wrappers))


def generate_code(data, models, wrappers, stackings, train_confs, test_confs):
    """
    Generates code from given meta model using Jinja templates
    :param test_confs:
    :param train_confs:
    :param stackings:
    :param wrappers:
    :param models:
    :param data:
    :return:
    """
    # Create the output folder
    if not osp.exists(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)

    generate_requirements_code()
    generate_data_code(data)
    generate_model_code(models)
    generate_wrapper_code(wrappers)
    generate_stacking_code(stackings)
    generate_run_conf_code(models, stackings, wrappers, train_confs, test_confs, data)
