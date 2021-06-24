import asyncio
import asyncws
import json
import logging
import os
import uuid
from google.cloud import pubsub_v1
from entityfilter import convert_filter

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

def get_required_env(var):
    """
    Gets the given environment variable or exits.
    """
    value = os.getenv(var)
    if value is None:
        LOGGER.error(f"Environment variable {var} is required")
        exit(1)

    return value


DEFAULT_FILTER = json.dumps(dict(
    include_domains=[],
    exclude_domains=[],
    include_entity_globs=[],
    exclude_entity_globs=[],
    include_entities=[],
    exclude_entities=[]
))

# Configuration constants.
HOME_ID=get_required_env("HOME_ID")
ACCESS_TOKEN=get_required_env("ACCESS_TOKEN")
FILTER=os.getenv("FILTER", DEFAULT_FILTER)
WEBSOCKET_URL=os.getenv("WEBSOCKET_URL", "ws://homeassistant.local:8123/api/websocket")
GCP_PROJECT_ID=get_required_env("GCP_PROJECT_ID")
PUBSUB_TOPIC_NAME=os.getenv("PUBSUB_TOPIC_NAME", "home-assistant-events")
PUBSUB_TOPIC= f"projects/{GCP_PROJECT_ID}/topics/${PUBSUB_TOPIC_NAME}"

# Create entity filter.
# @TODO: Validate filters against a schema
base_filter = json.loads(DEFAULT_FILTER)
user_filter = json.loads(FILTER)
final_filter = {**base_filter, **user_filter}
ENTITY_FILTER = convert_filter(final_filter)


async def main():
    """
    Application entry point. Connects to Home Assistant, listens
    for event notifications, and forwards them to Pub/Sub.
    """
    try:
        LOGGER.info("Connecting to Google Cloud Pub/Sub...")
        LOGGER.info(f"GOOGLE_APPLICATION_CREDENTIALS: {os.getenv('GOOGLE_APPLICATION_CREDENTIALS')}")
        publisher = pubsub_v1.PublisherClient()

        websocket = await hass_connect(WEBSOCKET_URL, ACCESS_TOKEN)
        await hass_subscribe_events(websocket)
        await listen_forever(websocket, publisher)
    except Exception as e:
        LOGGER.exception(f"Fatal error: {e}")



async def hass_connect(websocket_url, access_token):
    """
    Connects to the Home Assistant Websocket API.
    """
    # Connect to the websocket.
    LOGGER.info("Connecting to Home Assistant...")
    websocket = await asyncws.connect(websocket_url)
    response = await websocket.recv()
    LOGGER.info(f"Connection successful: {response}")

    # Authenticate using a long-lived access token.
    LOGGER.info("Authenticating...")
    await websocket.send(json.dumps(dict(
        type="auth",
        access_token=access_token
    )))

    # Check if authentication was successful.
    response = await websocket.recv()
    success = json.loads(response).get("type") == "auth_ok"
    if (success):
        LOGGER.info(f"Authentication successful: {response}")
        return websocket
    else:
        raise RuntimeError(f"Authentication failed: {response}")



async def hass_subscribe_events(websocket):
    """
    Subscribes to Home Assistant events.
    """
    # Subscribe to events.
    LOGGER.info("Subscribing to events...")
    await websocket.send(json.dumps(dict(
        id=1,
        type="subscribe_events",
        event_type="state_changed"
    )))
    response = await websocket.recv()
    LOGGER.info(f"Subscription result: {response}")


async def listen_forever(websocket, publisher):
    """
    Listens for events from Home Assistant.
    """
    LOGGER.info("Listening for events...")
    while True:
        message = await websocket.recv()
        if message is None:
            LOGGER.warning("No message received; continuing...")
            continue

        # Parse event info and print to log.
        try:
            raw_event = json.loads(message)
            parsed_event = parse_raw_event(raw_event)
            event_data = parsed_event["event"]["data"]
            entity = event_data['entity_id']
            old_state, new_state = get_states(event_data)
            LOGGER.info(f"Received event for {entity}: {old_state} --> {new_state}")
        except Exception as e:
            LOGGER.error(f"Could not parse event: {repr(e)}")
            continue

        # Bail out if event should not be published.
        if not should_publish(entity):
            LOGGER.info(f"{entity} does not match filters; not publishing.")
            continue

        # Publish to Pub/Sub.
        try:
            send_to_pubsub(parsed_event, publisher)
        except Exception as e:
            LOGGER.error(f"Could not publish to Pub/Sub: {repr(e)}")


def send_to_pubsub(event, publisher):
    """
    Publishes the given event to Google Cloud Pub/Sub.
    """
    def pubsub_callback(future):
        try:
            message_id = future.result()
            LOGGER.info(f"Event {message_id} published to Pub/Sub")
        except Exception as e:
            LOGGER.error(f"Pub/Sub error: {repr(e)}")

    future = publisher.publish(PUBSUB_TOPIC, json.dumps(event).encode("utf-8"))
    future.add_done_callback(pubsub_callback)


def parse_raw_event(raw_event):
    """
    Transforms the given raw event into a message
    that can be sent to the cloud.
    """
    return dict(
        id=str(uuid.uuid4()),
        home_id=HOME_ID,
        event=raw_event["event"],
        timestamp=raw_event["event"]["time_fired"]
    )


def get_states(event_data):
    """
    Returns a tuple containing the old and new state names
    from a state_changed event.
    """
    try:
        old_state = event_data["old_state"]["state"]
    except Exception as e:
        old_state = None

    try:
        new_state = event_data["new_state"]["state"]
    except Exception as e:
        new_state = None

    return (old_state, new_state)


def should_publish(entity_id):
    """
    Returns True if the given raw event should be published
    according to the configured filters.
    """
    return ENTITY_FILTER(entity_id)


asyncio.run(main())
