from pydantic import BaseModel, Field, root_validator


class HTTPError(BaseModel):
    code: str
    message: str


class CachedFile(BaseModel):
    name = str(Field(alias="name"))
    name = name.split("/")[-1]
    name: str = name
    size: int
    id: int = Field(default=None)

    class Config:
        allow_extra = "allow"


class CachedMagnet(BaseModel):
    name: str
    size: int
    hash: str
    files: list[CachedFile]

    @root_validator(pre=True)
    @classmethod
    def ignore_files_without_size(cls, values):
        values["files"] = [f for f in values.get("files", []) if "size" in f]
        return values


class CachedResponse(BaseModel):
    success: str
    data: list[CachedMagnet] = Field(default_factory=list)
    error: HTTPError | None = None

    @root_validator(pre=True)
    @classmethod
    def validate_status(cls, values):
        if "data" in values and len(values["data"]) > 0:
            values = values["data"]
        return values


class AddedMagnet(BaseModel):
    torrent_id: int
    name: str
    hash: str


class AddTorrentResponse(BaseModel):
    success: str
    data: list[AddedMagnet] = Field(default_factory=list)

    @root_validator(pre=True)
    @classmethod
    def validate_status(cls, values):
        if "data" in values and len(values["data"]) > 0:
            values = values["data"]
        return values


class DownloadFile(BaseModel):
    filename: str
    size: int
    link: str


class UnlockFile(BaseModel):
    webdownload_id: int

class TorrentInfo(BaseModel):
    id: int
    name: str
    size: int
    hash: str
    download_present: bool
    seeds: int
    files: list[CachedFile]


class MagnetStatusResponse(BaseModel):
    success: str
    magnets: list[TorrentInfo]

    @root_validator(pre=True)
    @classmethod
    def validate_status(cls, values):
        if "data" in values and len(values["data"]) > 0:
            magnets = values["data"]
            if isinstance(magnets, dict):
                magnets = [magnets]
            values = magnets
        return values


