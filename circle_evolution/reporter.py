"""Reporters for capturing events and notifying the user about them.

You can make your own Reporter class or use the already implemented one's.
Notice the abstract class before implementing your Reporter to see which
functions should be implemented.
"""
from abc import ABC, abstractmethod

import logging
import logging.config


class Reporter(ABC):
    """Base Reporter class.

    The Reporter is responsible for capturing particular events and sending
    them for visualization. Please, use this class if you want to implement
    your own Reporter.
    """

    def __init__(self):
        """Initialization calls setup to configure Reporter"""
        self.setup()

    def setup(self):
        """Function for configuring the reporter.

        Some reporters may need configuring some internal parameters or even
        creating objects to warmup. This function deals with this
        """

    @abstractmethod
    def update(self, report):
        """Receives report from subject.

        This is the main function for reporting events. The Reporter receives a
        report and have to deal with what to do with that. For Circle-Evolution
        you can expect anything from strings to `numpy.array`.
        """


class LoggerReporter(Reporter):
    """Reporter for logging.

    This Reporter is responsible for setting up a Logger object and logging all
    events that happened during circle-evolution cycle. Notice that this
    reporter only cares about strings and will notify minimal details about
    other types.
    """

    def setup(self):
        """Sets up Logger"""
        config_initial = {
            "version": 1,
            "disable_existing_loggers": True,
            "formatters": {"simple": {"format": "%(asctime)s %(name)s %(message)s"}},
            "handlers": {"console": {"level": "INFO", "class": "logging.StreamHandler", "formatter": "simple"}},
            "loggers": {"circle-evolution": {"handlers": ["console"], "level": "DEBUG"}},
            "root": {"handlers": ["console"], "level": "DEBUG"},
        }
        logging.config.dictConfig(config_initial)
        self.logger = logging.getLogger(__name__)  # Creating new logger

    def update(self, report):
        """Logs events using logger"""
        self.logger.debug("Received event...")
        if isinstance(report, str):
            # Only deals with string messages
            self.logger.info(report)
