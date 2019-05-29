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
    """
    Class represents stacking used in grammar
    """
    def __init__(self, parent, name, input_models, output_model):
        self.parent = parent
        self.type = 'ModelStacking'
        self.name = name
        self.input_models = input_models.num
        self.output_model = output_model


class Train(object):
    """
    Class represents training configuration used in grammar
    """
    def __init__(self, parent, name, data, models, verbose=2, seed=14):
        self.parent = parent
        self.name = name
        self.data = data
        self.models = models.num
        self.verbose = verbose
        self.seed = seed


class Test(object):
    """
    Class represents testing configuration used in grammar
    """
    def __init__(self, parent, name, data, models):
        self.parent = parent
        self.name = name
        self.data = data
        self.models = models.num
        self.model_names = []
