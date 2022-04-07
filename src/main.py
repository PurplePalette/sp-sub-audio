from fastapi import FastAPI, UploadFile, BackgroundTasks, HTTPException
from depends import dependsFile, dependsFileSize, MAXIMUM_FILESIZE
from task import AudioConversionTask

app = FastAPI()


@app.get("/")
async def get_root():
    return {"message": "Server is running."}


@app.post("/convert")
async def upload(
    background_tasks: BackgroundTasks,
    file: UploadFile = dependsFile,
    file_size: int = dependsFileSize,
):
    file_type = file.content_type
    if file_type != "audio/mp3":
        raise HTTPException(status_code=400, detail="Invalid file type")
    if file_size > MAXIMUM_FILESIZE:
        raise HTTPException(status_code=400, detail="File size is too large")
    background_tasks.add_task(AudioConversionTask(file))
    return {"message": "started preview generating..."}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
