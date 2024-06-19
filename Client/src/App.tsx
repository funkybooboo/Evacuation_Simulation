import { Button, Container } from '@chakra-ui/react';
import SimulationParamsForm from './components/SimulationParamsForm';
import SimulationPresentation from './components/SimulationPresentation';
import SimulationParams from './types/simulationParams';
import { simulate } from './api/simulationService';
import { useState } from 'react';

function App() {
    const [newRequest, setNewRequest] = useState<boolean>(false);
    const [loading, setLoading] = useState<boolean>(false);
    const [buffer, setBuffer] = useState<Buffer | null>(null);
    const [seeSimulation, setSeeSimulation] = useState<boolean>(false);

    const handleSubmit = async (formData: SimulationParams) => {
        setNewRequest(false);
        setLoading(true);
        console.log('Form submitted with data:', formData);
        try {
            const response = await simulate(formData);
            // Assuming simulate returns the file data
            setBuffer(response);
        } catch (error) {
            console.error('Failed to simulate:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleNewRequest = () => {
        setNewRequest(true);
        setBuffer(null);
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
            {buffer && (
                <Button onClick={() => setSeeSimulation(true)}>See Simulation</Button>
            )}
            {seeSimulation && <SimulationPresentation buffer={buffer!} />}
        </Container>
    );
}

export default App;
