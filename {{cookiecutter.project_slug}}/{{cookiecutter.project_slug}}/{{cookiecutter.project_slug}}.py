"""
Main module.

Defines the Controller for {{cookiecutter.project_slug}} resource
"""

import os
import logging

import tornado.web
from tornado.httpclient import AsyncHTTPClient

from {{cookiecutter.project_slug}}.events import (
  init_events,
)

from {{cookiecutter.project_slug}}.config import make_config
from {{cookiecutter.project_slug}}.auth import authenticated
from {{cookiecutter.project_slug}} import __version__

from {{cookiecutter.project_slug}}.store import (
  store,
)



log = logging.getLogger("{{cookiecutter.project_slug}}.{{cookiecutter.project_slug}}")
AsyncHTTPClient.configure("tornado.curl_httpclient.CurlAsyncHTTPClient")

def build_routes():
  init_params = {}
  routes = []
  return routes


async def get_app(config=make_config()):
  settings = {
    "cookie_secret": config.get('{{cookiecutter.project_slug}}', 'secret'),
    "debug": config.getboolean('{{cookiecutter.project_slug}}', 'debug')
  }
  app = tornado.web.Application(build_routes(), **settings)
  app.config = config
  app.events = await init_events()
  return app


async def on_shutdown(app):
  log.info("Shutdown service started")
  await app.events.close()
  log.info("Shutdown completed")


def build_ssl_options(config):
  ssl_options = {
    "certfile": config.get('{{cookiecutter.project_slug}}', 'servercert'),
    "keyfile": config.get('{{cookiecutter.project_slug}}', 'serverkey')
  }
  # if files for SSL do not exist, return None
  for filename in ssl_options.values():
    if not os.path.isfile(filename):
      return None

  return ssl_options

async def start_web_server(app):
  log.info("Starting web server...")
  addr = app.config.get('{{cookiecutter.project_slug}}', 'address')
  port = app.config.getint('{{cookiecutter.project_slug}}', 'port')
  protocol = app.config.get('{{cookiecutter.project_slug}}', 'protocol')

  ssl_options = build_ssl_options(app.config)

  protocol = "http" if ssl_options is None else "https"
  if protocol != "https":
    log.warn("This service should always be served on HTTPS!")
     
  app.config.set('{{cookiecutter.project_slug}}', 'protocol', protocol)

  server = tornado.httpserver.HTTPServer(app, ssl_options=ssl_options)
  server.bind(port)
  log.info("{{cookiecutter.project_slug}} at %s://%s:%s", protocol, addr, port)
    
  app.config.set('{{cookiecutter.project_slug}}', 'port', str(port))
  log.info("Registering services")

  server.start(app.config.getint('{{cookiecutter.project_slug}}', 'nproc'))
  log.info("{{cookiecutter.project_slug}}(%s) started (PID: %s)", __version__, os.getpid())


class BaseHandler(tornado.web.RequestHandler):
  def set_default_headers(self) -> None:
    super().set_default_headers()
    self.set_header('Content-Type', 'application/json')
    self.set_header('Access-Control-Allow-Origin', '*')

  async def finish_with_status(self, status, message):
    self.set_status(status)
    self.write({
      "status": status,
      "message": message
    })
    await self.flush()    
