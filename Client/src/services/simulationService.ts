import axiosInstance from './axiosInstance';
import SimulationParams from '../types/simulationParams';

export async function simulate(params: SimulationParams): Promise<any> {
    const url = '/simulate';
    const response = await axiosInstance.post(url, params, {
        responseType: 'arraybuffer', // Ensure Axios treats response as a buffer
    });
    if (Buffer.isBuffer(response.data)) {
        return response.data;
    }
    throw new Error('Invalid response data');
}
