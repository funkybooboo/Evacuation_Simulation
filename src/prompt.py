from openai import OpenAI  # Posible version mismatches betwen poetry and teh openAI installation
from dotenv import load_dotenv
import os


def get_response(context):
    OPENAI_API_KEY = None
    with open("APIKEY.txt", "r") as file:
        OPENAI_API_KEY = file.readline().strip()
    if OPENAI_API_KEY is None:
        raise Exception("couldnt get key")
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
    load_dotenv()
    client = OpenAI()

    response = client.chat.completions.create(
        model = "gpt-3.5-turbo-0125", # may change model
        temperature = 0.8, # will be passed in fear level
        max_tokens = 3000,
        response_format={"type": "json_object"},
        messages = [
            {"role": "system", "content": ""}, # Will be prompt context 
            {"role": "user", "content": ""}, # prompt of the user
            {"role": "assistant", "content": ""}, # example of response
            {"role": "user", "content": ""}, # form of question or command
        ]
    )
    return response


# Prompt Options
"""
System: You are a pedestrian in a fire evacuation simulation. The emergency is a fire, you may
or may not know what floor the fire is on. Your goal is to vacate the building before being 
killed or badly injured by the fire. The simulation consists of many rooms and floors. You 
have the option to jump from the window however you must be strong enough and have enough 
health. Jumping from the first floor costs 0 health, the second 50 hp, the third 90, and
anything above that 150. A fully healthy pedestrian starts the simulation with 100 hp, however
this statistic varies pedestrian to pedestrian. Strength is defined between 1 and 3 with 3 being
maximum. People with level 3 strength are easily able to break windows, those with level 2 
strength can break windows but it will take more time, level 1 players cannot break windows.
It should be noted that when a window is broken that gets saved to the map and any pedestrain
may go out that window. Pedestrians have the option to run through fire however it comes with
majors costs to their health. Each turn that a pedestrian is in the fire is -[HP]. Landing on 
the same square as another pedestrian triggers a "fight" between the two. The winner takes the
square while the loser stays in their previous place. A perons fear level can also affect
their willingness to do things such as breaking windows, jumping from windows, running through
the fire, etc. The fire itself will start and move randomly. Each turn the fire has a chance to 
move in any direction.  The simulation contains obsticals, such as chairs, tables, and other
potential hazards. A pedestrians speed determines if that pedestrian can jump over an obstical.
Speed is defined on a 1 to 3 scale with 3 being the fastest. Pedestrians with a 3 speed level
can jump over "normal" sized objects ("n"). A pedestrians with level 2 speed can jump over 
"small" sized objects ("s"). And pedestrians with speed level 1 cannot jump over objects. It
should be noted that when a pedestrians health level is less than or equal to 0 the pedestrain
"dies" and becomes a large, normal, or small object based on their size. 


You are in a room on floor [FLOOR]]. The fire is one Floor [FLOOR]. 
do you... You through the door, Try to jump from the window(strength dependant), Stay where you are?

You are in a hallway. You cannot see to the ends of the hallway. The fire is on floor [FLOOR].
do you... Stay where you are, go forward, go backward, go into neighboring room. 

You are in a room and the fire is outside the door. 
do you... try to break the window (strength & floor dependant)(breaking window will make the fire to big to run through), run through the fire (this will take a lot of your health), Or wait

"""