import {Request, Response} from "express";
import path from "path";
import {spawn} from "child_process";
import fs from "fs";
import express from "express";

const router = express.Router();

router.post('/run-python', (req: Request, res: Response) => {
    const {
        time_to_view_images = 0,
        number_of_people = 50,
        number_of_floors = 3,
        verbose = false,
        choice_mode = 2,
        time_for_firefighters = 50,
        fire_spread_rate = 0.01,
        max_visibility = 20,
        min_visibility = 15,
        max_strength = 10,
        min_strength = 1,
        max_speed = 5,
        min_speed = 1,
        max_fear = 10,
        min_fear = 1,
        max_age = 80,
        min_age = 18,
        max_health = 100,
        min_health = 80,
        likes_people_probability = 0.75,
        familiarity = 10,
        copycat = 0.125,
        cooperator = 0.125,
        detective = 0.125,
        simpleton = 0.125,
        cheater = 0.125,
        grudger = 0.125,
        copykitten = 0.125,
        random = 0.125
    }: SimulationParams = req.body;

    try {
        // Validate arguments
        validateArgs({
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
            random
        });

        // Path to your Python script
        const pythonScriptPath = path.join(__dirname, '../../Simulation/src/main.py');

        // Prepare arguments to pass to Python script
        const pythonArgs = [
            pythonScriptPath,
            `--time_to_view_images=${time_to_view_images}`,
            `--number_of_people=${number_of_people}`,
            `--number_of_floors=${number_of_floors}`,
            `--verbose=${verbose}`,
            `--choice_mode=${choice_mode}`,
            `--time_for_firefighters=${time_for_firefighters}`,
            `--fire_spread_rate=${fire_spread_rate}`,
            `--max_visibility=${max_visibility}`,
            `--min_visibility=${min_visibility}`,
            `--max_strength=${max_strength}`,
            `--min_strength=${min_strength}`,
            `--max_speed=${max_speed}`,
            `--min_speed=${min_speed}`,
            `--max_fear=${max_fear}`,
            `--min_fear=${min_fear}`,
            `--max_age=${max_age}`,
            `--min_age=${min_age}`,
            `--max_health=${max_health}`,
            `--min_health=${min_health}`,
            `--likes_people_probability=${likes_people_probability}`,
            `--familiarity=${familiarity}`,
            `--copycat=${copycat}`,
            `--cooperator=${cooperator}`,
            `--detective=${detective}`,
            `--simpleton=${simpleton}`,
            `--cheater=${cheater}`,
            `--grudger=${grudger}`,
            `--copykitten=${copykitten}`,
            `--random=${random}`
        ];

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

            // Read the output file with all the maps from the simulation
            const pathToOutputFile = '/path/to/output/file.txt'; // Replace with actual path
            fs.readFile(pathToOutputFile, 'utf8', (err, data) => {
                if (err) {
                    console.error('Error reading output file:', err);
                    return res.status(500).send('Error reading output file');
                }

                // Send the content of the output file back to the client
                res.send(data);
            });
        });

    } catch (error: any) {
        res.status(400).send(error.message);
    }
});

// Define type for request body
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

function validateArgs(args: SimulationParams): void {
    if (!args) {
        throw new Error("No arguments provided");
    }
    if (args.time_to_view_images !== undefined && args.time_to_view_images < 0) {
        throw new Error("Time to view images must be greater than or equal to 0");
    }
    if (args.max_visibility !== undefined && args.min_visibility !== undefined && args.max_visibility < args.min_visibility) {
        throw new Error("Max visibility must be greater than min visibility");
    }
    if (args.max_strength !== undefined && args.min_strength !== undefined && args.max_strength < args.min_strength) {
        throw new Error("Max strength must be greater than min strength");
    }
    if (args.max_speed !== undefined && args.min_speed !== undefined && args.max_speed < args.min_speed) {
        throw new Error("Max speed must be greater than min speed");
    }
    if (args.max_fear !== undefined && args.min_fear !== undefined && args.max_fear < args.min_fear) {
        throw new Error("Max fear must be greater than min fear");
    }
    if (args.max_age !== undefined && args.min_age !== undefined && args.max_age < args.min_age) {
        throw new Error("Max age must be greater than min age");
    }
    if (args.max_health !== undefined && args.min_health !== undefined && args.max_health < args.min_health) {
        throw new Error("Max health must be greater than min health");
    }
    if (args.likes_people_probability !== undefined && (args.likes_people_probability < 0 || args.likes_people_probability > 1)) {
        throw new Error("Likes people probability must be between 0 and 1");
    }
    if (args.familiarity !== undefined && args.familiarity < 0) {
        throw new Error("Familiarity must be greater than or equal to 0");
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
        throw new Error("Sum of all personalities must be approximately 1");
    }
    if (args.choice_mode !== undefined && (args.choice_mode < 0 || args.choice_mode > 3)) {
        throw new Error("Choice mode must be 0, 1, 2, or 3");
    }
    if (args.number_of_floors !== undefined && (args.number_of_floors < 1 || args.number_of_floors > 3)) {
        throw new Error("Number of floors must be between 1 and 3");
    }
}

export default router;