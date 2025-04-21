#!/usr/bin/python

import multiprocessing
import time

import uvicorn
import vlc
from fastapi import FastAPI

app = FastAPI()
# splash = "Lowdham in 1956 Malcolm Fletcher.jpg"


@app.get("/")
async def root():
    return {"message": "sigbox-lever-video"}


@app.get("/lever/{lever_id}/{state}")
async def handle_lever(lever_id: int, state):
    print("lever_id: ", lever_id, ", state: ", state)
    match lever_id:
        case 1:
            if state == "R":
                await play_sound("3-Stopping local-L-R.mp3")

        case 13:
            if state == "R":
                await play_sound("4-Steam train non-stop R-L.mp3")

        case 14:
            if state == "R":
                await play_video("1-Gates-opening.mp4")
            else:
                await play_video("2-Gates-closing.mp4")

        case _:
            pass

    return {"lever_id": lever_id, "state": state}


async def play_video(filename: str):
    pathname = f"c:/sigbox/videos/{filename}"
    print("playing " + pathname)
    player = vlc.MediaPlayer(pathname)
    player.set_fullscreen(1)
    player.play()

    # Wait for is_playing to register the fact that it is playing
    time.sleep(0.1)
    while True:
        # app.processEvents()

        if not player.is_playing():
            player.release()
            return


async def play_sound(filename: str):
    pathname = f"c:/sigbox/sounds/{filename}"
    print("playing " + pathname)
    player = vlc.MediaPlayer(pathname)
    player.play()


if __name__ == "__main__":
    multiprocessing.freeze_support()  # For Windows support
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False, workers=1)
