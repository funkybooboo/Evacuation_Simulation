# Fire Evacuation Simulation

## Directory Structure
- Backend: Contains the server and simulation logic
- Client: Contains the frontend code

## How to run the simulation with the GUI using Docker
1. Have Docker installed
2. Clone the repository
3. Run the docker-compose file
    - Go to the root directory
    - Run `docker compose up` or `docker-compose up` if the first command doesn't work
    - The client will start on `http://localhost:3001`

## How to manually run the simulation with the GUI
1. Clone the repository
2. Run the backend server
    - Go to the 'Backend/Api/' directory
    - Run `npm install`
    - Run `npm start`
    - The server will start on `http://localhost:3000`
3. Run the Client server
    - Go to the 'Client/' directory
    - Run `npm install`
    - Run `npm build`
    - The server will start on `http://localhost:3001`

## How to run the simulation with the CLI
1. Go to the 'Backend/Simulation' directory
- Run `python3 src/main.py`
