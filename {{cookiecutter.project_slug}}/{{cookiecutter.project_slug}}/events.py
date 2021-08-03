"""Events management"""
import os
import json
import logging

from time import time

from tornado.httpclient import (
  AsyncHTTPClient, 
  HTTPRequest
)

from nats.aio.client import Client as NATS

from {{cookiecutter.project_slug}}.store import store


log = logging.getLogger("{{cookiecutter.project_slug}}.events")


async def init_events():
  nc = NATS()
  await nc.connect(os.environ.get("NATS_SERVER", "{{cookiecutter.nats_server}}"))
  return nc

async def publish_create_{{cookiecutter.project_slug}}(events, change_me):
  """publish the '{{cookiecutter.project_slug}}.created' event"""
  event: Final = "{{cookiecutter.project_slug}}.created"
  await events.publish(event, json.dumps({
    "type": event,
    "data": {
    # add data here
    }
  }).encode())

async def publish_delete_{{cookiecutter.project_slug}}(events, change_me):
  event: Final = "{{cookiecutter.project_slug}}.deleted"
  await events.publish(event, json.dumps({
    "type": event,
    "data": {
    # add data here
    }
  }).encode())

async def replay_events(config):
  """Replay all events for this server (in case of restart)"""
  log.info("Replay events for {{cookiecutter.project_slug}} service")
  # get all events for "series.*"
  start_time = time()
  http_client = AsyncHTTPClient()

  def on_receive_data(msg):
    log.debug("Received: %s", msg)
    msg = msg.decode("utf-8")
    try:
      msg = json.loads(msg)
      data = msg["data"]
      store(data)
    except Exception as e:
      log.error("Received error while processing: %s, root: %s", msg, str(e))


  try:
    req = HTTPRequest(url="https://change.me:9999/api/events/{{cookiecutter.project_slug}}",
      streaming_callback = on_receive_data, validate_cert=config.getboolean("{{cookiecutter.project_slug}}", "validate_cert"), 
      request_timeout=600)
    await http_client.fetch(req)
  except Exception as e:
    log.error(e)
  finally:
    http_client.close()
  end_time = time()
  log.info("Replay events done (elapsed: %.1fs).", end_time - start_time)
  
