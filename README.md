CS5110 Project: Fire Evacuation Simulation 
Details and Information Document
Authors: Nate Stott and Rylei Mindrum

Objective of the Code
Our project aims to facilitate simulations of evacuations in the event of a fire outbreak.
Evacuation accidents pose a perpetual threat to society, and providing designers with the ability
to finely adjust simulation parameters to anticipate outcomes in emergency scenarios is crucial.
Preventing injury or even death would be the goal of designers. Our code aims to give them a
tool to predict what would happen given their parameters. Our simulation allows users to observe
how various types of individuals react in diverse situations. The research paper that we based our
simulation off of focuses on preventing stampedes in emergencies, we've expanded the concept
by introducing more complex behaviors among the agents in the simulation. Some complex
behaviors added include: being able to ask for help finding an exit or stair, fighting with game
theory rules, being able to jump out of windows if the agent deems it necessary, and so much
more. These behaviors are used to enhance the simulation's effectiveness in measuring a likely
outcome. The program measures numerous factors and gauges how well the evacuation went.
Metrics recorded include: the number of people, fire speed, individual attributes, behavioral
tendencies, and more. So much data is recorded in fact that it would be impractical for a human
to go through all the necessary data to see how things went. Data analysis tools could be used to
comb through the data and determine what happened during the evacuation simulation. Our
recorded data is broken up into relevant files. Making it easy to find the information you are
looking for. Our simulation could be expanded to include more choices for agents, more data
recorded, and other ideas as requested by the Designer. We are confident that our project could
be expanded to be a real asset to society. Allowing Designers to see what would happen in the
worst case scenario in their building before it's even built.

Description of the Simulation
The simulation operates on a 3D grid representing a building that is populated with
individuals. The building consists of multiple floors, each containing numerous rooms and
hallways. Individuals vary in their familiarity with the building and adherence to evacuation
plans. A fire initiates randomly on the map and progressively spreads over time. Individuals
assess their surroundings and make decisions on evacuation routes. They utilize environmental
memory for decision-making. We followed the see-think-act model for agents. In unfamiliar
surroundings, they can explore to find stairs or exits. Conflict avoidance and physical
confrontation are modeled behaviors determined by an agent's ability to get to an exit without
hitting other agents first. If unable to get to the desired location, and they want to fight, they can
compete with an agent over a location. Individuals trapped in rooms with fires attempt to escape
via doors or windows, stronger individuals are capable of breaking windows or even attempting
to pass through fires at a great cost of health. Fear and health status influence decision-making,
with frightened individuals exhibiting more irrational behaviors. The simulation continues until
all individuals exit the building, die, or the firefighters arrive.
We allow agents to make decisions in a number of ways as selected by the operator of the
simulation: All agents choose randomly, by ChatGPT, by logical statements, or by the operator
making the choice for the agent themselves! This is exciting because there is not just one way
that your simulation could turn out given the same starting parameters, agents will make different
decisions depending on what choice mode you have selected. This gives the operator the ability
to select how agents make choices.

How to Run
● Fork the project and run in your IDE of choice
● Go to Main.py
● Adjust the default parameters in get_args to your liking
● Hit play!

Expanding the Simulation
● Introducing other emergency scenarios such as earthquakes, floods, or terrorist attacks.
● Modeling familial relationships among individuals to simulate group dynamics and
decision-making processes.
● Incorporating disabilities among individuals to account for different mobility levels and
evacuation challenges.
● Allowing individuals to carry objects such as personal belongings, pets, or emergency
supplies, affecting their mobility and decision-making.
● Enhancing interpersonal relationships among individuals to simulate cooperation,
leadership, or conflicts during evacuations.
● Fine-tuning individual attributes such as strengths, weaknesses, health conditions, and
fears to create more nuanced behaviors and responses.
● Enriching environmental details with additional objects, diverse terrain types, and
weather effects to simulate realistic evacuation scenarios.
● Implementing dynamic environmental changes, such as complex fire spread patterns, and
extinguishing efforts by individuals or emergency responders.
● Facilitating information sharing among individuals about the environment, emergency
procedures, and safe evacuation routes to promote collaboration and collective
decision-making.
● Exit knowledge based on the path of entry to a current location; people should know the
path they took to get in and be able to use it to get out.
● There are many more, but we don't want to bore you!

Significance of the Output
The simulation output serves as a valuable resource for understanding the impact of
various factors on evacuation outcomes. Insights gained can inform better building designs,
emergency training protocols, and evacuation strategies; ultimately enhancing preparedness and
safety measures. Moreover, the expanded simulation capabilities offer opportunities for
interdisciplinary research and collaboration across fields such as urban planning, disaster
management, and human behavior studies. By continuously refining and expanding the
simulation, we contribute to the development of more effective emergency response strategies
and the mitigation of potential risks in diverse real-world scenarios. All before the building is
even built and someone has the opportunity to get hurt.
