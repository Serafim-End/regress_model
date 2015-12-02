import re
import os


def check_correct_path(filename):
    """
    check whether file exists
    :param filename: file to check
    :return: True if exists and else otherwise
    """
    if not os.path.isfile(filename):
        raise BaseException('Stupid girl, please enter correct path')


def line_preparation(line):
    """
    :param line: changing line
    :return: line without transitions to new line
    """
    line = re.sub('\n', '', line)
    line = re.sub('\r', '', line)
    return [item for item in line.split(' ') if item != '']


def read_parameters(filename, years=3):
    """
    :param years: number of years
    :param filename: path to parameters
    :return: dictionary with all parameters
    {
        1: [all parameters]
        2: [all ...]
        3: [...]
    }
    where 1, 2, 3 - years (1997, ...)
    """
    check_correct_path(filename)
    parameter_dict = {i + 1: [] for i, year in enumerate(xrange(years))}
    for line in open(filename, 'r'):
        parameters = line_preparation(line)
        for i, item in enumerate(parameters):
            parameter_dict[i + 1].append(item)
    return parameter_dict


def read_connections(filename):
    """
    [[connections of first student], [connections of second student], ...]
    :param filename: path to connections file
    :return: list of lists with connections
    """
    check_correct_path(filename)
    connections = []
    for line in open(filename, 'r'):
        parameters = line_preparation(line)
        connections.append(parameters)
    return connections


def prepare_values(*args):
    """
    convert values to integer type
    :param args: arguments to convert
    :return: list of integer values
    """
    try:
        return [float(arg) for arg in args]
    except TypeError:
        raise TypeError('disgusting data')


def prepare_function(value_a, value_b):
    """
    it is really obvious function
    :param value_a: value of first parameter
    :param value_b: value of second parameter
    :return: parameter_function
    """
    value_a, value_b = prepare_values(value_a, value_b)
    if value_a == value_b:
        return 1
    elif abs(value_a - value_b) == 1:
        return 0.5
    else:
        return 0


def prepare_data(connections_filename, paths_to_parameters, year_index=1):
    """
    :param connections_filename: connection filename contain only one year data
    :param paths_to_parameters: list of path to parameters
    :param year_index: exists because parameters file consist
            from all years parameters
    :return: dictionary with structure like this
    {
        'connections': [1, 0, 2, ...]
        ':parameters': [[1, 0.5, 0, ...], [0.5, 1, 0, ...], ...]
    }

    length of connections list equals length of parameters list
    """
    connections = read_connections(connections_filename)
    parameters = [read_parameters(path) for path in paths_to_parameters]
    user_connections = {'connections': [], 'parameters': []}
    for i in xrange(len(connections) - 1):
        for j in xrange(i + 1, len(connections)):
            if prepare_values(connections[i][j])[0] == float(1) \
                    or prepare_values(connections[j][i])[0] == float(1):
                user_connections['connections'].append(1)
            else:
                user_connections['connections'].append(0)
            paramters_functions = []
            for parameter in parameters:
                if len(parameter[year_index]) < 1:
                    continue
                paramters_functions.append(
                    prepare_function(parameter[year_index][i],
                                     parameter[year_index][j])
                )
            user_connections['parameters'].append(paramters_functions)
    return user_connections
