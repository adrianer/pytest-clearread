import pytest
from _pytest.terminal import TerminalReporter


def pytest_addoption(parser):
    group = parser.getgroup("terminal reporting", "reporting", after="general")
    group._addoption(
        '--clear', action="store_true", dest="clear", default=False,
        help=(
            "make pytest reporting output more readable"
        )
    )


@pytest.mark.trylast
def pytest_configure(config):
    if hasattr(config, 'slaveinput'):
        return  # xdist slave, we are already active on the master
    if config.option.clear:
        # Get the standard terminal reporter plugin...
        standard_reporter = config.pluginmanager.getplugin('terminalreporter')
        clear_reporter = ClearTerminalReporter(standard_reporter)

        # ...and replace it with our own clearing reporter.
        config.pluginmanager.unregister(standard_reporter)
        config.pluginmanager.register(clear_reporter, 'terminalreporter')


@pytest.mark.tryfirst
def pytest_runtest_teardown(item, nextitem):
    # This fixes py.test writing stuff after the progress indication
    print('\n')


class ClearTerminalReporter(TerminalReporter):
    def __init__(self, reporter):
        TerminalReporter.__init__(self, reporter.config)
        self._tw = reporter._tw

    def pytest_runtest_logstart(self, nodeid, location):
        # ensure that the path is printed before the
        # 1st test of a module starts running
        if self.showlongtestinfo:
            line = self._locationline(nodeid, *location)
            self.write_sep("-", line, bold=True)
        elif self.showfspath:
            fsid = nodeid.split("::")[0]
            self.write_fspath_result(fsid, "")
