from enum import Enum
from hashlib import sha1
from tempfile import NamedTemporaryFile

from config import get_bucket
from fastapi import UploadFile
from pydub import AudioSegment


class AudioConversionStatus(Enum):
    """音源変換ステータス定数"""

    # 処理中
    PROCESSING = 0
    # 変換済み
    COMPLETED = 1
    # 変換失敗
    FAILED = -1


class AudioConversionTask:
    """
    pydubを用いて音源変換を行うタスク
    """

    status: AudioConversionStatus = AudioConversionStatus.PROCESSING

    def __init__(self, file: UploadFile) -> None:
        self.status = AudioConversionStatus.PROCESSING
        self.file = file
        print("AudioConversion task initialized.")

    async def __call__(self) -> None:
        """バックグラウンドタスクとして実行されるメソッド"""
        try:
            fp = NamedTemporaryFile()
            buf: bytes = await self.file.read()  # type: ignore
            sha1_hash = sha1(buf).hexdigest()
            fp.write(buf)
            fp.seek(0)
            sound = AudioSegment.from_file(fp.name, format="mp3")
            cuted = sound[:30000].fade_out(5000)
            cuted.export(
                fp.name,
                format="mp3",
                bitrate="128k",
                tags={"album": sha1_hash, "artist": "PurplePalette"},
            )
            fp.seek(0)
            bucket = get_bucket()
            bucket.put_object(Body=fp.read(), Key=f"AudioPreview/{sha1_hash}")
            fp.close()
        except Exception as e:
            print("変換エラー:", e)
            self.status = AudioConversionStatus.FAILED
        else:
            print("変換できたらしい")
            self.status = AudioConversionStatus.COMPLETED

    def get_status(self) -> AudioConversionStatus:
        return self.status
