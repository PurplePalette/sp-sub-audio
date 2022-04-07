import os
from os.path import dirname, join
from typing import Any, cast
import boto3

from dotenv import load_dotenv

load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

S3_ENDPOINT = os.environ.get("S3_ENDPOINT")
S3_BUCKET = os.environ.get("S3_BUCKET")
S3_KEY = os.environ.get("S3_KEY")
S3_SECRET = os.environ.get("S3_SECRET")
MAXIMUM_FILESIZE = (
    int(cast(str, os.environ.get("MAXIMUM_FILESIZE")))
    if os.environ.get("MAXIMUM_FILESIZE") is not None
    else 30 * 1024 * 1024  # 30MB
)


def get_bucket() -> Any:
    """Boto3インスタンスを作成し、S3バケットを返します"""
    s3 = boto3.resource(
        "s3",
        endpoint_url=S3_ENDPOINT,
        aws_access_key_id=S3_KEY,
        aws_secret_access_key=S3_SECRET,
    )
    bucket = s3.Bucket(S3_BUCKET)  # type: ignore
    return bucket
