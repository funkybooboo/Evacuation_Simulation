from openai import OpenAI  # Posible version mismatches betwen poetry and teh openAI installation
from dotenv import load_dotenv
import os


def get_response(situation, options, temperature):
    OPENAI_API_KEY = None
    with open("APIKEY.txt", "r") as file:
        OPENAI_API_KEY = file.readline().strip()
    if OPENAI_API_KEY is None:
        raise Exception("couldn't get key")
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
    load_dotenv()
    client = OpenAI()

    # option A: explore | always open
    # option B: move randomly | always open
    # option C: move towards a person | if know about person, more likely if you like people
    # option D: move towards a door | if know about door
    # option E: move towards a glass | if know about glass
    # option F: move towards a fire | if know about fire and stuck in room
    # option G: break glass | if next to glass
    # option H: fight someone for a spot | if someone is in a spot you want
    # option I: run through fire to safety | if stuck in room
    # option J: jump out of building | if next to
    # option K: follow evacuation plan | if know about evacuation plan
    # option L: move to exit | if know about exit on your floor
    # option M: move to stair | if know about stair on your floor

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125", # may change model
        temperature=temperature, # will be passed in fear level
        max_tokens=3000,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": ""}, # Will be prompt context 
            {"role": "user", "content": situation}, # prompt of the user
            {"role": "assistant", "content": """
            Options:
            A. Explore
            C. Move towards a person
            D. Move towards a door
            E. Move towards a glass
            H. Fight someone for a spot
            I. Run through fire to safety
            K. Follow evacuation plan
            L. Move towards an exit
            M. Move towards a stair
            ----------------------
            Pick a letter:
            L
            """}, # example of response
            {"role": "user", "content": "Options:\n" + options + "\n----------------------\nPick a letter:"}, # form of question or command
        ]
    )
    return response

def get_random_choice(situation, options, tempurature):
    pass

def get_choice_from_AI(situation, options, tempurature):
    response = get_response(situation, options, tempurature)
    return response.choices[0].message["content"]


# Prompt Options
"""
System: You are a pedestrian in a fire evacuation simulation. You may
or may not know what floor the fire is on. Your goal is to vacate the building before being 
killed or badly injured by the fire. The simulation consists of many rooms and floors. You 
have the option to jump from the window however you must be strong enough and have enough 
health. Jumping from the first floor costs 0 health, the second 50 hp, the third 90, and
anything above that 150. A fully healthy pedestrian starts the simulation with 100 hp, however
this statistic varies pedestrian to pedestrian. Strength is defined between 1 and 3 with 3 being
maximum. People with level 3 strength are easily able to break windows, those with level 2 
strength can break windows but it will take more time, level 1 players cannot break windows.
It should be noted that when a window is broken that gets saved to the map and any pedestrian
may go out that window. Pedestrians have the option to run through fire however it comes with
majors costs to their health. Each turn that a pedestrian is in the fire is -[HP]. Landing on 
the same square as another pedestrian triggers a "fight" between the two. The winner takes the
square while the loser stays in their previous place. A persons fear level can also affect
their willingness to do things such as breaking windows, jumping from windows, running through
the fire, etc. The fire itself will start and move randomly. Each turn the fire has a chance to 
move in any direction.  The simulation contains obstetrical, such as chairs, tables, and other
potential hazards. A pedestrians speed determines if that pedestrian can jump over an obstetrical.
Speed is defined on a 1 to 3 scale with 3 being the fastest. Pedestrians with a 3 speed level
can jump over "normal" sized objects ("n"). A pedestrians with level 2 speed can jump over 
"small" sized objects ("s"). And pedestrians with speed level 1 cannot jump over objects. It
should be noted that when a pedestrians health level is less than or equal to 0 the pedestrian
"dies" and becomes a large, normal, or small object based on their size. 


You are in a room on floor [FLOOR]]. The fire is one Floor [FLOOR]. 
do you... You through the door, Try to jump from the window(strength dependant), Stay where you are?

You are in a hallway. You cannot see to the ends of the hallway. The fire is on floor [FLOOR].
do you... Stay where you are, go forward, go backward, go into neighboring room. 

You are in a room and the fire is outside the door. 
do you... try to break the window (strength & floor dependant)(breaking window will make the fire to big to run through), run through the fire (this will take a lot of your health), Or wait

"""