"""Base Class for Reported Objects.

If you want to receive reports about any objects in Circle-Evolution you just
need to extend your class with the base Runner. It provides an interface for
attaching reporters and notifying all reporters of a particular event.
"""
# Constants for Runners
START = 0
PROCESSING = 1
END = 2


class Runner:
    """Base Runner class.

    The Runner class is responsible for managing reporters and sending events
    to them. If you need to receive updates by a particular reporter you just
    need to use this base class.

    Attributes:
        _reporters: list of reporters that are going to receive reports.
    """

    _reporters = []

    def attach(self, reporter):
        """Attaches reporter for notifications"""
        self._reporters.append(reporter)

    def notify(self, report, status=PROCESSING):
        """Send report to all attached reporters"""
        if status == START:
            for reporter in self._reporters:
                reporter.on_start(report)
        elif status == END:
            for reporter in self._reporters:
                reporter.on_stop(report)
        elif status == PROCESSING:
            for reporter in self._reporters:
                reporter.update(report)
