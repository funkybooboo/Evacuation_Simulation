import React, { useEffect, useState } from 'react';
import Carousel from "./Carousel.tsx";

interface Props {
    fileData: Blob;
}

const SimulationPresentation: React.FC<Props> = ({ fileData }) => {
    const [carouselItems, setCarouselItems] = useState<React.ReactNode[]>([]);

    useEffect(() => {
        const reader = new FileReader();

        reader.onload = () => {
            if (reader.result) {
                const fileContent = reader.result as string;
                const lines = fileContent.split('\n');

                // Process each line
                lines.forEach((line, index) => {
                    if (line.includes('INFO')) {
                        // Create iframe element
                        const iframeElement = (
                            <iframe
                                key={index} // Ensure each iframe has a unique key
                                title={`Simulation ${index}`}
                                srcDoc={line} // Assuming line contains HTML content for iframe
                                width="100%"
                                height="600px"
                                frameBorder="0"
                            />
                        );

                        // Add iframe to carousel items
                        setCarouselItems((prevItems) => [...prevItems, iframeElement]);
                    }
                });
            }
        };

        reader.onerror = (event) => {
            console.error('Error reading blob:', event.target?.error);
        };

        // Read Blob as text
        reader.readAsText(fileData);
    }, [fileData]);

    return (
        <>
            <h2>Simulation Results</h2>
            <Carousel items={carouselItems}/>
        </>

    );
};

export default SimulationPresentation;
