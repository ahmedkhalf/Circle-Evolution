"""Reporters for capturing events and notifying the user about them.

You can make your own Reporter class or use the already implemented one's.
Notice the abstract class before implementing your Reporter to see which
functions should be implemented.
"""
from abc import ABC, abstractmethod

import csv

from datetime import datetime

import logging
import logging.config

import tempfile


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
            "formatters": {
                "simple": {"format": "Circle-Evolution %(message)s"},
                "complete": {"format": "%(asctime)s %(name)s %(message)s", "datefmt": "%H:%M:%S"},
            },
            "handlers": {
                "console": {"level": "INFO", "class": "logging.StreamHandler", "formatter": "simple"},
                "file": {
                    "level": "DEBUG",
                    "class": "logging.FileHandler",
                    "filename": f"{tempfile.gettempdir()}/circle_evolution.log",
                    "mode": "w",
                    "formatter": "complete",
                },
            },
            "loggers": {"circle-evolution": {"handlers": ["console", "file"], "level": "DEBUG"}},
            "root": {"handlers": ["console", "file"], "level": "DEBUG"},
        }
        logging.config.dictConfig(config_initial)
        self.logger = logging.getLogger(__name__)  # Creating new logger

    def update(self, report):
        """Logs events using logger"""
        self.logger.debug("Received event...")

        improvement = report.new_fit - report.best_fit
        message = f"\tGeneration {report.generation} - Fitness {report.new_fit:.5f}"

        if improvement > 0:
            improvement = improvement / report.best_fit * 100
            message += f" - Improvement {improvement:.5f}%%"
            self.logger.info(message)
        else:
            message += " - No Improvement"
            self.logger.debug(message)

    def on_start(self, report):
        """Just logs the maximum generations"""
        self.logger.info("Starting evolution...")

    def on_stop(self, report):
        """Just logs the final fitness"""
        self.logger.info("Evolution ended! Enjoy your Circle-Evolved Image!\t" f"Final fitness: {report.best_fit:.5f}")


class CSVMetricReporter(Reporter):
    """CSV Report for Data Analysis.

    In case one wants to extract evolution metrics for a CSV file.
    """

    def setup(self):
        """Sets up Logger"""
        now = datetime.now()
        self.filename = f"circle-evolution-{now.strftime('%d-%m-%Y_%H-%M-%S')}.csv"
        self._write_to_csv(["generation", "fitness"])  # header

    def _write_to_csv(self, content):
        """Safely writes content to CSV file."""
        with open(self.filename, "a") as fd:
            writer = csv.writer(fd)
            writer.writerow(content)

    def update(self, report):
        """Logs events using logger"""
        self._write_to_csv([report.generation, report.new_fit])

    def on_start(self, report):
        # Nothing to do here
        pass

    def on_stop(self, report):
        # Nothing to do here
        pass
