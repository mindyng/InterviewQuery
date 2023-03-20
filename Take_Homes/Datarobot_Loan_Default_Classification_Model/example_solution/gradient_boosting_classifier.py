import sklearn.ensemble
import numpy
import warnings


def gradient_boosting_classifier_train(x, y, param_list={}):
    """
    Performs training using GradientBoostingClassfier()

    :param x: numerically encoded input of size (number of samples x number of parameters)
    :param y: target column with actual class indices
    :param param_list: parameters of the gradient boosting classification, if not provided default values are selected from here:|br|
                       https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.GradientBoostingClassifier.html
    :return: sklearn classifier
    """
    supported_parameters = {'loss', 'learning_rate', 'n_estimators', 'subsample', 'criterion',
                            'min_samples_split', 'min_samples_leaf', 'min_weight_fraction_leaf', 'max_depth',
                            'min_impurity_decrease', 'min_impurity_split',
                            'init', 'random_state', 'max_features', 'verbose', 'max_leaf_nodes',
                            'warm_start', 'presort'
                            }

    default_params = {'loss': 'deviance', 'learning_rate': 0.1, 'n_estimators': 100,
                      'subsample': 1.0, 'criterion': 'friedman_mse',
                      'min_samples_split': 2, 'min_samples_leaf': 1, 'min_weight_fraction_leaf': 0.0,
                      'max_depth': 3, 'min_impurity_decrease': 0.0, 'min_impurity_split': None,
                      'init': None, 'random_state': None, 'max_features': None, 'verbose': 0, 'max_leaf_nodes': None,
                      'warm_start': False, 'presort': 'auto'
                      }

    param_list_filtered = {key: param_list[key] for key in supported_parameters.intersection(param_list.keys())}
    param_list_missing = {key: default_params[key] for key in supported_parameters.difference(param_list.keys())}

    ignored = set(param_list.keys()).difference(supported_parameters)
    if len(ignored) > 0:
        warning_message = 'Parameters ' + str(ignored) +\
                          ' for method GradientBoostingGlassifier are not supported and will be ignored'
        warnings.warn(warning_message)

    param_list = dict(param_list_filtered, **param_list_missing)

    classifier = sklearn.ensemble.GradientBoostingClassifier(**param_list)

    if 2 > len(x.shape):
        x = x.reshape(1, -1)
    classifier.fit(x.values, y.values.ravel().astype(int))

    return classifier


def gradient_boosting_classifier_predict(x, classifier, decimal_rounding=3):
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
