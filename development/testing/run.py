#!/usr/bin/env python
""" Script to start development test battery for the ROBUPY package.
"""

# standard library
from datetime import timedelta
from datetime import datetime

import numpy as np

import traceback
import importlib
import argparse
import random
import time
import sys
import os

# virtual environment
if not hasattr(sys, 'real_prefix'):
    raise AssertionError('Please use a virtual environment for testing')

# ROBPUPY testing codes. The import of the PYTEST configuration file ensures
# that the PYTHONPATH is modified to allow for the use of the tests..
TEST_DIR = os.path.dirname(os.path.realpath(__file__))
TEST_DIR = TEST_DIR.replace('development/testing', '') + 'robupy/tests'

sys.path.insert(0, TEST_DIR)
import conftest

# Setup for dealing with PYTEST command line options
import functools
import inspect

VERSIONS = ['PYTHON', 'FORTRAN', 'F2PY']

# Testing infrastructure
from modules.auxiliary import cleanup_testing_infrastructure
from modules.auxiliary import get_random_request
from modules.auxiliary import distribute_input
from modules.auxiliary import get_test_dict

from modules.auxiliary import finalize_testing_record
from modules.auxiliary import update_testing_record
from modules.auxiliary import send_notification
from modules.auxiliary import compile_package

''' Main Function.
'''
import string

def randomword(length):
   return ''.join(random.choice(string.ascii_lowercase) for i in range(
 length))



def run(hours, compile):
    """ Run test battery.
    """
    # Compile the debug version of the ROBUPY program.
    if compile:
        compile_package()

    # Get a dictionary with all candidate test cases.
    test_dict = get_test_dict(TEST_DIR)

    # We initialize a dictionary that allows to keep track of each test's
    # success or failure.
    full_test_record = dict()
    for key_ in test_dict.keys():
        full_test_record[key_] = dict()
        for value in test_dict[key_]:
            full_test_record[key_][value] = [0, 0]

    # Start with a clean slate.
    cleanup_testing_infrastructure(False)

    start, timeout = datetime.now(), timedelta(hours=hours)

    # # Evaluation loop.

    while True:

        # Set seed.
        seed = random.randrange(1, 100000)
        np.random.seed(seed)

        # Construct test case.
        module, method = get_random_request(test_dict)
        mod = importlib.import_module(module)
        test = getattr(mod.TestClass(), method)

        # Deal with PYTEST command line options.
        if 'versions' in inspect.getargspec(test)[0]:
            test = functools.partial(test, VERSIONS)

        # Run random tes
        is_success, msg = None, None

        # Create a fresh test directory.
        tmp_dir = randomword(5)

        os.mkdir(tmp_dir)
        os.chdir(tmp_dir)

        try:
            test()
            full_test_record[module][method][0] += 1
            is_success = True
        except Exception:
            full_test_record[module][method][1] += 1
            msg = traceback.format_exc()
            is_success = False

        # The directory is deleted by the cleanup
        os.chdir('../')

        # Record iteration
        update_testing_record(module, method, seed, is_success, msg,
                              full_test_record, start, timeout)


        if seed == 20920:
            import sys
            sys.exit('problemn again')
        cleanup_testing_infrastructure(True)


        #  Timeout.
        if timeout < datetime.now() - start:
            break

    finalize_testing_record()

''' Execution of module as script.
'''
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run development test '
                'battery of ROBUPY package.',
                formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--hours', action='store', dest='hours',
                        type=float, default=1.0, help='run time in hours')

    parser.add_argument('--notification', action='store_true',
                        dest='notification', default=False,
                        help='send notification')

    parser.add_argument('--compile', action='store_true',
                        dest='compile', default=False,
                        help='compile toolbox with debug flag')

    # Start from a clean slate and extract a user's request.
    cleanup_testing_infrastructure(False)
    hours, notification, compile = distribute_input(parser)

    # Run testing infrastructure and send a notification (if requested).
    run(hours, compile)

    if notification:
        send_notification(hours)
