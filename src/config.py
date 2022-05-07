import os
from os.path import dirname, join
from typing import TYPE_CHECKING

import boto3
from dotenv import load_dotenv

if TYPE_CHECKING:
    import botostubs

load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

S3_ENDPOINT = os.environ.get("S3_ENDPOINT")
S3_BUCKET = os.environ.get("S3_BUCKET")
S3_KEY = os.environ.get("S3_KEY")
S3_SECRET = os.environ.get("S3_SECRET")
FFMPEG_PATH = os.environ.get("FFMPEG", "ffmpeg")


def get_bucket() -> "botostubs.S3.S3Resource.Bucket":
    """Boto3インスタンスを作成し、S3バケットを返します"""
    s3: "botostubs.S3.S3Resource" = boto3.resource(
        "s3",
        endpoint_url=S3_ENDPOINT,
        aws_access_key_id=S3_KEY,
        aws_secret_access_key=S3_SECRET,
    )
    bucket: "botostubs.S3.S3Resource.Bucket" = s3.Bucket(S3_BUCKET)  # type: ignore
    return bucket
