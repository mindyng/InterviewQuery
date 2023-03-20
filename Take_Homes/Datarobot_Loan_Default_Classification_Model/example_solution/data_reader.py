from config import CONFIG
from pandas import read_csv, DataFrame
from pandas.io.common import EmptyDataError
import numpy
import warnings


def custom_strip(x):
    x = str.strip(x)
    if x in CONFIG["values_as_missing"]:
        return ""
    else:
        return x


def read_Nstr_from_Csv(namefile, length_segment=numpy.inf, iteration_number=0, selection_columns=None):
    """
    Reads specified number of rows from the csv file starting from selected position.
    Starting position is determined according to the parameter
    iteration_number and length_segment - in case some part of the part was uploaded on previous step.
    The initial shift also determined by the position of the header in the file

    :param namefile: path to  CSV file with data
    :param length_segment: number of rows to read on each step
    :param iteration_number:  number of previously completed reading steps

    :return: data list representing read rows
    """
    if selection_columns is None:
        try:
            data = read_csv(namefile, delimiter=',', skiprows=int(0),
                           nrows=int(2), header=0,
                           encoding='utf-8', skip_blank_lines=True, error_bad_lines=False,
                           skipinitialspace=False, dtype=str , na_values=None,
                           na_filter=False, keep_default_na=False, usecols=selection_columns,
                               engine='c', compression=None, low_memory=False,lineterminator='\n')
            selection_columns = list(range(len(data.columns)))
        except EmptyDataError:
            raise Exception('File is empty.')
        except Exception as e:
            raise Exception((str(e) + '. Invalid file.').replace("can't", "cannot"))
    converter_strip = {element: custom_strip for element in selection_columns}
    if not numpy.isfinite(length_segment):
        length_segment = numpy.iinfo(numpy.int64).max
    # Definition of reading parameters
    if length_segment is None:
        skip = 0
    else:
        skip = length_segment * iteration_number + int(iteration_number != 0) + 0

    if iteration_number == 0:
        rowHeader = 0
    else:
        rowHeader = None

    # Read data
    try:
        data = read_csv(namefile, delimiter=',', skiprows=int(skip),
                               nrows=int(length_segment), header=rowHeader,
                               encoding='utf-8', skip_blank_lines=True,  error_bad_lines=False,
                               skipinitialspace=False, na_values=None,
                               na_filter=False, keep_default_na=False, converters=converter_strip,
                               usecols=selection_columns,lineterminator='\n')

        data.columns = [custom_strip(element) for element in data.columns]
    except EmptyDataError:
        data = DataFrame()
    except Exception as e:
        raise Exception((str(e) + '. Invalid file.').replace("can't", "cannot"))

    nRow = data.shape[0]
    if nRow > length_segment:
        warnings.warn('Number of rows in file  is greater than allowed amount to load (' +
                      str(length_segment) + ') by memory restriction.')

    return data
