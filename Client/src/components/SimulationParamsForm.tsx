import React, { useState } from 'react';
import {
    Box,
    FormControl,
    FormLabel,
    Input,
    Button,
    Stack,
} from '@chakra-ui/react';

interface SimulationParams {
    number_of_people?: number;
    number_of_floors?: number;
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
}

interface SimulationParamsFormProps {
    onSubmit: (formData: SimulationParams) => void;
}

const SimulationParamsForm: React.FC<SimulationParamsFormProps> = ({ onSubmit }) => {
    const [formData, setFormData] = useState<SimulationParams>({});

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target;

        setFormData((prevFormData) => ({
            ...prevFormData,
            [name]: parseFloat(value) || undefined, // Parse value to float or undefined if empty
        }));
    };

    const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        onSubmit(formData);
    };

    return (
        <Box p={4} shadow="md" borderWidth="1px" borderRadius="md">
            <form onSubmit={handleSubmit}>
                <Stack spacing={4}>
                    <FormControl>
                        <FormLabel>Number of People</FormLabel>
                        <Input
                            type="number"
                            name="number_of_people"
                            value={formData.number_of_people || ''}
                            onChange={handleChange}
                        />
                    </FormControl>

                    <FormControl>
                        <FormLabel>Number of Floors</FormLabel>
                        <Input
                            type="number"
                            name="number_of_floors"
                            value={formData.number_of_floors || ''}
                            onChange={handleChange}
                        />
                    </FormControl>

                    <FormControl>
                        <FormLabel>Choice Mode</FormLabel>
                        <Input
                            type="number"
                            name="choice_mode"
                            value={formData.choice_mode || ''}
                            onChange={handleChange}
                        />
                    </FormControl>

                    <FormControl>
                        <FormLabel>Time for Firefighters</FormLabel>
                        <Input
                            type="number"
                            name="time_for_firefighters"
                            value={formData.time_for_firefighters || ''}
                            onChange={handleChange}
                        />
                    </FormControl>

                    <FormControl>
                        <FormLabel>Fire Spread Rate</FormLabel>
                        <Input
                            type="number"
                            name="fire_spread_rate"
                            value={formData.fire_spread_rate || ''}
                            onChange={handleChange}
                        />
                    </FormControl>

                    <FormControl>
                        <FormLabel>Max Visibility</FormLabel>
                        <Input
                            type="number"
                            name="max_visibility"
                            value={formData.max_visibility || ''}
                            onChange={handleChange}
                        />
                    </FormControl>

                    <FormControl>
                        <FormLabel>Min Visibility</FormLabel>
                        <Input
                            type="number"
                            name="min_visibility"
                            value={formData.min_visibility || ''}
                            onChange={handleChange}
                        />
                    </FormControl>

                    <FormControl>
                        <FormLabel>Max Strength</FormLabel>
                        <Input
                            type="number"
                            name="max_strength"
                            value={formData.max_strength || ''}
                            onChange={handleChange}
                        />
                    </FormControl>

                    <FormControl>
                        <FormLabel>Min Strength</FormLabel>
                        <Input
                            type="number"
                            name="min_strength"
                            value={formData.min_strength || ''}
                            onChange={handleChange}
                        />
                    </FormControl>

                    <FormControl>
                        <FormLabel>Max Speed</FormLabel>
                        <Input
                            type="number"
                            name="max_speed"
                            value={formData.max_speed || ''}
                            onChange={handleChange}
                        />
                    </FormControl>

                    <FormControl>
                        <FormLabel>Min Speed</FormLabel>
                        <Input
                            type="number"
                            name="min_speed"
                            value={formData.min_speed || ''}
                            onChange={handleChange}
                        />
                    </FormControl>

                    <FormControl>
                        <FormLabel>Max Fear</FormLabel>
                        <Input
                            type="number"
                            name="max_fear"
                            value={formData.max_fear || ''}
                            onChange={handleChange}
                        />
                    </FormControl>

                    <FormControl>
                        <FormLabel>Min Fear</FormLabel>
                        <Input
                            type="number"
                            name="min_fear"
                            value={formData.min_fear || ''}
                            onChange={handleChange}
                        />
                    </FormControl>

                    <FormControl>
                        <FormLabel>Max Age</FormLabel>
                        <Input
                            type="number"
                            name="max_age"
                            value={formData.max_age || ''}
                            onChange={handleChange}
                        />
                    </FormControl>

                    <FormControl>
                        <FormLabel>Min Age</FormLabel>
                        <Input
                            type="number"
                            name="min_age"
                            value={formData.min_age || ''}
                            onChange={handleChange}
                        />
                    </FormControl>

                    <FormControl>
                        <FormLabel>Max Health</FormLabel>
                        <Input
                            type="number"
                            name="max_health"
                            value={formData.max_health || ''}
                            onChange={handleChange}
                        />
                    </FormControl>

                    <FormControl>
                        <FormLabel>Min Health</FormLabel>
                        <Input
                            type="number"
                            name="min_health"
                            value={formData.min_health || ''}
                            onChange={handleChange}
                        />
                    </FormControl>

                    <FormControl>
                        <FormLabel>Likes People Probability</FormLabel>
                        <Input
                            type="number"
                            name="likes_people_probability"
                            value={formData.likes_people_probability || ''}
                            onChange={handleChange}
                        />
                    </FormControl>

                    <Button colorScheme="blue" type="submit">
                        Submit
                    </Button>
                </Stack>
            </form>
        </Box>
    );
};

export default SimulationParamsForm;
