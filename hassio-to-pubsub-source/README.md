# Publishing Home Assistant events to Pub/Sub

## About

This add-on subscribes to a websocket that listens to the events from Home Assistant and pushes them to a Google Cloud Pub/Sub topic.

## You will need

- Home Assistant running and accessible on the network
- A [long-lived access token](https://www.atomicha.com/home-assistant-how-to-generate-long-lived-access-token-part-1/) from Home Assistant

## Installing as a Home Assistant add-on

1. Install the repository in the Supervisor add-on store (https://github.com/a2i2/hassio-addons).
2. Open and install the `Home Assistant to Pub/Sub` add-on.
3. Set the config.

## Set config

**Note:** *Remember to restart the add-on when the configuration is changed.*

Example add-on configuration:
```
house_id: rohan-house
service_account_json: {}
filter:
  include_domains: []
  exclude_domains: []
  include_entity_globs: []
  exclude_entity_globs: []
  include_entities: []
  exclude_entities: []
```

## Running locally

1. Set personalised config as specified above.
2. Make sure Home Assistant is running.
3. Run `pip3 install --user -r requirements.txt` to install dependencies.
4. Run `python3 hass_to_pubsub.py`.

## Notes

- Had a lot of trouble getting the `grpcio` Pip package to install. [This](https://github.com/basisai/python-alpine-grpcio) seemed to do the trick.
