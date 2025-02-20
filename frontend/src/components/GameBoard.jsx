import {
  Box,
  Button,
  Grid,
  HStack,
  Heading,
  IconButton,
  Modal,
  ModalBody,
  ModalCloseButton,
  ModalContent,
  ModalHeader,
  ModalOverlay,
  Text,
  VStack,
  useColorModeValue,
} from '@chakra-ui/react';
import { CheckIcon, CloseIcon, QuestionIcon, RepeatIcon } from '@chakra-ui/icons';

import MovieCard from './MovieCard';
import { useState } from 'react';

// Sample data
const sampleData = {
    "items": [
      {"id":"1-Hasee Toh Phasee","text":"Hasee Toh Phasee","group_id":1},
      {"id":"1-Khushi","text":"Khushi","group_id":1},
      {"id":"1-Bachna Ae Haseeno","text":"Bachna Ae Haseeno","group_id":1},
      {"id":"1-Aap Ki Khatir","text":"Aap Ki Khatir","group_id":1},
      {"id":"2-Sector 36","text":"Sector 36","group_id":2},
      {"id":"2-Baaz: A Bird in Danger","text":"Baaz: A Bird in Danger","group_id":2},
      {"id":"2-Supari","text":"Supari","group_id":2},
      {"id":"2-Gumraah","text":"Gumraah","group_id":2},
      {"id":"3-Liger","text":"Liger","group_id":3},
      {"id":"3-Crakk","text":"Crakk","group_id":3},
      {"id":"3-Toolsidas Junior","text":"Toolsidas Junior","group_id":3},
      {"id":"3-Ready","text":"Ready","group_id":3},
      {"id":"4-Lipstick Under My Burkha","text":"Lipstick Under My Burkha","group_id":4},
      {"id":"4-Ribbon","text":"Ribbon","group_id":4},
      {"id":"4-Hum Bhi Akele Tum Bhi Akele","text":"Hum Bhi Akele Tum Bhi Akele","group_id":4},
      {"id":"4-Sharmajee Ki Beti","text":"Sharmajee Ki Beti","group_id":4}
    ],
    "groups": [
      {"id":1,"theme":"Romantic comedies"},
      {"id":2,"theme":"Action thrillers"},
      {"id":3,"theme":"Sports dramas"},
      {"id":4,"theme":"Women-centric themes"}
    ]
  };

const GameBoard = () => {
    const [movies, setMovies] = useState(sampleData.items.map(item => ({
        ...item,
        isSelected: false
      })));
  const [showHelp, setShowHelp] = useState(false);
  const bgColor = useColorModeValue('gray.50', 'gray.900');

  const handleMovieClick = (clickedId) => {
    setMovies(movies.map(movie => {
      // If trying to deselect, always allow it
      if (movie.id === clickedId && movie.isSelected) {
        return { ...movie, isSelected: false };
      }
      
      // If trying to select, check if we already have 4 selected
      const selectedCount = movies.filter(m => m.isSelected).length;
      if (movie.id === clickedId && selectedCount < 4) {
        return { ...movie, isSelected: true };
      }
      
      return movie;
    }));
  };

  const handleClear = () => {
    setMovies(movies.map(movie => ({ ...movie, isSelected: false })));
  };
  
  return (
    <Box
      position="fixed"
      top="50%"
      left="50%"
      transform="translate(-50%, -50%)"
      width="90%"
      maxWidth="600px"
    >
      <Box position="relative">
        <IconButton
          icon={<QuestionIcon />}
          aria-label="Help"
          position="absolute"
          right="-10"
          top="-10"
          size="sm"
          isRound
          onClick={() => setShowHelp(true)}
        />
        
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
                  title={movie.text}
                  isSelected={movie.isSelected}
                  onClick={() => handleMovieClick(movie.id)}
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
              onClick={handleClear}
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

      <Modal isOpen={showHelp} onClose={() => setShowHelp(false)} isCentered>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>How to Play</ModalHeader>
          <ModalCloseButton />
          <ModalBody pb={6}>
            <Text mb={4}>
              Find groups of four movies that share something in common. Select four movies and hit submit to make a guess.
            </Text>
            <Text mb={4}>
              You have four attempts to find all four groups. Each incorrect guess uses one attempt.
            </Text>
            <Text>
              Examples of connections: Same Director, Same Actor, Similar Themes, Award Winners, etc.
            </Text>
          </ModalBody>
        </ModalContent>
      </Modal>
    </Box>
  );
};

export default GameBoard;