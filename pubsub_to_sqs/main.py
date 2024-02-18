# Standard library
import base64
import os

# Third-party
import boto3
import functions_framework
from cloudevents.http import CloudEvent
from google.auth import default
from google.cloud import logging


_, project_id = default()
logging_client = logging.Client(project=project_id)
logger = logging_client.logger(__name__)



def _get_sqs_client():
    return boto3.client(
        "sqs",
        "us-east-2",
        aws_access_key_id=os.environ["AWS-ACCESS-KEY-ID"],
        aws_secret_access_key=os.environ["AWS-SECRET-ACCESS-KEY"],
    )


@functions_framework.cloud_event
def send_notification(cloud_event: CloudEvent) -> None:
    logger.log_text(f"{cloud_event.data=}")
    sqs_client = _get_sqs_client()
    response = sqs_client.send_message(
        QueueUrl=os.environ["SQS-URL"],
        MessageBody=base64.b64decode(cloud_event.data["message"]["data"]).decode(),
    )
    logger.log_text(f"SQS MessageId : {response.get('MessageId')}")
