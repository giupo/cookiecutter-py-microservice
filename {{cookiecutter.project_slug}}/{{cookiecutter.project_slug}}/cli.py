"""Console script for {{cookiecutter.project_slug}}"""

import tornado
import sys
import coloredlogs
import asyncio
import logging

from {{cookiecutter.project_slug}}.{{cookiecutter.project_slug}} import (
  get_app, 
  start_web_server,
  on_shutdown
)

from {{cookiecutter.project_slug}}.events import replay_events

log = logging.getLogger("{{cookiecutter.project_slug}}.cli")

def main():
  """Console script for {{cookiecutter.project_slug}}."""
  tornado.log.enable_pretty_logging()
  coloredlogs.install(level=log.level)
  loop = asyncio.get_event_loop()
  app = loop.run_until_complete(get_app())
  try:
    loop.run_until_complete(replay_events(app.config))
    loop.run_until_complete(start_web_server(app = app))
    loop.run_forever()
  except BaseException as e:
    log.info("Closing... (root: %s)", e)
  finally:
    loop.run_until_complete(on_shutdown(app))
    loop.close()

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
