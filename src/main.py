from textx import metamodel_from_file

if __name__ == '__main__':
    robot_mm = metamodel_from_file('grammar/grammar.tx')
    robot_model = robot_mm.model_from_file('grammar/grammar_test.rbt')
