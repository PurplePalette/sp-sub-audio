import hashlib
import boto3
import os
from dotenv import load_dotenv
from fastapi.testclient import TestClient
import pytest

from src.main import app

load_dotenv()

client = TestClient(app)
s3_endpoint = os.getenv("S3_ENDPOINT")
s3 = boto3.resource(
    "s3", endpoint_url=s3_endpoint, aws_access_key_id=os.getenv("S3_KEY"), aws_secret_access_key=os.getenv("S3_SECRET")
)
s3_bucket = s3.Bucket(os.getenv("S3_BUCKET"))

with open("./test_song.mp3", "rb") as fd:
    song_data = fd.read()
song_hash = hashlib.sha1(song_data).hexdigest()


@pytest.fixture
def upload_test_song():
    s3_bucket.put_object(Key="test_song.mp3", Body=song_data)


def test_get_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_post_convert():
    response = client.post("/convert", json={"hash": song_hash})
    response_hash = response.json()["hash"]
    assert response.status_code == 200

    s3_bucket.Object("LevelPreview/" + response_hash).get()["Body"]  # check if file exists


def test_post_convert_start():
    response = client.post("/convert", json={"hash": song_hash, "start": 10000})
    response_hash = response.json()["hash"]
    assert response.status_code == 200

    s3_bucket.Object("LevelPreview/" + response_hash).get()["Body"]  # check if file exists


def test_post_convert_start_end():
    response = client.post("/convert", json={"hash": song_hash, "start": 10000, "end": 20000})
    response_hash = response.json()["hash"]
    assert response.status_code == 200

    s3_bucket.Object("LevelPreview/" + response_hash).get()["Body"]  # check if file exists


def test_post_convert_end():
    response = client.post("/convert", json={"hash": song_hash, "end": 10000})
    response_hash = response.json()["hash"]
    assert response.status_code == 200

    s3_bucket.Object("LevelPreview/" + response_hash).get()["Body"]  # check if file exists


def test_post_convert_error_5sec():
    response = client.post("/convert", json={"hash": song_hash, "start": 10000, "end": 11000})
    assert response.status_code == 400


def test_post_convert_error_5sec_end():
    response = client.post("/convert", json={"hash": song_hash, "end": 1000})
    assert response.status_code == 400


def test_post_convert_error_30sec():
    response = client.post("/convert", json={"hash": song_hash, "start": 0, "end": 40000})
    assert response.status_code == 400
