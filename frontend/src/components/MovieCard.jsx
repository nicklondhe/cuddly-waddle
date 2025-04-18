import {
  Box,
  Text,
  useColorModeValue
} from '@chakra-ui/react';

import PropTypes from 'prop-types';

const MovieCard = ({ title, isSelected, onClick }) => {
  const bgColor = useColorModeValue('white', 'gray.700');
  const selectedBgColor = useColorModeValue('brand.100', 'brand.800');
  const borderColor = useColorModeValue('gray.200', 'gray.600');
  const selectedBorderColor = useColorModeValue('brand.500', 'brand.300');
  
  return (
    <Box
      p={3}
      bg={isSelected ? selectedBgColor : bgColor}
      borderRadius="md"
      border="2px solid"
      borderColor={isSelected ? selectedBorderColor : borderColor}
      cursor="pointer"
      onClick={onClick}
      transition="all 0.2s"
      _hover={{
        transform: 'translateY(-2px)',
        boxShadow: 'md',
        borderColor: isSelected ? selectedBorderColor : 'gray.300'
      }}
      height="80px"  // Fixed height
      display="flex"
      alignItems="center"
      justifyContent="center"
    >
      <Text
        fontWeight="medium"
        textAlign="center"
        fontSize="sm"  // Smaller font size
        noOfLines={3}  // Show max 3 lines
        overflow="hidden"
      >
        {title}
      </Text>
    </Box>
  );
};

MovieCard.propTypes = {
  title: PropTypes.string.isRequired,
  isSelected: PropTypes.bool.isRequired,
  onClick: PropTypes.func.isRequired
};

export default MovieCard;