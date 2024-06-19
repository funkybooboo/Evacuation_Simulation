import axiosInstance from './axiosInstance';
import SimulationParams from '../types/simulationParams';

export async function simulate(params: SimulationParams): Promise<any> {
    try {
        const response = await axiosInstance.post('/simulate', params, {
            responseType: 'blob', // Ensure Axios treats the response as a blob (for files)
        });

        return response.data;

    } catch (error) {
        throw new Error(`Failed to simulate: ${error}`);
    }
}
