#!/usr/bin/python

import multiprocessing
import time

import uvicorn
import vlc
from fastapi import FastAPI

version = "1.1"
app = FastAPI()
levers = []
player = None
train_playing = None

for x in range(0, 17):
    levers.append("N")


@app.get("/")
async def root():
    messages = {"message": "sigbox-lever-video", "version": version}
    for x in range(1, 17):
        if levers[x] != "N":
            print(f"lever {x} is {levers[x]}")
            messages[str(x)] = levers[x]
    return messages


@app.put("/lever/{lever_id}/{state}")
async def handle_lever(lever_id: int, state):
    global train_playing
    global player

    # await debug_sound(lever_id, state)
    levers[lever_id] = state
    print(f"Playing: {train_playing}")

    match lever_id:
        case 1 | 13:
            if state == "N":
                print(f"Distant lever {lever_id} replaced")
                return

            if train_playing:
                print("Already playing a train")
                return

            train = get_train_type()
            if not train:
                return

            train_playing = "Down" if lever_id == 1 else "Up"
            print(f"{train_playing} {train} approaching")

            time.sleep(8)
            await play_video(f"{train_playing}-{train}.mp4", 30)

        case 11 | 12:
            if state == "N":
                if not player:
                    # Only play returning the signal to danger if nothing else is playing
                    await play_video("Signal-12-replaced.mp4")
            else:
                await play_video("Signal-12-cleared.mp4")

        case 4 | 8 | 10:
            if state == "N":
                await play_video("Points and Ground Signal 2.mp4")
            else:
                await play_video("Points and Ground Signal 1.mp4")

        case 14:
            if state == "N":
                await play_video("1-Gates-opening.mp4")
            else:
                await play_video("2-Gates-closing.mp4")

        case 15 | 16:
            get_train_type()

            if player:
                player.release()
                player = None
                train_playing = None

        case _:
            pass

    return {"lever_id": lever_id, "state": state}


def get_train_type():
    # Switch to Green wire: Stopping passenger
    # Switch to Brown wire: Mineral train
    # Switch central: No effects
    if levers[15] == "R":
        print("Stopping-Local train selected")
        return "Stopping-Local"
    elif levers[16] == "R":
        print("Mineral train selected")
        return "Mineral"
    print("No train type selected")
    return None


async def play_video(filename: str, min_play_seconds=30):
    global player
    global train_playing
    # Play at least {min_play_seconds}. Return then, or when the video has finished, whichever is soonest.
    pathname = f"c:/sigbox/videos/{filename}"
    print("playing " + pathname)

    if player:
        player.release()

    player = vlc.MediaPlayer(pathname)
    player.set_fullscreen(1)
    player.play()

    end_time = time.time() + min_play_seconds
    # Wait for is_playing to register the fact that it is playing
    time.sleep(0.1)

    while time.time() < end_time:
        # app.processEvents()
        time.sleep(1)

        if not player.is_playing():
            player.release()
            player = None
            train_playing = None
            return


async def debug_sound(lever_id: int, state):
    print("lever_id: ", lever_id, ", state: ", state)
    pathname = f"c:/sigbox/debug sounds/lever {lever_id}.m4a"
    # print("playing " + pathname)
    player = vlc.MediaPlayer(pathname)
    player.play()

    time.sleep(0.1)
    while player.is_playing():
        time.sleep(0.01)

    match state:
        case "N":
            pathname = "c:/sigbox/debug sounds/Normal.m4a"

        case "R":
            pathname = "c:/sigbox/debug sounds/Reversed.m4a"

        case _:
            return

    # print("playing " + pathname)
    player = vlc.MediaPlayer(pathname)
    player.play()


async def play_sound(filename: str):
    pathname = f"c:/sigbox/sounds/{filename}"
    print("playing " + pathname)
    player = vlc.MediaPlayer(pathname)
    player.play()


if __name__ == "__main__":
    # splash = "Lowdham in 1956 Malcolm Fletcher.jpg"

    multiprocessing.freeze_support()  # For Windows support
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False, workers=1)
