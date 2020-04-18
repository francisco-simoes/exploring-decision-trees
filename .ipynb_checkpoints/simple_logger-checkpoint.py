import logging

# Specify format for the logging (as simple as possible, to mimic normal prints).
logging.basicConfig(level=logging.DEBUG, format='%(message)s')

# Create global logger. We will always use the same logger.
global logger
logger = logging.getLogger()
# Create global boolean which will record the previous state of the logger, so that we can revert back to it. 
global logger_bool_record
logger_bool_record = True

# The main function of this module is now defined. It basically acts as a printing function, the advantage being that you can deactivate the prints by disabling the logger.
def log(*args, separator=' ', logger=logger):
    '''
    Logs args into the console using logger, separating them by separator.
    A (global) logger must be defined externally.
    '''
    str_args = [str(arg) for arg in args]
    string = separator.join(str_args)
    logger.debug(string)

# We need a simple a function which activates or not the logger depending on its argument.
# This function will usually be called at the start of the function where we (may) want to use the logger.
def logger_switch(printing: bool):
    '''
    Disables the logger in printing = False. Enables it if printing = True.
    Records the original state of the logger in the global logger_bool_record.
    '''
    logger_bool_record = logger.disabled
    if printing:
        logger.disabled = False
    else:
        logger.disabled = True 

# Finally, we create a cleanup function, which returns the logger to the state it was in before running logger_switch.
# This is particularly important when we want to use the logger in nested functions, since its state in the inner function will affect its state in the outer function.
def logger_cleanup():
    '''
    Reverts the logger back to its original state, before logger_switch was called.
    '''
    logger.disabled = logger_bool_record

