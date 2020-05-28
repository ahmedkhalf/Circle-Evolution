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
        report and have to deal with what to do with that. To accomodate with
        context, it also receives an status.
        """

    @abstractmethod
    def on_start(self, report):
        """Receives report for when the Subject start processing.

        If a reporter needs to report an object being initialized or starts
        processing, it can use this. Please note that ALL reporters need
        to implement this, if it is not used you can just `return` or `pass`
        """

    @abstractmethod
    def on_stop(self, report):
        """Receives report for when the Subject finishes processing.

        If a reporter needs to report an object that finished
        processing, it can use this. Please note that ALL reporters need
        to implement this, if it is not used you can just `return` or `pass`
        """


class LoggerMetricReporter(Reporter):
    """Reporter for logging.

    This Reporter is responsible for setting up a Logger object and logging all
    events that happened during circle-evolution cycle.
    """

    def setup(self):
        """Sets up Logger"""
        config_initial = {
            "version": 1,
            "disable_existing_loggers": True,
            "formatters": {"simple": {"format": "%(asctime)s %(name)s %(message)s", "datefmt": "%H:%M:%S"}},
            "handlers": {"console": {"level": "INFO", "class": "logging.StreamHandler", "formatter": "simple"}},
            "loggers": {"circle-evolution": {"handlers": ["console"], "level": "DEBUG"}},
            "root": {"handlers": ["console"], "level": "DEBUG"},
        }
        logging.config.dictConfig(config_initial)
        self.logger = logging.getLogger(__name__)  # Creating new logger
        self.last_fit = float("-inf")  # Value for fresh run

    def update(self, report):
        """Logs events using logger"""
        self.logger.debug("Received event...")

        # We are going to show the percentual improvement from last fit, but
        # because don't want to slow perfomance we remove having to calculate
        # really small values
        improvement = report.current_fitness - self.last_fit
        self.last_fit = report.current_fitness
        if improvement > 0.00001:
            improvement = improvement / self.last_fit * 100
        # Updating last_fit
        self.logger.info(
            "Generation %s - Fitness %.5f - Improvement %.5f%%", report.generation, report.current_fitness, improvement
        )

    def on_start(self, report):
        """Just logs the maximum generations"""

    def on_stop(self, report):
        """Just logs the final fitness"""
