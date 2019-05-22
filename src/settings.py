import os.path as osp


LANGUAGE_EXTENSION = 'lama'

BASE_DIR = osp.dirname(osp.dirname(osp.abspath(__file__)))
GRAMMAR_FILE_PATH = osp.join(BASE_DIR, 'src', 'grammar', 'grammar.tx')

JINJA_TEMPLATE_DIR = osp.join(BASE_DIR, 'src', 'code_generator', 'templates')
JINJA_DATA_TEMPLATE_DIR = osp.join(JINJA_TEMPLATE_DIR, 'data')

OUTPUT_DIR = osp.join(BASE_DIR, 'output')

