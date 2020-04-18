import logging

# Specify format for the logging (as simple as possible, to mimic normal prints).
logging.basicConfig(level=logging.DEBUG, format='%(message)s')


# The following function will be used to construct a log (printing) function which utilizes a specific logger from the Logger class of the logging module.
def make_log(*args, separator=' ', logger):
    '''
    Logs args into the console using logger, separating them by separator.
    A (global) logger must be defined externally.
    '''
    str_args = [str(arg) for arg in args]
    string = separator.join(str_args)
    logger.debug(string)
    return

# We now want function decorator which will create a local logger and switch it on or off as desired, reverting the logger to its original state after calling the function to decorate.
# This allows logging in nested function smoothly.
def with_logger(printing: bool, func, *args, **kargs):
    '''
    Function decorator creating a local logger and switching it on if printing = True and off otherwise.
    func must have an arg log at the first position, which we will set equal to a function log_func created locally.
    *args and **kargs can contain all the arguments of func.
    ----
    Example:
    > def f(log, x): 
        log('x is {}'.format(x))
        return x**2
    > def f_with_logging(x, debug_prints=False):
        return with_logger(f, x, printing=debug_prints)
    > f_with_logging(3, True)
        > 'x is 3'
        Out: 9
    > f_with_logging(3)
        Out: 9
    '''
    # Create logger variable, and switch it on/off
    logger = logging.getLogger()
    # The name logger will always refer to the same (root) logger object, so other functions will use the same (root) logger
    # So we store the original logger state to restore it afterwards
    logger_og_state = logger.disabled
    if printing:
        logger.disabled = False
    else:
        logger.disabled = True 
    # Now that a logger exists, we can define a log function to use in the function to decorate
    log_func = lambda *args_: make_log(*args_, separator=' ', logger=logger)
    # Run function to decorate
    args = (log_func,) + args # Adds log_func to beginning of args
    result = func(*args, **kargs)
    #result = func(*args, **kargs, log=log_func)
    # Restore logger state
    logger.disabled = logger_og_state
    return result
