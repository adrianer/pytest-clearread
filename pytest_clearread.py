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


def pytest_collection_modifyitems(config, items):
    for item in items:
        node = item.obj
        parent = item.parent.obj
        function_comment = node.__doc__ or ''
        class_comment = parent.__doc__ or ''
        item._nodeid = f"{item.nodeid};;;;;{class_comment};;;;;{function_comment}"


# @pytest.mark.tryfirst
# def pytest_runtest_teardown(item, nextitem):
#     # This fixes py.test writing stuff after the progress indication
#     print('\n')


class ClearTerminalReporter(TerminalReporter):
    def __init__(self, reporter):
        TerminalReporter.__init__(self, reporter.config)
        self._tw = reporter._tw

    def pytest_runtest_logstart(self, nodeid, location):
        # ensure that the path is printed before the
        # 1st test of a module starts running
        real_node_id = nodeid.split(";;;;;")[0]
        if len(nodeid.split(";;;;;")) > 1:
            function_comment = nodeid.split(";;;;;")[-1]
        else:
            function_comment = None
        if len(nodeid.split(";;;;;")) > 2:
            class_comment = nodeid.split(";;;;;")[-2]
        else:
            class_comment = None
        if self.showlongtestinfo:
            line = self._locationline(real_node_id, *location)
            self.write_sep("-", line, bold=True)
            if class_comment:
                self.write(class_comment)
                self._tw.line()
                self.write_sep("-", bold=True)
            if function_comment:
                self.write(function_comment)
                self._tw.line()
                self.write_sep("-", bold=True)
        elif self.showfspath:
            fsid = real_node_id.split("::")[0]
            self.write_fspath_result(fsid, "")

    def pytest_runtest_logreport(self, report):
        report.nodeid = report.nodeid.split(";;;;;")[0]
        super().pytest_runtest_logreport(report=report)
        self._tw.line()

    def pytest_runtest_logfinish(self, nodeid):
        nodeid = nodeid.split(";;;;;")[0]
        super().pytest_runtest_logfinish(nodeid=nodeid)
