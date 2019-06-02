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
    def __init__(self, parent, type, name, folds, params):
        self.parent = parent
        self.type = type
        self.name = name
        self.params = params
        self.folds = folds if folds > 1 else None


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
        self.input_models = input_models.collection
        self.output_model = output_model


class Train(object):
    """
    Class represents training configuration used in grammar
    """
    def __init__(self, parent, name, data, models, verbose, seed):
        self.parent = parent
        self.name = name
        self.data = data
        self.models = models.collection
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
        self.models = models.collection
        self.model_names = []


class List(object):
    """
    Class represents List rule used in grammar to represent collection
    of values
    """
    def __init__(self, parent, collection):
        self.parent = parent
        self.collection = collection


class Param(object):
    """
    Class represents Param rule used in grammar
    """
    def __init__(self, parent, name, value):
        self.parent = parent
        self.name = name
        self.inner_value = value


    @property
    def value(self):
        if isinstance(self.inner_value, List):
            return self.inner_value.collection
        return self.inner_value