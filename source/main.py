#!/usr/bin/python

import multiprocessing
import time

import uvicorn
import vlc
from fastapi import FastAPI


version = '1.0'
app = FastAPI()
levers = []
for x in range(0,17):
    levers.append('N')

@app.get("/")
async def root():
    messages =  {"message": "sigbox-lever-video", "version": version}
    for x in range(1,17):
        if levers[x] != 'N':
            print(f"lever {x} is {levers[x]}")
            messages[str(x)] = levers[x]
    return messages


@app.put("/lever/{lever_id}/{state}")
async def handle_lever(lever_id: int, state):
    # await debug_sound(lever_id, state)
    levers[lever_id] = state
    
    match lever_id:
        case 1:
            if state == "R":
                time.sleep(8)
                # Switch to Green wire: Stopping passenger
                # Switch to Brown wire: Mineral train
                # Switch central: No effects
                if levers[15] == 'R':
                    await play_video("Down-Stopping-Local.mp4")
                elif levers[16] == 'R':
                    await play_video("Down-Mineral.mp4")
                
        case 12:
            if state == "N":
                await play_video("Signal-12-replaced.mp4")
            else:
                await play_video("Signal-12-cleared.mp4")

        case 13:
            if state == "R":
                time.sleep(8)
                # Switch to Green wire: Stopping passenger
                # Switch to Brown wire: Mineral train
                # Switch central: No effects
                if levers[15] == 'R':
                    await play_video("Up-Stopping-Local.mp4")
                elif levers[16] == 'R':
                    await play_video("Up-Mineral.mp4")

        case 14:
            if state == "N":
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
        case 'N':
            pathname = "c:/sigbox/debug sounds/Normal.m4a"
            
        case 'R':
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
