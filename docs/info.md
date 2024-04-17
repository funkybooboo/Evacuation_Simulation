# CS5110 Project Details Document
## Group: Rylei Nate
## Authors: Nate Stott and Rylei Mindrum
## Instructions: Submit the code you have produced. Include a two-page document which outlines the following:

### Objective of the Code

Our project aims to facilitate simulations of evacuations in the event of a fire outbreak. 
Evacuations pose a perpetual threat in society, and providing designers with the ability to finely adjust simulation parameters to anticipate outcomes in emergency scenarios is crucial. 
Our simulation allows users to observe how various types of individuals react in diverse situations. 
Based on a research paper focusing on preventing stampedes in emergencies, we've expanded the concept by introducing more complex behaviors among the agents in the simulation. 
We measure numerous factors to gauge their impact on the simulation's outcome, including the number of people, fire speed, individual attributes, and behavioral tendencies.

### Description of the Simulation

The simulation operates on a 3D grid representing a building, populated with individuals. 
The building consists of multiple floors, each containing numerous rooms and hallways. 
Individuals vary in their familiarity with the building and adherence to evacuation plans. 
A fire initiates in one of the rooms, progressively spreading over time. 
Individuals assess their surroundings, making decisions on evacuation routes. 
They utilize environmental memory for decision-making; in unfamiliar surroundings, they explore to find exits. 
Conflict avoidance and physical confrontation are modeled behaviors. 
Individuals trapped in rooms with fires attempt to escape via doors or windows, with stronger individuals capable of breaking windows or even attempting to pass through fires. 
Fear and health status influence decision-making, with frightened individuals exhibiting more irrational behaviors. 
The simulation continues until all individuals exit the building or the firefighters arrive.

### Parameters
- number_of_people: Number of individuals in the building.
- verbose: Output verbosity.
- with_ai: Integration of ChatGPT4 for decision-making.
- time_for_firefighters: Duration until firefighters arrive. 
- fire_spread_rate: Rate of fire spread. 
- max_visibility: Maximum visibility range. 
- min_visibility: Minimum visibility range. 
- max_strength: Maximum strength of individuals. 
- min_strength: Minimum strength of individuals. 
- max_speed: Maximum speed of individuals. 
- min_speed: Minimum speed of individuals. 
- max_fear: Maximum fear level of individuals. 
- min_fear: Minimum fear level of individuals. 
- max_age: Maximum age of individuals. 
- min_age: Minimum age of individuals. 
- max_health: Maximum health of individuals. 
- min_health: Minimum health of individuals. 
- follower_probability: Likelihood of individuals to follow others. 
- familiarity: Number of objects individuals know about at maximum at the simulation start.

### Modifying Simulation Parameters and Running

To adjust simulation parameters, execute the simulation from the command line and specify desired parameters:

```bash
python main.py --number_of_people 100 --verbose True --with_ai True --time_for_firefighters 10 --fire_spread_rate 1 --max_visibility 10 --min_visibility 1 --max_strength 10 --min_strength 1 --max_speed 10 --min_speed 1 --max_fear 10 --min_fear 1 --max_age 100 --min_age 1 --max_health 100 --min_health 1 --follower_probability 0.5 --familiarity 10
```

For running the simulation with with_ai set to True, create a file named openai_key.txt in the project's src directory containing your OpenAI API key.

### Viewing Simulation Output

During simulation runtime, verbose output (if enabled) displays real-time simulation events, including individuals' movements, fire spread, and firefighter arrivals. 
Additionally, simulation logs are stored in the logs/ directory, providing detailed information about simulation runs, individual experiences, and general simulation outcomes.

### Interpreting Output

Given the substantial data generated per simulation run, data analysis tools can aid in interpreting results. 
However, textual logs also provide insights into simulation events. 
Key aspects to observe include the statistics report, which outlines the number of individuals inside and outside the building, casualties, and remaining individuals within the building.

### Expanding the Simulation

The simulation can be expanded in various ways:
- Introducing other emergency scenarios such as earthquakes, floods, or terrorist attacks. 
- Modeling familial relationships among individuals to simulate group dynamics and decision-making processes. 
- Incorporating disabilities among individuals to account for different mobility levels and evacuation challenges. 
- Allowing individuals to carry objects such as personal belongings, pets, or emergency supplies, affecting their mobility and decision-making. 
- Enhancing interpersonal relationships among individuals to simulate cooperation, leadership, or conflicts during evacuations. 
- Fine-tuning individual attributes such as strengths, weaknesses, health conditions, and fears to create more nuanced behaviors and responses. 
- Enriching environmental details with additional objects, diverse terrain types, and weather effects to simulate realistic evacuation scenarios. 
- Implementing dynamic environmental changes, such as complex fire spread patterns and extinguishing efforts by individuals or emergency responders. 
- Facilitating information sharing among individuals about the environment, emergency procedures, and safe evacuation routes to promote collaboration and collective decision-making.
- Exit knowledge based on path of entry to a current location; people should know the path they took to get in and be able to use it to get out.

### Significance of the Output

The simulation output serves as a valuable resource for understanding the impact of various factors on evacuation outcomes. 
Insights gained can inform better building designs, emergency training protocols, and evacuation strategies, ultimately enhancing preparedness and safety measures. 
Moreover, the expanded simulation capabilities offer opportunities for interdisciplinary research and collaboration across fields such as urban planning, disaster management, and human behavior studies. 
By continuously refining and expanding the simulation, we contribute to the development of more effective emergency response strategies and the mitigation of potential risks in diverse real-world scenarios.