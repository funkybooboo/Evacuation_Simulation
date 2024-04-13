CS5110 Project Details Document
Group: Rylei Nate
Authors: Nate Stott and Rylei Mindrum
Instructions: Submit the code you have produced. Include a two-page document which outlines

### The objective of the code

The objective of our project is to allow people to simulate evacuations in the event a fire catches on fire. 
Evacuations are a constant danger in society. 
Allowing designers to fine tune simulation parameters to see what would happen in emergency situations is a vital tool.

Parameters include the following:
- number_of_people: How many people should be in the building
- verbose: should information be output to the terminal
- with_ai: should choices be made by ChatGPT4
- time_for_firefighters: how long should it take for firefighters to arrive
- fire_spread_rate: how fast should the fire spread
- max_visibility: how far can people see at max
- min_visibility: how far can people see at minimum
- max_strength: how strong can people be at max
- min_strength: how strong can people be at minimum
- max_speed: how fast can people be at max
- min_speed: how fast can people be at minimum
- max_fear: how scared can people be at max
- min_fear: how scared can people be at minimum
- max_age: how old can people be at max
- min_age: how old can people be at minimum
- max_health: how healthy can people be at the start at max
- min_health: how healthy can people be at the start at minimum
- follower_probability: how likely are people to like others
- familiarity: how many objects should a person know about at max when the simulation starts

#### How to modify the simulation parameters and run the simulation

To modify the simulation parameters, you can run the simulation from the command line and pass in the parameters you want to change.

```bash
python main.py --number_of_people 100 --verbose True --with_ai True --time_for_firefighters 10 --fire_spread_rate 1 --max_visibility 10 --min_visibility 1 --max_strength 10 --min_strength 1 --max_speed 10 --min_speed 1 --max_fear 10 --min_fear 1 --max_age 100 --min_age 1 --max_health 100 --min_health 1 --follower_probability 0.5 --familiarity 10
```

This will run the simulation with 100 people, verbose output, with AI, 10 seconds for firefighters to arrive, a fire spread rate of 1, max visibility of 10, min visibility of 1, max strength of 10, min strength of 1, max speed of 10, min speed of 1, max fear of 10, min fear of 1, max age of 100, min age of 1, max health of 100, min health of 1, a follower probability of 0.5, and a familiarity of 10.

If you would like to run the simulation with the with_ai flag set to True, you must create a file called `openai_key.txt` in the src directory of the project. This file should contain your OpenAI API key.

#### How to see the output of the simulation

While the simulation is running, you will see output in the terminal if the verbose flag in True. This output will show you what is happening in the simulation. You can see the people moving around, the fire spreading, and the firefighters arriving.

Either way, you will be able to see the output of the simulation in the logs/ directory. There will be a directory for each run of the simulation, and inside that directory, you will find a log file that shows you what happened in the simulation. There will be log files for each person, the simulation, and the main file. You can use these log files to see what happened in the simulation.

#### Description of the simulation



#### How to interpret the output




#### How to expand the simulation
- Other types of emergencies
- Agents could have families
- Agents could have disabilities
- Agents could carry objects
- Agents could have different types of relationships with other agents
- Agents could have more detailed strengths and weaknesses
- Agents could have more detailed health conditions
- Agents could have more detailed fears
- The environment could be more detailed
  - More types of objects
  - Terrain types (rooms could have different types of floors, walls, and ceilings)
  - The environment could have weather effects
    - Temperatures
    - Humidity
    - Air quality
    - Wind
    - Precipitation
  - Lighting effects
  - Sound effects
  - Smells
- The environment could be more dynamic
  - Fires could spread in more complex ways
  - Fires could be put out by agents with fire extinguishers



### Significance of the output