# {
#     "status": "success",
#     "data": {
#         "magnets": {
#             "id": 225881725,
#             "filename": "Fargo.S05.COMPLETE.2160p.SDR.DDP5.1.x265.MKV-BEN.THE.MEN",
#             "size": 55880677310,
#             "hash": "72bb8cdf32e0cda3f73942f3f9811b53e52ab59c",
#             "status": "Ready",
#             "statusCode": 4,
#             "downloaded": 55880677310,
#             "uploaded": 55880677310,
#             "seeders": 0,
#             "downloadSpeed": 0,
#             "processingPerc": 0,
#             "uploadSpeed": 0,
#             "uploadDate": 1710306624,
#             "completionDate": 1710306624,
#             "links": [
#                 {
#                     "filename": "Fargo.S05E01.2160p.SDR.DDP5.1.x265.MKV-BEN.THE.MEN.mkv",
#                     "size": 6771186259,
#                     "files": [
#                         {
#                             "n": "Fargo.S05E01.2160p.SDR.DDP5.1.x265.MKV-BEN.THE.MEN.mkv",
#                             "s": 6771186259
#                         }
#                     ],
#                     "link": "https://alldebrid.com/f/1AsHpzyDo-7S1V6zDdxc9j6JEP7KAAFsWNIToSP2NdA"
#                 },
#                 {
#                     "filename": "Fargo.S05E02.2160p.SDR.DDP5.1.x265.MKV-BEN.THE.MEN.mkv",
#                     "size": 5770936047,
#                     "files": [
#                         {
#                             "n": "Fargo.S05E02.2160p.SDR.DDP5.1.x265.MKV-BEN.THE.MEN.mkv",
#                             "s": 5770936047
#                         }
#                     ],
#                     "link": "https://alldebrid.com/f/GsHiZaP2RLi49OOFdemNISViZAV-CLOUExwlTFhN928"
#                 },
#                 {
#                     "filename": "Fargo.S05E03.2160p.SDR.DDP5.1.x265.MKV-BEN.THE.MEN.mkv",
#                     "size": 5064974609,
#                     "files": [
#                         {
#                             "n": "Fargo.S05E03.2160p.SDR.DDP5.1.x265.MKV-BEN.THE.MEN.mkv",
#                             "s": 5064974609
#                         }
#                     ],
#                     "link": "https://alldebrid.com/f/JDVAqqP5aGdqaeQmxaiZCdJTvJb0ctwAOoVbuZCCsng"
#                 },
#                 {
#                     "filename": "Fargo.S05E04.2160p.SDR.DDP5.1.x265.MKV-BEN.THE.MEN.mkv",
#                     "size": 5624917222,
#                     "files": [
#                         {
#                             "n": "Fargo.S05E04.2160p.SDR.DDP5.1.x265.MKV-BEN.THE.MEN.mkv",
#                             "s": 5624917222
#                         }
#                     ],
#                     "link": "https://alldebrid.com/f/HOVQyjNJthaAXlXr8JxkT9xegu0yarZZACcjPum-wKQ"
#                 },
#                 {
#                     "filename": "Fargo.S05E05.2160p.SDR.DDP5.1.x265.MKV-BEN.THE.MEN.mkv",
#                     "size": 5037059219,
#                     "files": [
#                         {
#                             "n": "Fargo.S05E05.2160p.SDR.DDP5.1.x265.MKV-BEN.THE.MEN.mkv",
#                             "s": 5037059219
#                         }
#                     ],
#                     "link": "https://alldebrid.com/f/b8JUwBpCyeX2lgnjTRItHVvSokfq6XEz-CscIoCFMx0"
#                 },
#                 {
#                     "filename": "Fargo.S05E06.2160p.SDR.DDP5.1.x265.MKV-BEN.THE.MEN.mkv",
#                     "size": 5703000890,
#                     "files": [
#                         {
#                             "n": "Fargo.S05E06.2160p.SDR.DDP5.1.x265.MKV-BEN.THE.MEN.mkv",
#                             "s": 5703000890
#                         }
#                     ],
#                     "link": "https://alldebrid.com/f/Uxc9bNyRRGuuuWKhZg0H8tvPPax_gL8-wUG-XS0y0kU"
#                 },
#                 {
#                     "filename": "Fargo.S05E07.2160p.SDR.DDP5.1.x265.MKV-BEN.THE.MEN.mkv",
#                     "size": 5799180930,
#                     "files": [
#                         {
#                             "n": "Fargo.S05E07.2160p.SDR.DDP5.1.x265.MKV-BEN.THE.MEN.mkv",
#                             "s": 5799180930
#                         }
#                     ],
#                     "link": "https://alldebrid.com/f/-BeMNm7UT2HexdQugAHNayNCC59TMireRhdfHYWiEpw"
#                 },
#                 {
#                     "filename": "Fargo.S05E08.2160p.SDR.DDP5.1.x265.MKV-BEN.THE.MEN.mkv",
#                     "size": 5452286605,
#                     "files": [
#                         {
#                             "n": "Fargo.S05E08.2160p.SDR.DDP5.1.x265.MKV-BEN.THE.MEN.mkv",
#                             "s": 5452286605
#                         }
#                     ],
#                     "link": "https://alldebrid.com/f/zwLfW6Oyi4nvFCvpV9waQZUnNOrPGZOkpOFcudGR3Mc"
#                 },
#                 {
#                     "filename": "Fargo.S05E09.2160p.SDR.DDP5.1.x265.MKV-BEN.THE.MEN.mkv",
#                     "size": 5041949750,
#                     "files": [
#                         {
#                             "n": "Fargo.S05E09.2160p.SDR.DDP5.1.x265.MKV-BEN.THE.MEN.mkv",
#                             "s": 5041949750
#                         }
#                     ],
#                     "link": "https://alldebrid.com/f/rdj6De45OZQFdHrdjDJIiziWWsVjEgC6vTrKThs3Jr8"
#                 },
#                 {
#                     "filename": "Fargo.S05E10.2160p.SDR.DDP5.1.x265.MKV-BEN.THE.MEN.mkv",
#                     "size": 5615185779,
#                     "files": [
#                         {
#                             "n": "Fargo.S05E10.2160p.SDR.DDP5.1.x265.MKV-BEN.THE.MEN.mkv",
#                             "s": 5615185779
#                         }
#                     ],
#                     "link": "https://alldebrid.com/f/SQD2lKdMXDpHpfxUMaIBkJG50qrCDMTJPo1dwE2imkc"
#                 }
#             ],
#             "type": "m",
#             "notified": false,
#             "version": 2
#         }
#     }
# }
