import { Request, Response, Router } from 'express';
import path from 'path';
import { spawn } from 'child_process';
import * as fs from "node:fs";

interface SimulationParams {
    time_to_view_images?: number;
    number_of_people?: number;
    number_of_floors?: number;
    verbose?: boolean;
    choice_mode?: number;
    time_for_firefighters?: number;
    fire_spread_rate?: number;
    max_visibility?: number;
    min_visibility?: number;
    max_strength?: number;
    min_strength?: number;
    max_speed?: number;
    min_speed?: number;
    max_fear?: number;
    min_fear?: number;
    max_age?: number;
    min_age?: number;
    max_health?: number;
    min_health?: number;
    likes_people_probability?: number;
    familiarity?: number;
    copycat?: number;
    cooperator?: number;
    detective?: number;
    simpleton?: number;
    cheater?: number;
    grudger?: number;
    copykitten?: number;
    random?: number;
}

interface Dto {
    time_to_view_images: any;
    number_of_people: any;
    number_of_floors: any;
    verbose: any;
    choice_mode: any;
    time_for_firefighters: any;
    fire_spread_rate: any;
    max_visibility: any;
    min_visibility: any;
    max_strength: any;
    min_strength: any;
    max_speed: any;
    min_speed: any;
    max_fear: any;
    min_fear: any;
    max_age: any;
    min_age: any;
    max_health: any;
    min_health: any;
    likes_people_probability: any;
    familiarity: any;
    copycat: any;
    cooperator: any;
    detective: any;
    simpleton: any;
    cheater: any;
    grudger: any;
    copykitten: any;
    random: any;
}

const router = Router();

router.post('/simulate', async (req: Request<{}, {}, Dto>, res: Response) => {
    const simulationParams = getSimulationParams(req.body);

    try {
        validateArgs(simulationParams);
    }
    catch (error) {
        res.status(400).send("Invalid arguments: " + error);
    }

    const pythonScriptPath = path.join(__dirname, '../Simulation/src/main.py');

    const pythonArgs = Object.entries(simulationParams).reduce((args, [key, value]) => {
        if (value !== undefined) {
            args.push(`--${key}=${value}`);
        }
        return args;
    }, [pythonScriptPath]);

    // Run Python script as a child process
    const pythonProcess = spawn('python', pythonArgs);

    // Handle data from Python script stdout
    pythonProcess.stdout.on('data', (data) => {
        console.log(`Python script output: ${data}`);
    });

    // Handle Python script exit
    pythonProcess.on('close', (code) => {
        console.log(`Python script exited with code ${code}`);
        res.send(`Python script exited with code ${code}`);

        // read file and get the run number
        let run = 0;
        fs.readFile('../Simulation/logs/run', 'utf8', function(err, data) {
            if (err) {
                console.error('Error reading file:', err);
                res.status(500).send('Error reading file');
            } else {
                console.log('File read successfully');
                run = parseInt(data);
            }
        })

        // Assuming the output file path is known and constant
        const pathToOutputFile = path.join(__dirname, `../Simulation/logs/run${run}/simulation/grid_image.html`);

        // Stream the file back to the client
        fs.readFile(pathToOutputFile, (err, data) => {
            if (err) {
                console.error('Error reading file:', err);
                res.status(500).send('Error reading file');
            } else {
                console.log('File read successfully');
                res.send(data);
            }
        })
    });
});

