import React, { useEffect, useState } from 'react';
import Carousel from "./Carousel.tsx";
import { Buffer } from 'buffer';

interface Props {
    buffer: Buffer;
}

const SimulationPresentation: React.FC<Props> = ({ buffer }) => {
    const [maps, setMaps] = useState<React.ReactNode[]>([]);

    useEffect(() => {
        setMaps([]); // Clear previous maps (if any

        const data = buffer.toString('utf-8');

        const items: React.ReactNode[] = [];

        let map = '';

        for (let line in data.split('\n')) {
            line = line.trim();
            if (line === '') {
                items.push(
                    <iframe
                        key={items.length}
                        title={`Simulation Frame ${items.length}`}
                        srcDoc={map.trim()} // Embed content directly using srcDoc
                        style={{ width: '100%', height: '500px', border: 'none' }}
                    />
                );
                map = '';
                continue;
            }
            if (line.includes('INFO')) {
                continue;
            }
            map += line + '\n';
        }

        setMaps(items);
    }, [buffer]);

    return (
        <>
            <h2>Simulation Results</h2>
            <Carousel items={maps}/>
        </>
    );
};

export default SimulationPresentation;
