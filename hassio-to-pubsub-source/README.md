# Publishing Home Assistant events to Pub/Sub

## TODO

- [ ] Home Assistant add-on
- [ ] Use GCP service account for authentication (can be done with `GOOGLE_APPLICATION_CREDENTIALS`)
- [ ] Implement filtering for certain events/domains/entities

## You will need

- Home Assistant running and accessible on the network
- Access to the `a2i2-ua-smart-home` project on GCP (or a service account)
- A [long-lived access token](https://www.atomicha.com/home-assistant-how-to-generate-long-lived-access-token-part-1/) from Home Assistant

## Set config

Open up `hass_to_pubsub.py` and set values as appropriate near the top of the file. You will need to set:

- `HOME_ID` to something that identifies your house (e.g. `rohan-home`)
- `ACCESS_TOKEN` to your long-lived access token

## Running locally

1. Set personalised config as specified above.
2. Make sure Home Assistant is running.
3. Make sure you're authenticated with the `a2i2-ua-smart-home` project on GCP.

- To set the project, run `gcloud config set project a2i2-ua-smart-home` to set the active GCP project.
- To use your own account for authentication, run `gcloud auth application-default login`.
- To use a service account, generate a JSON key and set `GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/key.json`.

4. Run `pip3 install --user -r requirements.txt` to install dependencies.
5. Run `python3 hass_to_pubsub.py`.

## Installing as a Home Assistant add-on

TODO

## Notes

- Had a lot of trouble getting the `grpcio` Pip package to install. [This](https://github.com/basisai/python-alpine-grpcio) seemed to do the trick.