function getSimulationParams(body: Dto): SimulationParams {
    const defaultParams: SimulationParams = {
        time_to_view_images: 0,
        number_of_people: 50,
        number_of_floors: 3,
        verbose: false,
        choice_mode: 2,
        time_for_firefighters: 50,
        fire_spread_rate: 0.01,
        max_visibility: 20,
        min_visibility: 15,
        max_strength: 10,
        min_strength: 1,
        max_speed: 5,
        min_speed: 1,
        max_fear: 10,
        min_fear: 1,
        max_age: 80,
        min_age: 18,
        max_health: 100,
        min_health: 80,
        likes_people_probability: 0.75,
        familiarity: 10,
        copycat: 0.125,
        cooperator: 0.125,
        detective: 0.125,
        simpleton: 0.125,
        cheater: 0.125,
        grudger: 0.125,
        copykitten: 0.125,
        random: 0.125,
    };

    const {
        time_to_view_images,
        number_of_people,
        number_of_floors,
        verbose,
        choice_mode,
        time_for_firefighters,
        fire_spread_rate,
        max_visibility,
        min_visibility,
        max_strength,
        min_strength,
        max_speed,
        min_speed,
        max_fear,
        min_fear,
        max_age,
        min_age,
        max_health,
        min_health,
        likes_people_probability,
        familiarity,
        copycat,
        cooperator,
        detective,
        simpleton,
        cheater,
        grudger,
        copykitten,
        random,
    } = body;

    return {
        ...defaultParams,
        time_to_view_images,
        number_of_people,
        number_of_floors,
        verbose,
        choice_mode,
        time_for_firefighters,
        fire_spread_rate,
        max_visibility,
        min_visibility,
        max_strength,
        min_strength,
        max_speed,
        min_speed,
        max_fear,
        min_fear,
        max_age,
        min_age,
        max_health,
        min_health,
        likes_people_probability,
        familiarity,
        copycat,
        cooperator,
        detective,
        simpleton,
        cheater,
        grudger,
        copykitten,
        random,
    };
}

function validateArgs(args: SimulationParams): void {
    if (!args) {
        throw new Error('No arguments provided');
    }
    if (args.time_to_view_images !== undefined && args.time_to_view_images < 0) {
        throw new Error('Time to view images must be greater than or equal to 0');
    }
    if (args.max_visibility !== undefined && args.min_visibility !== undefined && args.max_visibility < args.min_visibility) {
        throw new Error('Max visibility must be greater than min visibility');
    }
    if (args.max_strength !== undefined && args.min_strength !== undefined && args.max_strength < args.min_strength) {
        throw new Error('Max strength must be greater than min strength');
    }
    if (args.max_speed !== undefined && args.min_speed !== undefined && args.max_speed < args.min_speed) {
        throw new Error('Max speed must be greater than min speed');
    }
    if (args.max_fear !== undefined && args.min_fear !== undefined && args.max_fear < args.min_fear) {
        throw new Error('Max fear must be greater than min fear');
    }
    if (args.max_age !== undefined && args.min_age !== undefined && args.max_age < args.min_age) {
        throw new Error('Max age must be greater than min age');
    }
    if (args.max_health !== undefined && args.min_health !== undefined && args.max_health < args.min_health) {
        throw new Error('Max health must be greater than min health');
    }
    if (args.likes_people_probability !== undefined && (args.likes_people_probability < 0 || args.likes_people_probability > 1)) {
        throw new Error('Likes people probability must be between 0 and 1');
    }
    if (args.familiarity !== undefined && args.familiarity < 0) {
        throw new Error('Familiarity must be greater than or equal to 0');
    }
    if (
        args.copycat !== undefined &&
        args.cooperator !== undefined &&
        args.detective !== undefined &&
        args.simpleton !== undefined &&
        args.cheater !== undefined &&
        args.grudger !== undefined &&
        args.copykitten !== undefined &&
        args.random !== undefined &&
        Math.abs(args.copycat + args.cooperator + args.detective + args.simpleton + args.cheater + args.grudger + args.copykitten + args.random - 1) > 0.001
    ) {
        throw new Error('Sum of all personalities must be approximately 1');
    }
    if (args.choice_mode !== undefined && (args.choice_mode < 0 || args.choice_mode > 3)) {
        throw new Error('Choice mode must be 0, 1, 2, or 3');
    }
    if (args.number_of_floors !== undefined && (args.number_of_floors < 1 || args.number_of_floors > 3)) {
        throw new Error('Number of floors must be between 1 and 3');
    }
}

export default router;
