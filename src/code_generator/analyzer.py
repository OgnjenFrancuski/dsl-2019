import numpy as np

from src.code_generator.meta_models import Model, Data, ModelWrapper, Stacking, Train, Test


def check_names(names):

    name2idx = {name: idx for idx, name in enumerate(np.unique(names))}
    idx2name = {idx: name for name, idx in name2idx.items()}

    name_idxs = list(map(lambda name: name2idx[name], names))

    y = np.bincount(name_idxs)
    ii = np.nonzero(y)[0]
    name_freq = list(map(lambda zi: (idx2name[zi[0]], zi[1]), list(zip(ii, y[ii]))))

    for nf in name_freq:
        if nf[1] > 1:
            return False, nf[0], nf[1]

    return True, None, None


def update_wrapper_references(models, wrappers):

    matrix = np.zeros((len(wrappers), len(models)))

    for wi, w in enumerate(wrappers):
        for mi, m in enumerate(models):
            if w.model == m.name:
                matrix[wi][mi] += 1

    for idx, el in enumerate(list(np.sum(matrix, axis=1))):
        if el < 1:
            raise Exception('ModelWrapper \'{}\' references undefined model \'{}\''
                            .format(wrappers[idx].name, wrappers[idx].model))

    for wi in range(0, matrix.shape[0]):
        for mi in range(0, matrix.shape[1]):
            if matrix[wi][mi] > 0:
                wrappers[wi].model = models[mi]


def update_stacking_references(models, stackings):
    matrix = np.zeros((len(stackings), len(models)))

    for si, s in enumerate(stackings):
        for mi, m in enumerate(models):
            if m.name in s.input_models:
                matrix[si][mi] += 1
            if m.name == s.output_model:
                s.output_model = m

    for si in range(0, matrix.shape[0]):
        stackings[si].input_models = []
        for mi in range(0, matrix.shape[1]):
            if matrix[si][mi] > 0:
                stackings[si].input_models.append(models[mi])
    print()


def update_train_references(data, models, stackings, train_configurations):
    models_matrix = np.zeros((len(train_configurations), len(models)))
    stackings_matrix = np.zeros((len(train_configurations), len(stackings)))

    for ti, t in enumerate(train_configurations):
        for si, s in enumerate(stackings):
            if s.name in t.models:
                stackings_matrix[ti][si] += 1
        for mi, m in enumerate(models):
            if m.name in t.models:
                models_matrix[ti][mi] += 1
        for d in data:
            if d.name == t.data:
                t.data = d

    for ti in range(models_matrix.shape[0]):
        train_configurations[ti].models = []
        for si in range(0, stackings_matrix.shape[1]):
            if stackings_matrix[ti][si] > 0:
                train_configurations[ti].models.append(stackings[si])
        for mi in range(0, models_matrix.shape[1]):
            if models_matrix[ti][mi] > 0:
                train_configurations[ti].models.append(models[mi])


def update_test_references(data, models, stackings, wrappers, test_configurations):
    models_matrix = np.zeros((len(test_configurations), len(models)))
    stackings_matrix = np.zeros((len(test_configurations), len(stackings)))
    wrappers_matrix = np.zeros((len(test_configurations), len(wrappers)))

    for ti, t in enumerate(test_configurations):
        for si, s in enumerate(stackings):
            if s.name in t.models:
                stackings_matrix[ti][si] += 1
                t.model_names.append(s.name)
        for mi, m in enumerate(models):
            if m.name in t.models:
                models_matrix[ti][mi] += 1
                t.model_names.append(m.name)
        for wi, w in enumerate(wrappers):
            if w.name in t.models:
                wrappers_matrix[ti][wi] += 1
                t.model_names.append(w.name)
        for d in data:
            if d.name == t.data:
                t.data = d

    for ti in range(models_matrix.shape[0]):
        test_configurations[ti].models = []
        for si in range(0, stackings_matrix.shape[1]):
            if stackings_matrix[ti][si] > 0:
                test_configurations[ti].models.append(stackings[si])
        for mi in range(0, models_matrix.shape[1]):
            if models_matrix[ti][mi] > 0:
                test_configurations[ti].models.append(models[mi])
        for wi in range(0, wrappers_matrix.shape[1]):
            if models_matrix[ti][wi] > 0:
                test_configurations[ti].models.append(wrappers[wi])

def analyze_code(grammar_model):

    names = []
    names.extend(list(map(lambda p: p.name, grammar_model.data_expressions)))
    names.extend(list(map(lambda p: p.name, grammar_model.model_expressions)))
    names.extend(list(map(lambda p: p.name, grammar_model.run_expressions)))

    passed, object_name, times = check_names(names)
    if not passed:
        raise Exception('Object with name \'{}\' is defined more than once ({} times)'
                        .format(object_name, times))

    for gm in grammar_model.model_expressions:
        if isinstance(gm, Model):
            param_names = list(map(lambda p: p.name, gm.params))
            passed, object_name, times = check_names(param_names)
            if not passed:
                raise Exception('Param with name \'{}\' is defined more than once ({} times) in '
                                'model / model wrapper with name \'{}\''
                                .format(object_name, times, gm.name))

        elif isinstance(gm, Train):
            pass


def update_references(grammar_model):

    data = []
    models = []
    wrappers = []
    stackings = []
    train_confs = []
    test_confs = []

    for gm in grammar_model.data_expressions:
        data.append(gm)

    for gm in grammar_model.model_expressions:
        if isinstance(gm, Model):
            models.append(gm)
        if isinstance(gm, ModelWrapper):
            wrappers.append(gm)
        if isinstance(gm, Stacking):
            stackings.append(gm)

    for gm in grammar_model.run_expressions:
        if isinstance(gm, Train):
            train_confs.append(gm)
        if isinstance(gm, Test):
            test_confs.append(gm)

    update_wrapper_references(models, wrappers)
    update_stacking_references(models, stackings)
    update_train_references(data, models, stackings, train_confs)
    update_test_references(data, models, stackings, wrappers, test_confs)
    return data, models, wrappers, stackings, train_confs, test_confs
