import json
import logging
from datetime import datetime
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from xml.etree import ElementTree

import boto3
from botocore.exceptions import ClientError
from dateutil import parser

logger = logging.getLogger()
logger.setLevel(logging.INFO)

sns = boto3.client("sns")


def lambda_handler(event, context):
    logger.info("Event: " + str(event))

    game_item = {"item_name": "Condottiere", "item_id": "112"}
    try:
        url = f'https://boardgamegeek.com/xmlapi2/thing?id={game_item["item_id"]}&marketplace=1'
        response = urlopen(
            Request(url=url, headers={"Accept": "application/json"}, method="GET"),
            timeout=5,
        )

        root = ElementTree.fromstring(response.read())
        for child in root[0]:
            if child.tag == "marketplacelistings":
                listings = child

        listings = listings.findall("listing")
        listings_count = len(listings)
        new_item_count = 0
        for listing in listings:
            list_date = listing.find("listdate")
            list_date_datetime = parser.parse(list_date.attrib["value"])
            if list_date_datetime.date() == datetime.today().date():
                new_item_count += 1

        # TODO: Determine better way to count new listings. API data is stale, and may not show listings until day later.
        message = f"There are {new_item_count} new listings for {game_item['item_name']} today. There are {listings_count} total listings."
        publish_sns_message(message)
    except HTTPError as e:
        logger.error("Request failed: %d %s", e.code, e.reason)
    except URLError as e:
        logger.error("Server connection failed: %s", e.reason)


def publish_sns_message(message):
    try:
        response = sns.publish(
            TargetArn="arn:aws:sns:us-east-1:498122022799:bgg-market-monitor",
            Message=json.dumps({"default": json.dumps(message)}),
            MessageStructure="json",
        )
        message_id = response["MessageId"]
        logger.info("Published message")
    except ClientError:
        logger.exception("Couldn't publish message.")
        raise
    else:
        return message_id
