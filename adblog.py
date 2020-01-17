import logging

# # create logger
# logger = logging.getLogger('simple_example')
# logger.setLevel(logging.DEBUG)
#
# # create console handler and set level to debug
# ch = logging.StreamHandler()
# ch.setLevel(logging.DEBUG)
#
# # create formatter
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#
# # add formatter to ch
# ch.setFormatter(formatter)
#
# # add ch to logger
# logger.addHandler(ch)


class AdbLog:
    debug_level = logging.DEBUG
    ch = logging.StreamHandler()
    ch_debug_level = logging.DEBUG
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    @classmethod
    def get_logger(cls, logfile_name):
        logger = logging.getLogger(logfile_name)
        logger.setLevel(cls.debug_level)
        cls.ch.setLevel(cls.ch_debug_level)
        cls.ch.setFormatter(cls.formatter)
        logger.addHandler(cls.ch)
        return logger

    @classmethod
    def set_debug_level(cls, level):
        return cls.setLevel(level)

    @classmethod
    def set_stream_debug_level(cls, level):
        return cls.ch.setLevel(level)

    @classmethod
    def set_log_format(cls, formatter):
        cls.ch.setFormatter(formatter)
