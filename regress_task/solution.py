import os

from pprint import pprint
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline

from preparation import prepare_data


def solution(prepared_data, degree=1, test_data=None):
    """
    solution of task
    if test data is None put train_data into test_data
    :param prepared_data: train data with structure
            which determined in preparation file
    :param degree: number of max polynomial degree
    :param test_data: test data with structure like prepared_data
    :return: regress coefficients and r_square
    """
    sparse_matrix = prepared_data['parameters']
    y = prepared_data['connections']
    model = Pipeline([('poly', PolynomialFeatures(degree=degree)),
                      ('linear', LinearRegression(fit_intercept=False))])
    model = model.fit(sparse_matrix, y)
    regress_coef = model.named_steps['linear'].coef_

    regression = LinearRegression()
    if test_data is None:
        regression.fit(sparse_matrix, y)
        r_square = regression.score(sparse_matrix, y)
    else:
        if not isinstance(test_data, dict) or 'connections' not in test_data \
                or 'parameters' not in test_data:
            raise BaseException('put correct data into test_data')
        regression.fit(sparse_matrix, y)
        r_square = regression.score(test_data['parameters'],
                                    test_data['connections'])
    return regress_coef, r_square


def prepare_reply(parameters_paths, prepared_data, test_data,
                  degree=1, index_year=1):
    """
    print
    :param parameters_paths:
    :param prepared_data:
    :param test_data:
    :param degree:
    :param index_year:
    :return:
    """
    regress_coef, r_square = solution(prepared_data, degree, test_data)
    reply = {path.split('.')[0][4:]: regress_coef[i]
             for i, path in enumerate(parameters_paths)}
    print 'Index of year: {}'.format(index_year)
    print 'R^2: {}'.format(r_square)
    print 'Coefficients: '
    pprint(reply)
    print


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
        's50-alcohol.dat', 's50-drugs.dat',
        's50-familyevent.dat', 's50-smoke.dat', 's50-sport.dat'
    )
    paths_to_parameters = [os.path.join('DATA', path) for path in paths]
    for i in xrange(len(connection_paths)):
        data = prepare_data(connections_filenames[i], paths_to_parameters,
                            year_index=i + 1)
        prepare_reply(paths, data, test_data=data, degree=1, index_year=i + 1)


if __name__ == '__main__':
    main()
