import numpy as np


def get_confusion_matrix(real, predicted, classes_number):
    """ Returns the confusion matrix

    :param real: array, actual numeric indices of classes in  target column
    :param predicted: predicted numeric indices of classes for target column
    :param classes_number:  total number of possible classes in target column

    :return: matrix - array of size (class_number x class_number) as misclassification table,
             rows represent ground truth and columns - predicted values
    """

    matrix = np.zeros((classes_number, classes_number), dtype=np.int32)
    r = np.array(real)
    p = np.array(predicted)

    for i in range(len(real)):
        if r[i] >= classes_number or p[i] >= classes_number:
            continue
        matrix[r[i], p[i]] += 1

    return matrix


def accuracy_confusion_binary(confusion_matrix):
    """
    Returns accuracy by confusion

    :param confusion_matrix: array of size *number of classes x number of classes* with
     misclassification labels where rows present ground truth labels and columns predicted results

    :return: accuracy, precision, recall, F1
    """
    positive_index = np.argmin(np.sum(confusion_matrix,axis=0))
    tp = confusion_matrix[positive_index, positive_index]
    fn = confusion_matrix[positive_index, 1-positive_index]
    tn = confusion_matrix[1-positive_index, 1-positive_index]
    fp = confusion_matrix[1-positive_index, positive_index]

    n0 = sum(sum(confusion_matrix))

    if n0 > 0:
        accuracy = float(tp + tn)/float(n0)
    else:
        accuracy = 0

    if (tp + fn) > 0:
        recall = float(tp)/float(tp + fn)
    else:
        recall = 0

    if (tp + fp) > 0:
        precision = float(tp)/float(tp + fp)
    else:
        precision = 0

    if (precision + recall) > 0:
        f1 = 2*(precision*recall)/(precision + recall)
    else:
        f1 = 0
    return accuracy, precision, recall, f1


def log_loss(probability, actual, positive_index):
    old_shape = actual.shape
    actual.shape = (actual.size,)
    actual_positive = np.equal(actual, positive_index)
    actual.shape = old_shape
    placeholder = np.zeros(probability.shape)
    placeholder[actual_positive, positive_index] = 1
    placeholder[np.logical_not(actual_positive), 1-positive_index] = 1
    logloss = -1 * np.sum(np.multiply(np.log(np.maximum(probability,10e-5)), placeholder))
    return logloss