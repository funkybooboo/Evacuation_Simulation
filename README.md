# Fire Evacuation Simulation

## Directory Structure
- 'Api/' contains the backend code written with TypeScript & Express using Node.js.
- 'Client/' contains the frontend code written in TypeScript & React.
- 'Simulation/' contains the simulation code write in python.
- 'Scripts/' contains the scripts to run the simulation with the CLI or GUI without having to manually run commands.

## How to run the simulation with the GUI
1. Clone the repository
2. Run the backend server
    - Go to the 'Api/' directory
    - Run `npm install`
    - Run `npm start`
    - The server will start on `http://localhost:3000`
3. Run the Client server
    - Go to the 'Client/' directory
    - Run `npm install`
    - Run `npm start`
    - The server will start on `http://localhost:3001`

## How to run the simulation with the CLI
1. Go to the 'Simulation/' directory
- Run `src/python3 main.py`
