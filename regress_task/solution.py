import os

import numpy as np
import statsmodels.api as sm

from preparation import prepare_data


def solution(prepared_data):
    """
    solution of task
    if test data is None put train_data into test_data
    :param prepared_data: train data with structure
            which determined in preparation file
    :param degree: number of max polynomial degree
    :param test_data: test data with structure like prepared_data
    :return: regress coefficients and r_square
    """
    matrix = prepared_data['parameters']
    y = prepared_data['connections']

    sparse_matrix = [[0] * len(matrix)] * len(matrix[0])
    for i in xrange(len(matrix)):
        for j in xrange(len(matrix[0])):
            sparse_matrix[j][i] = matrix[i][j]
    ones = np.ones(len(sparse_matrix[0]))
    X = sm.add_constant(np.column_stack((sparse_matrix[0], ones)))
    for ele in sparse_matrix[1:]:
        X = sm.add_constant(np.column_stack((ele, X)))

    regression = sm.OLS(y, X).fit()
    print regression.summary()

def main():
    """
    connection_paths - path from DATA directory with connections of students
                    if you want to add year just add file to directory
                    and write name of file to this list
    paths - files with parameters if you want to add parameter
            just add file to DATA directory and write name to this tuple

    IMPORTANT
    test_data in prepare_reply (red color): change value of this parameter
    from data to your real test data
    P.S. do not forget to make prepare_data for test data too.

    :return: reply
    """
    connection_paths = ('s50-network1.dat', 's50-network2.dat',
                        's50-network3.dat')
    connections_filenames = [os.path.join('DATA', path)
                             for path in connection_paths]
    paths = (
        's50-alcohol.dat', 's50-drugs.dat', 's50-smoke.dat', 's50-sport.dat'
    )
    paths_to_parameters = [os.path.join('DATA', path) for path in paths]

    data_array = []
    for i in xrange(len(connection_paths)):
        data_array.append(prepare_data(connections_filenames[i],
                                       paths_to_parameters, year_index=i + 1))
        print 'index of year: {}'.format(i + 1)
        solution(data_array[i])
        print '\n' * 5

if __name__ == '__main__':
    main()
