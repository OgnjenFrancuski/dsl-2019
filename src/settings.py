import os.path as osp


LANGUAGE_EXTENSION = 'lama'


BASE_DIR = osp.dirname(osp.dirname(osp.abspath(__file__)))
GRAMMAR_FILE_PATH = osp.join(BASE_DIR, 'src', 'grammar', 'grammar.tx')

OUTPUT_DIR = osp.join(BASE_DIR, 'output')

JINJA_TEMPLATE_DIR = osp.join(BASE_DIR, 'src', 'code_generator', 'templates')
JINJA_DATA_TEMPLATE_DIR = osp.join(JINJA_TEMPLATE_DIR, 'data')
JINJA_MODEL_TEMPLATE_DIR = osp.join(JINJA_TEMPLATE_DIR, 'model')
JINJA_RUN_TEMPLATE_DIR = osp.join(JINJA_TEMPLATE_DIR, 'run_configurations')
JINJA_REQUIREMENTS_TEMPLATE_DIR = osp.join(JINJA_TEMPLATE_DIR, 'requirements')

_SUPPORTED_MODELS = [
    {'template_name': 'naive_bayes',    'class_name': 'NaiveBayes'},
    {'template_name': 'random_forest',  'class_name': 'RandomForest'},
    {'template_name': 'svm',            'class_name': 'SVM'},
    {'template_name': 'xgboost',        'class_name': 'XGBoost'}
]
SUPPORTED_MODELS = {}
for m in _SUPPORTED_MODELS:
    SUPPORTED_MODELS[m['class_name']] = '{}.template'.format(m['template_name'])


