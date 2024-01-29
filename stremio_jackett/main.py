from typing import Any

from fastapi import FastAPI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor  # type: ignore
from opentelemetry.instrumentation.requests import RequestsInstrumentor  # type: ignore

from stremio_jackett import human, jackett
from stremio_jackett.debrid import rd
from stremio_jackett.stremio import Stream, StreamResponse, get_media_info
from stremio_jackett.torrent import Torrent

app = FastAPI()


@app.get("/manifest.json")
async def get_manifest() -> dict[str, Any]:
    return {
        "id": "community.blockloop.jackettpy",
        "icon": "https://i.imgur.com/wEYQYN8.png",
        "version": "0.1.0",
        "catalogs": [],
        "resources": ["stream"],
        "types": ["movie", "series"],
        "name": "JackettPy",
        "description": "Stremio Jackett Addon",
        "behaviorHints": {
            "configurable": "true",
        },
    }


@app.get("/stream/{type:str}/{id:str}.json")
async def search(
    type: str,
    id: str,
    streamService: str,
    jackettUrl: str,
    jackettApiKey: str,
    debridApiKey: str,
    maxResults: int = 5,
) -> StreamResponse:
    print(f"Received request for {type} {id}")
    imdb_id = id.split(":")[0]
    print(f"Searching for {type} {id}")

    media_info = await get_media_info(id=imdb_id, type=type)
    if not media_info:
        print(f"Error getting media info for {type} {id}")
        return StreamResponse(streams=[], error="Error getting media info")
    print(f"Found Media Info: {media_info.model_dump_json()}")

    q = jackett.SearchQuery(
        name=media_info.name,
        type=type,
    )

    if type == "series":
        q.season = id.split(":")[1]
        q.episode = id.split(":")[2]

    torrents: list[Torrent] = await jackett.search(
        debrid_api_key=debridApiKey,
        jackett_url=jackettUrl,
        jackett_api_key=jackettApiKey,
        max_results=maxResults,
        search_query=q,
        imdb=int(imdb_id.replace("tt", "")),
    )

    # print(f"Found {len(torrents)} torrents for {type} {id}")
    # for torrent in torrents:
    #     print(f"Torrent: {torrent.model_dump_json(indent=2)}")
    # return StreamResponse(streams=[], error="Error getting media info")

    # make get_movie_rd_links return a better struct with more info like
    # resolution (4K) and audio channels (5.1)
    rd_links: list[rd.UnrestrictedLink] = await rd.get_stream_links(
        torrents=torrents,
        debrid_token=debridApiKey,
        season_episode="E".join(id.split(":")[1:]),
        max_results=maxResults,
    )

    # sort by size
    # rd_links.sort(key=lambda link: link.filesize, reverse=True)

    streams: list[Stream] = [
        Stream(
            title=media_info.name,
            url=link.download,
            name="\n".join(
                [
                    link.filename,
                    f"💾{human.bytes(float(link.filesize))}",
                ]
            ),
        )
        for link in rd_links
        if link
    ]
    return StreamResponse(streams=streams)


if __name__ == "__main__":
    FastAPIInstrumentor.instrument_app(app)  # type: ignore
    RequestsInstrumentor().instrument()  # type: ignore

    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)  # type: ignore