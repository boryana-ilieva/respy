#!/usr/bin/env python
""" I will now try to run some estimations.
"""


# ROOT DIRECTORY
# standard library
import os
import sys

# ROOT DIRECTORY
from respy.python.estimate.estimate_auxiliary import dist_optim_paras

# project library
from respy.python.evaluate.evaluate_python import pyth_evaluate
from respy.fortran.f2py_library import f2py_evaluate

from respy.fortran.fortran import fort_evaluate
from respy.tests.codes.auxiliary import write_draws

from respy.python.evaluate.evaluate_auxiliary import check_input
from respy.python.evaluate.evaluate_auxiliary import check_output

from respy.python.shared.shared_auxiliary import dist_class_attributes
from respy.python.shared.shared_auxiliary import dist_model_paras
from respy.python.shared.shared_auxiliary import create_draws

from respy import simulate, solve, evaluate, estimate, RespyCls
import numpy as np
import pickle as pkl

respy_obj = RespyCls('model.respy.ini')

solve.solve(respy_obj)

respy_obj = pkl.load(open('solution.respy.pkl', 'rb'))

np.testing.assert_equal(respy_obj.get_attr('periods_emax')[0, 0], 157671.41881517219)


