# Google Cloud Pub/Sub publisher

Publishes Home Assistant events from multiple homes to Google Cloud Pub/Sub.

## Note

This add-on is currently for internal use only and requires access to a private Google Cloud project.

## Installation

1. Login to homeassistant.local:8123 and navigate to the Supervisor tab.
2. Add this repository to the Add-On Store.
3. Locate the add-on and install it.
4. Add required configuration (see below).

## Configuration

Two configuration values are required before running this add-on:

* `home_id`: Unique identifier for your home.
* `service_account_json`: Contents of a GCP service account with `Pub/Sub Publisher` access to the `a2i2-ua-smart-home` project.

## Building

This add-on is currently built/pushed manually from our internal repository.
