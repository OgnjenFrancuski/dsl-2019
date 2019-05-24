class Data(object):
    """
    Class represents rule Data used in grammar
    """
    def __init__(self, parent,
                 name, path, label_column, test_size, validation_size,
                 missing_values, normalization, outlier):
        self.parent = parent
        self.name = name
        self.path = path
        self.label_column = label_column
        self.test_size = test_size
        self.validation_size = validation_size
        self.missing_values = missing_values
        self.normalization = normalization
        self.outlier = outlier


class Model(object):
    """
    Class represent rule model used in grammar
    """
    def __init__(self, parent, type, name, cv_folds, params):
        self.parent = parent
        self.type = type
        self.name = name
        self.params = params
        self.cv_folds = cv_folds if cv_folds > 1 else None


class ModelWrapper(object):
    """
    Class represents model wrapper used in grammar
    """
    def __init__(self, parent, name, model, input_size, output='voting'):
        self.parent = parent
        self.name = name
        self.model = model
        self.input_size = input_size
        self.output = output


class Stacking(object):
    pass


class Train(object):
    pass


class Test(object):
    pass

