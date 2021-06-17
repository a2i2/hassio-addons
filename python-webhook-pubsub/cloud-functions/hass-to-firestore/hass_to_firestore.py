import base64
import uuid
import json
from google.cloud import firestore

db = firestore.Client()


def hass_to_firestore(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    hass_event = json.loads(base64.b64decode(event['data']).decode('utf-8'))
    print(hass_event)

    home_id = hass_event['home_id']
    event_id = hass_event['id']

    doc_ref = db.collection(home_id).document(event_id)
    doc_ref.set(hass_event)

    print(doc_ref)
