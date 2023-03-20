import numpy as np
from os import remove
from os.path import isfile


def clean_files(files_structure):
    for file_name in (files_structure['train_files'] + files_structure['validation_files']):
        if isfile(file_name):
            try:
                remove(file_name)
            except Exception as e:
                print('Fail to remove file "' + file_name + '".')

def check_extra_values(columndata, encoder):
    """
    Checks if there are extra values in column

    :param columndata: column data as numpy array
    :param encoder: encoder for this column
    :return: (no_extra_flag, true_index_array)
    """
    encoded_values = encoder.classes_
    column_values = np.unique(columndata)
    new_values = set(column_values).difference(encoded_values)
    no_extra_flag = len(new_values) <= 0
    if not no_extra_flag:
        true_index_array = np.asarray([x in encoded_values for x in columndata])
    else:
        true_index_array = np.empty((columndata.shape[0],),dtype=bool)
        true_index_array.fill(True)
    return no_extra_flag, true_index_array


def normalize_numeric(column_data, column_description):
    """
    Normalize numeric column substracting its mean and dividing the result by standard deviation

    :param column_data: Column numeric vector
    :param column_description: Dictionary with column description

    :return: Modified column
    """
    mean = float(column_description['mean'])
    std = float(column_description["std"])
    column_data = column_data - mean
    if std > 10e-6:
        column_data = column_data / std
    return column_data
