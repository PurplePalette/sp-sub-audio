import asyncio
import hashlib
import os

import botocore.exceptions
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from .config import FFMPEG_PATH, get_bucket
from .model import GetRootResponse, PostConvertParams, PostConvertResponse

app = FastAPI()
tmp_path = os.path.dirname(__file__) + "/../tmp/"


@app.get("/")
async def get_root() -> GetRootResponse:
    return JSONResponse(content={"status": "ok"})


@app.post("/convert")
async def upload(data: PostConvertParams) -> PostConvertResponse:
    bucket = get_bucket()
    try:
        bucket.download_file("LevelBgm/" + data.hash, tmp_path + data.hash)
    except botocore.exceptions.ClientError as e:
        if e.response["Error"]["Code"] == "404":
            return JSONResponse(content={"status": "not_found"})
    dist_filename = f"{data.hash}-{data.start}-{data.end}.mp3"
    if data.start is not None and data.end is not None:
        if data.end - data.start < 1:
            return JSONResponse(content={"message": "Must be at least 1 second"})
        elif data.end - data.start > 30000:
            return JSONResponse(content={"message": "Too long duration."}, status_code=400)
        time_args = [
            "-ss",
            str(data.start / 1000),
            "-to",
            str(data.end / 1000),
        ]
        end_time = data.end / 1000
    elif data.start is not None:
        time_args = ["-ss", str(data.start / 1000), "-to", str(data.start / 1000 + 30)]
        end_time = data.start / 1000 + 30
    elif data.end is not None:
        start = max(data.end / 1000 - 30, 0)
        time_args = ["-ss", str(start), "-to", str(data.end / 1000)]
        end_time = data.end / 1000
    else:
        time_args = ["-t", str(30)]
        end_time = 30

    await asyncio.create_subprocess_exec(
        FFMPEG_PATH,
        "-i",
        tmp_path + data.hash,
        "-vn",
        "-b:a",
        "128k",
        "-ar",
        "44100",
        "-f",
        "mp3",
        *time_args,
        "-af",
        f"afade=t=out:st={end_time - 5}:d=5",
        "-y",
        tmp_path + dist_filename,
    )

    with open(tmp_path + dist_filename, "rb") as f:
        cut_hash = hashlib.sha1(f.read()).hexdigest()
    bucket.put_object(
        Key="LevelPreview/" + cut_hash,
        Body=open(tmp_path + dist_filename, "rb"),
        ContentType="audio/mpeg",
    )
    os.remove(tmp_path + data.hash)
    os.remove(tmp_path + dist_filename)
    return JSONResponse(content={"hash": cut_hash})
