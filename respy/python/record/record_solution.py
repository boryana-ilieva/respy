import os


def record_solution_progress(indicator, period=None, num_states=None):

    if indicator == 1:
        if os.path.exists('sol.respy.log'):
            os.unlink('sol.respy.log')

        line = 'Starting state space creation'
    elif indicator == 2:
        line = 'Starting calculation of systematic payoffs'
    elif indicator == 3:
        line = 'Starting backward induction procedure'
    elif indicator == 4:
        string = '''{0[0]:>18}{0[1]:>3}{0[2]:>5}{0[3]:>6} {0[4]:>7}'''
        line = string.format(['... solving period', period, 'with', num_states, 'states'])
    elif indicator == -1:
        line = '... finished\n'
    elif indicator == -2:
        line = '... not required due to myopic agents'
    else:
        raise AssertionError

    with open('sol.respy.log', 'a') as outfile:
        outfile.write('  ' + line + '\n\n')


def record_prediction_model(results):
    """ Write out some basic information to the solutions log file.
    """

    with open('sol.respy.log', 'a') as outfile:
        outfile.write('    Information about Prediction Model')

        string = '      {:<19}' + '{:15.4f}' * 9
        outfile.write(string.format('Coefficients', *results.params))
        outfile.write(string.format('Standard Errors', *results.bse))

        string = '      {0:<19}{1:15.4f}\n'
        outfile.write(string.format('R-squared', results.rsquared))

