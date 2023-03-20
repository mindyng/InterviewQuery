import numpy as np
from sklearn.ensemble import ExtraTreesClassifier


def get_tree_importance(X, y, counting_dictionary, encoders, average=True):
    """
    Returns the tree importances

    :param X: Data matrix
    :param y: Goal values vector
    :param counting_dictionary: dictioanry storing the counts of each label entrance
    :return: list of tree importance
    """
    _ncols = X.shape[1]
    labels = ["" for i in range(_ncols)]
    for _key, (_st, _len) in counting_dictionary.items():
        for _p in range(_len):
            if average or _key not in encoders["label"]:
                labels[_st + _p] = _key
            else:
                labels[_st + _p] = _key + '_' + str(encoders["label"][_key].classes_[_p])

    forest = ExtraTreesClassifier(n_estimators=250,
                                  random_state=0)

    forest.fit(X, y)
    importances = forest.feature_importances_
    indices = np.argsort(importances)[::-1]
    dict_res = {}
    for i in indices:
        dict_res.setdefault(labels[i], 0)
        dict_res[labels[i]] += importances[i]

    res = sorted(list(dict_res.items()), key = lambda x : -x[1])
    return res
