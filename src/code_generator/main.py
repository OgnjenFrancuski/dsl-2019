from textx import metamodel_from_file

from src.code_generator.analyzer import analyze_code, update_references
from src.code_generator.code_generator import generate_code
from src.code_generator.meta_models import Data, Model, ModelWrapper, Stacking, Test, Train, List, Param
from src.settings import GRAMMAR_FILE_PATH


def get_meta_model():
    """
    Builds and returns a meta-model for language.
    """
    mm = metamodel_from_file(file_name=GRAMMAR_FILE_PATH,
                             classes=[Data, ModelWrapper, Model,
                                      Stacking, Train, Test, List, Param])
    return mm


def main(file_path):

    # Instantiate the Entity meta-model
    mm = get_meta_model()

    # Build a model from file
    model = mm.model_from_file(file_path)

    # Analyze code and update references
    analyze_code(model)
    data, models, wrappers, stackings, train_confs, test_confs = update_references(model)

    # # Generate Python code
    generate_code(data, models, wrappers, stackings, train_confs, test_confs)


if __name__ == "__main__":
    # main('/home/milos/PycharmProjects/fax/dsl-2019/src/grammar/grammar_test.rbt')
    main(r'D:\Fax\DSL\dsl-2019\src\grammar\grammar_test.rbt')
    # main('/home/ognjen/Projects/Fax/DSL/dsl-2019/src/grammar/grammar_test.rbt')
