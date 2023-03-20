import sklearn.linear_model
import numpy
import warnings


def logistic_regression_train(x, y, param_list={}):
    """
    Performs training using logistic regression

    :param x: numerically encoded input of size (number of samples x number of parameters)
    :param y: target column with actual class indices
    :param param_list: parameters of the logistic regression, if not provided default values are selected from here:|br|
                       http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html
    :return: sklearn classifier
    """
    supported_parameters = {'penalty', 'dual', 'tol', 'C', 'fit_intercept', 'intercept_scaling', 'class_weight',
                            'random_state', 'solver', 'max_iter', 'multi_class', 'verbose', 'warm_start', 'n_jobs'
                            }

    default_params = {'penalty': 'l2', 'dual': False, 'tol': 0.0001, 'C': 1.0, 'fit_intercept': True,
                      'intercept_scaling': 1, 'class_weight': None, 'random_state': None, 'solver': 'liblinear',
                      'max_iter': 100, 'multi_class': 'ovr', 'verbose': 0, 'warm_start': False, 'n_jobs': 1
                      }

    param_list_filtered = {key: param_list[key] for key in supported_parameters.intersection(param_list.keys())}
    param_list_missing = {key: default_params[key] for key in supported_parameters.difference(param_list.keys())}

    ignored = set(param_list.keys()).difference(supported_parameters)
    if len(ignored) > 0:
        warning_message = 'Parameters ' + str(ignored) +\
                          ' for method logisticRegression are not supported and will be ignored'
        warnings.warn(warning_message)

    param_list = dict(param_list_filtered, **param_list_missing)

    classifier = sklearn.linear_model.LogisticRegression(**param_list)

    if 2 > len(x.shape):
        x = x.reshape(1, -1)
    classifier.fit(x.values, y.values.ravel().astype(int))

    return classifier


def logistic_regression_predict(x, classifier, decimal_rounding=3):
    """
    Make predictions using trained classifier and returns results and score of prediction

    :param x: numerically encoded input of size (number of samples x number of parameters)
    :param classifier: classifier object
    :param decimal_rounding: int - decimal rounding parameter

    :return: tuple of results and score of prediction
    """
    if 2 > len(x.values.shape):
        x.values = x.values.reshape(1, -1)

    score = classifier.predict_proba(x)
    value = classifier.classes_[numpy.argmax(score, axis=1)]  # classifier.predict(X)
    score = numpy.around(score, decimals=decimal_rounding)

    return value, score
