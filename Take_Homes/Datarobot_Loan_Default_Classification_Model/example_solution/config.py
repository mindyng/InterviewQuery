"""
The shared configuration file.
"""

CONFIG = {'round_float_digits': 2,
          'values_as_missing':["", "#N/A", "#N/A N/A", "#NA", "-1.#IND", "-1.#QNAN", "-NaN",
                               "-nan","NAN","-NAN", "1.#IND", "1.#QNAN", "N/A", "NA","-NA",
                               "NULL","NaN", "nan","na","Na","-na","-Na""Inf","inf","-Inf",
                               "-inf"],
          'remove_columns': ['Id','purpose','Notes','initial_list_status','pymnt_plan','collections_12_mths_ex_med'],
          'target_column': 'is_bad',
          'k_fold_k': 5,
          'hold_out_train_size': 0.9,
          'supported_algorithms': ['logistic_regression', 'gradient_boosting_classifier']
          }