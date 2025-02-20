import {
  Box,
  Button,
  Grid,
  HStack,
  Heading,
  VStack,
  useColorModeValue
} from '@chakra-ui/react';
import { CheckIcon, CloseIcon, RepeatIcon } from '@chakra-ui/icons';

import MovieCard from './MovieCard';
import { useState } from 'react';

const dummyMovies = Array(16).fill(null).map((_, index) => ({
  id: `movie-${index}`,
  title: `Movie ${index + 1}`,
  isSelected: false
}));

const GameBoard = () => {
  const [movies, setMovies] = useState(dummyMovies);
  const bgColor = useColorModeValue('gray.50', 'gray.900');
  
  return (
    <Box
      position="fixed"
      top="50%"
      left="50%"
      transform="translate(-50%, -50%)"
      width="90%"
      maxWidth="600px"
    >
      <VStack spacing={5} align="center">
        <Heading 
          size="xl" 
          color={useColorModeValue("gray.800", "white")}
          textAlign="center"
          mb={2}
        >
          Bollywood Rishtey
        </Heading>

        <HStack spacing={2}>
          {[1, 2, 3, 4].map((attempt) => (
            <Box
              key={attempt}
              w="12px"
              h="12px"
              borderRadius="full"
              border="2px solid"
              borderColor={useColorModeValue("gray.800", "white")}
              bg={useColorModeValue("white", "gray.800")}
            />
          ))}
        </HStack>
        
        <Box 
          p={4} 
          bg={bgColor} 
          borderRadius="md" 
          boxShadow="md"
          width="100%"
        >
          <Grid 
            templateColumns="repeat(4, 1fr)" 
            gap={4}
          >
            {movies.map(movie => (
              <MovieCard 
                key={movie.id}
                title={movie.title}
                isSelected={movie.isSelected}
                onClick={() => {
                  // We'll implement selection logic later
                }}
              />
            ))}
          </Grid>
        </Box>

        <HStack spacing={4} width="100%" justify="center" mt={2}>
          <Button
            leftIcon={<RepeatIcon />}
            colorScheme="purple"
            variant="solid"
            size="md"
          >
            Shuffle
          </Button>
          <Button
            leftIcon={<CloseIcon />}
            colorScheme="red"
            variant="outline"
            size="md"
          >
            Clear
          </Button>
          <Button
            leftIcon={<CheckIcon />}
            colorScheme="green"
            variant="solid"
            size="md"
          >
            Submit
          </Button>
        </HStack>
      </VStack>
    </Box>
  );
};

export default GameBoard;