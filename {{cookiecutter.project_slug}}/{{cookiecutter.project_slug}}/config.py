# -*- coding: utf-8 -*-

"""
Config module

manage all che configurable options for this microservice
"""

import os
import logging
import coloredlogs

from socket import gethostname
from tornado.options import define, options, parse_command_line
from tornado.log import enable_pretty_logging
from configparser import ConfigParser

DEFAULT_DBURL = os.environ.get("DBURL", "sqlite://")
DEFAULT_SERVER_CERT = "../server.crt"
DEFAULT_SERVER_KEY = "../server.key"
DEFAULT_PORT = {{cookiecutter.microservice_port}}

define('serverkey', default=DEFAULT_SERVER_KEY, help='SSL key')
define('servercert', default=DEFAULT_SERVER_CERT, help='SSL cert')
define("nproc", default=1, type=int, help="Numero processi")
define("port", default=DEFAULT_PORT, type=int, help="Porta TCP")
define("debug", default=False, type=bool)

log = logging.getLogger("{{cookiecutter.project_slug}}.config")


def make_config():
  """builds the default config for {{cookiecutter.project_slug}}"""
  parse_command_line()
  enable_pretty_logging()
  config = ConfigParser()
  config.optionxform = str
  config.add_section('{{cookiecutter.project_slug}}')

  config.set('{{cookiecutter.project_slug}}', 'debug', str(options.debug))
  config.set('{{cookiecutter.project_slug}}', 'nproc', str(options.nproc))
  config.set('{{cookiecutter.project_slug}}', 'secret', os.environ.get('SECRET', 'secret0000000000'))

  config.set('{{cookiecutter.project_slug}}', 'protocol', 'https')
  config.set('{{cookiecutter.project_slug}}', 'address', gethostname())
  config.set('{{cookiecutter.project_slug}}', 'port', str(options.port))
  config.set('{{cookiecutter.project_slug}}', 'servicename', '{{cookiecutter.project_slug}}')

  config.set('{{cookiecutter.project_slug}}', 'servercert', options.servercert)
  config.set('{{cookiecutter.project_slug}}', 'serverkey', options.serverkey)
  config.set('{{cookiecutter.project_slug}}', 'validate_cert', str(False))
  coloredlogs.install(level=log.level)

  for section in config.sections():
    for key, value in config.items(section):
      if key == "secret" or key == "password":
        value = "*" * len(value)
      log.info("[%s] %s = %s", section, key, value)

  return config
