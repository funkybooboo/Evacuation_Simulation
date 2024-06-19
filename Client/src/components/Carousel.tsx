import React from 'react';
import Slider from 'react-slick';
import 'slick-carousel/slick/slick.css';
import 'slick-carousel/slick/slick-theme.css';
import { Box, Text } from '@chakra-ui/react'; // Import ChakraUI components as needed

interface Props {
    items: React.ReactNode[];
}

const Carousel: React.FC<Props> = ({ items }) => {
    const settings = {
        dots: false,
        infinite: false,
        speed: 500,
        slidesToShow: 1,
        slidesToScroll: 1,
        adaptiveHeight: true,
        autoplay: false,
        autoplaySpeed: 5000,
        arrows: true, // Change to false if you don't want arrows
    };

    return (
        <Box>
            <Slider {...settings}>
                {items.length > 0 ? (
                    items.map((item, index) => (
                        <Box key={index} p={4}>
                            {item}
                        </Box>
                    ))
                ) : (
                    <Text>No simulation data available.</Text>
                )}
            </Slider>
        </Box>
    );
};

export default Carousel;
