# -*- coding: utf-8 -*-


import logging
import logging.handlers
import sys

import sshrc


LOG_NAMESPACE = "sshrc"
LOG_FORMAT_DEBUG = "[%(levelname)s] %(name)30s:%(lineno)d - %(message)s"
LOG_FORMAT_SIMPLE = "%(message)s"
LOG_FORMAT_SYSLOG = "{}(%(process)d) {}".format(
    LOG_NAMESPACE, LOG_FORMAT_SIMPLE)


def topen(filename, write=False):
    mode = "w" if write else "r"
    return open(filename, mode, encoding="utf-8", errors="surrogateescape")


def get_content(filename):
    with topen(filename) as filefp:
        return filefp.read()


def logger(namespace):
    return logging.getLogger(LOG_NAMESPACE + "." + namespace)


def configure_logging(debug=False, stderr=True):
    root_logger = logging.getLogger(LOG_NAMESPACE)
    root_logger.propagate = False
    root_logger.setLevel(logging.DEBUG)
    root_logger.handlers = []

    if sys.platform.startswith("linux"):
        syslog_address = "/dev/log"
    elif sys.platform == "darwin":
        syslog_address = "/var/run/syslog"
    else:
        syslog_address = "localhost", 514

    syslog_formatter = logging.Formatter(LOG_FORMAT_SYSLOG)
    syslog_handler = logging.handlers.SysLogHandler(syslog_address)
    syslog_handler.setLevel(logging.INFO)
    syslog_handler.setFormatter(syslog_formatter)
    root_logger.addHandler(syslog_handler)

    if stderr:
        if debug:
            log_format = LOG_FORMAT_DEBUG
        else:
            log_format = LOG_FORMAT_SIMPLE

        stderr_formatter = logging.Formatter(log_format)
        stderr_hander = logging.StreamHandler()
        level = logging.DEBUG if debug else logging.ERROR
        stderr_hander.setLevel(level)
        stderr_hander.setFormatter(stderr_formatter)
        root_logger.addHandler(stderr_hander)