import json
import base64

from google.cloud import bigquery

PROJECT = "a2i2-ua-smart-home"
DATASET = "event_data"
TABLE = "events"

bigquery_client = bigquery.Client(project=PROJECT)
dataset = bigquery_client.dataset(DATASET)
table_ref = dataset.table(TABLE)
table = bigquery_client.get_table(table_ref)


def hass_to_bigquery(data, context):

    if "data" in data:
        event = json.loads(
            base64.b64decode(
                data["data"]
            )
        )
    else:
        raise ValueError("No data provided")

    # Stringify attributes as these are event-specific and can't be accounted for in the schema.
    try:
        event["event"]["data"]["old_state"]["attributes"] = json.dumps(event["event"]["data"]["old_state"]["attributes"])
    except KeyError as e:
        print("Can't rewrite old_state attributes")

    try:
        event["event"]["data"]["new_state"]["attributes"] = json.dumps(event["event"]["data"]["new_state"]["attributes"])
    except KeyError as e:
        print("Can't rewrite new_state attributes")


    res = bigquery_client.insert_rows_json(table, [event])

    print(f"Result: {res}")