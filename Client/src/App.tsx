import { Button, Container } from '@chakra-ui/react';
import SimulationParamsForm from './components/SimulationParamsForm';
import SimulationPresentation from './components/SimulationPresentation';
import SimulationParams from './types/simulationParams';
import { simulate } from './api/simulationService';
import { useState } from 'react';

function App() {
    const [newRequest, setNewRequest] = useState<boolean>(false);
    const [loading, setLoading] = useState<boolean>(false);
    const [fileData, setFileData] = useState<Blob | null>(null);
    const [seeSimulation, setSeeSimulation] = useState<boolean>(false);

    const handleSubmit = async (formData: SimulationParams) => {
        setNewRequest(false);
        setLoading(true);
        console.log('Form submitted with data:', formData);
        try {
            const response = await simulate(formData);
            // Assuming simulate returns the file data
            setFileData(response);
        } catch (error) {
            console.error('Failed to simulate:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleNewRequest = () => {
        setNewRequest(true);
        setFileData(null);
        setSeeSimulation(false);
    };

    return (
        <Container maxW="lg" centerContent>
            {!newRequest && (
                <Button disabled={loading} onClick={handleNewRequest}>
                    New Request
                </Button>
            )}
            {newRequest && <SimulationParamsForm onSubmit={handleSubmit} />}
            {loading && <h2>Simulation running...</h2>}
            {fileData && (
                <Button onClick={() => setSeeSimulation(true)}>See Simulation</Button>
            )}
            {seeSimulation && <SimulationPresentation fileData={fileData!} />}
        </Container>
    );
}

export default App;
