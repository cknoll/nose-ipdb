"""
This plugin provides ``--ipdb`` and ``--ipdb-failures`` options. The ``--ipdb``
option will drop the test runner into pdb when it encounters an error. To
drop into pdb on failure, use ``--ipdb-failures``.
"""
import logging
import sys
import inspect
import traceback
from nose.plugins.base import Plugin
import unittest

from ipydex import IPS

log = logging.getLogger("nose.plugins.ipdbplugin")

class iPdb(Plugin):
    """
    Provides --ipdb and --ipdb-failures options that cause the test runner to
    drop into ipdb if it encounters an error or failure, respectively.
    """
    enabled_for_errors = False
    enabled_for_failures = False
    ips_enabled_for_failures_and_errors = False
    score = 5 # run last, among builtins

    def options(self, parser, env):
        """Register commandline options.
        """
        parser.add_option(
            "--ipdb", action="store_true", dest="ipdbErrors",
            default=env.get('NOSE_IPDB', False),
            help="Drop into ipdb on errors")
        parser.add_option(
            "--ipdb-failures", action="store_true",
            dest="ipdbFailures",
            default=env.get('NOSE_IPDB_FAILURES', False),
            help="Drop into ipdb on failures")
        parser.add_option(
            "--ips", action="store_true", dest="ipsErrorsAndFailures",
            default=False,
            help="Drop into IPython embedded shell on errors")

    def configure(self, options, conf):
        """Configure which kinds of exceptions trigger plugin.
        """
        self.conf = conf
        self.enabled = any([options.ipdbErrors, options.ipdbFailures, options.ipsErrorsAndFailures])
        self.enabled_for_errors = options.ipdbErrors
        self.enabled_for_failures = options.ipdbFailures
        self.ips_enabled_for_failures_and_errors = options.ipsErrorsAndFailures

        if options.capture:
            log.warn("Autocomplete will not work with stdout capture on. "
                     "Use --nocapture to have the ipdb shell working properly.")

    def addError(self, test, err):
        """Enter ipdb if configured to debug errors.
        """
        if self.enabled_for_errors:
            self.debug(err)
        elif self.ips_enabled_for_failures_and_errors:
            self.debug(err, ips=True)

    def addFailure(self, test, err):
        """Enter ipdb if configured to debug failures.
        """

        if self.enabled_for_failures:
            self.debug(err)
        elif self.ips_enabled_for_failures_and_errors:
            self.debug(err, ips=True)
            return

    def debug(self, err, ips=False):
        ec, ev, tb = err
        # This is to work around issue #16, that occured when the exception
        # value was being passed as a string.
        if isinstance(ev, str):
            ev = ec(ev)
        stdout = sys.stdout
        sys.stdout = sys.__stdout__
        sys.stderr.write('\n- TRACEBACK --------------------------------------------------------------------\n')
        traceback.print_exception(ec, ev, tb)
        sys.stderr.write('--------------------------------------------------------------------------------\n')
        try:

            debugger = get_debugger(ips)

            frame = get_relevant_frame(tb)
            debugger(frame, tb)
        finally:
            sys.stdout = stdout


def get_debugger(ips):
    import IPython

    if ips:
        from ipydex import ip_shell_after_exception

        return ip_shell_after_exception
    else:
        from IPython.terminal.ipapp import TerminalIPythonApp
        app = TerminalIPythonApp.instance()
        app.initialize(argv=['--no-banner'])
        try:
            # ipython >= 5.0
            p = IPython.terminal.debugger.TerminalPdb(app.shell.colors)
        except AttributeError:
            p = IPython.core.debugger.Pdb(app.shell.colors)

        p.reset()
        return p.interaction


def get_relevant_frame(tb):
    """
    Plain tests (like `assert x==y`) raise an direct exception so that frame shall be returned.
    However the unittest package works like `self.assertEqual(x, y)` so the Exception is raised not in
    the actual test case method. Here we go up in the frame list to leave the unittest package and hopefully
    the caller frame is the actual testcase.

    :param tb:
    :return:
    """

    # inspect.getinnerframes() returns a list of frames information
    # from this frame to the one that raised the exception being
    # treated

    frame_info_list = inspect.getinnerframes(tb)
    frame_info_list.reverse()
    for fi in frame_info_list:
        frame, filename, line, func_name, ctx, idx = fi
        if not filename == inspect.getabsfile(unittest.TestCase):
            break

    return frame
