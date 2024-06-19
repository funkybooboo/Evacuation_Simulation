import axios from 'axios';

const axiosInstance = axios.create({
    baseURL: 'http://localhost:3000/',
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json',
        // Add any headers common to all API requests
    },
});

export default axiosInstance;
