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
  Spinner,
  Text,
  VStack,
  useColorModeValue
} from '@chakra-ui/react';
import { CheckIcon, CloseIcon, QuestionIcon, RepeatIcon } from '@chakra-ui/icons';
import {
  checkGuess,
  colorSchemes,
  getGroupTheme,
  initializeGameState,
  shuffleArray
} from '../game/gameLogic';
import { useEffect, useRef, useState } from 'react';

import MovieCard from './MovieCard';

const GameBoard = () => {
  const bgColor = useColorModeValue('gray.50', 'gray.900');
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [puzzleData, setPuzzleData] = useState(null);  
  const [movies, setMovies] = useState([]);
  const [completedGroups, setCompletedGroups] = useState([]);
  const [attemptsLeft, setAttemptsLeft] = useState(4);
  const [showHelp, setShowHelp] = useState(false);
  const [showError, setShowError] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const [isGameOver, setIsGameOver] = useState(false);
  const hasFetchedPuzzle = useRef(false);

  useEffect(() => {
    const fetchPuzzle = async () => {
        try {
            const response = await fetch ('/puzzle', {
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                  }
            });
            
            if (!response.ok) {
                throw new Error ('Failed to load puzzle!');
            }

            const data = await response.json();
            setPuzzleData(data);
            setMovies(initializeGameState(data.items));
            setIsLoading(false);
        } catch (err) {
            setError(err.message);
            setIsLoading(false);
        }
    };
    
    if (!hasFetchedPuzzle.current) {
        fetchPuzzle();
        hasFetchedPuzzle.current = true;
    }
  }, []);

  const handleMovieClick = (clickedId) => {
    setMovies(movies.map(movie => {
      if (movie.id === clickedId && movie.isSelected) {
        return { ...movie, isSelected: false };
      }
      
      const selectedCount = movies.filter(m => m.isSelected).length;
      if (movie.id === clickedId && selectedCount < 4) {
        return { ...movie, isSelected: true };
      }
      
      return movie;
    }));
  };

  const handleSubmit = () => {
    const selectedMovies = movies.filter(movie => movie.isSelected);
    const result = checkGuess(selectedMovies);

    if (!result.isCorrect) {
      if (result.message === 'Select exactly 4 movies') {
        setErrorMessage(result.message);
        setShowError(true);
        setTimeout(() => setShowError(false), 2000);
        return;
      }

      setAttemptsLeft(prev => {
        const newAttempts = prev - 1;
        if (newAttempts === 0) {
          setIsGameOver(true);
        }
        return newAttempts;
      });
      
      setErrorMessage(result.message);
      setShowError(true);
      setTimeout(() => setShowError(false), 2000);
      return;
    }

    // Handle correct guess
    const theme = getGroupTheme(puzzleData.groups, result.groupId);
    setCompletedGroups([...completedGroups, { 
      movies: selectedMovies,
      theme,
      groupId: result.groupId
    }]);

    setMovies(movies.map(movie => 
      selectedMovies.find(m => m.id === movie.id)
        ? { ...movie, isSelected: false, isCompleted: true }
        : movie
    ));
  };

  const handleClear = () => {
    setMovies(movies.map(movie => ({ ...movie, isSelected: false })));
  };

  const handleShuffle = () => {
    const uncompletedMovies = movies.filter(m => !m.isCompleted);
    const shuffledUncompleted = shuffleArray(uncompletedMovies);
    const newMovies = movies.map(movie => 
      movie.isCompleted ? movie : { ...shuffledUncompleted.pop(), isSelected: false }
    );
    setMovies(newMovies);
  };

  const restartGame = () => {
    setMovies(initializeGameState(puzzleData.items));
    setCompletedGroups([]);
    setAttemptsLeft(4);
    setIsGameOver(false);
    setShowError(false);
  };

  if (isLoading) {
    return (
      <Box
        position="fixed"
        top="50%"
        left="50%"
        transform="translate(-50%, -50%)"
      >
        <VStack spacing={4}>
          <Spinner
            thickness="4px"
            speed="0.65s"
            emptyColor="gray.200"
            color="blue.500"
            size="xl"
          />
          <Text>Loading puzzle...</Text>
        </VStack>
      </Box>
    );
  }

  if (error) {
    return (
      <Box
        position="fixed"
        top="50%"
        left="50%"
        transform="translate(-50%, -50%)"
      >
        <Text color="red.500">Error loading puzzle: {error}</Text>
      </Box>
    );
  }

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
                bg={attempt > attemptsLeft ? useColorModeValue("gray.800", "white") : useColorModeValue("white", "gray.800")}
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
            {completedGroups.map((group, index) => {
              const colorScheme = colorSchemes[index];
              return (
                <Box
                  key={group.groupId}
                  p={4}
                  mb={3}
                  bg={useColorModeValue(`${colorScheme}.50`, `${colorScheme}.900`)}
                  borderLeft="4px solid"
                  borderLeftColor={`${colorScheme}.500`}
                  borderRadius="md"
                  transition="all 0.2s"
                  _hover={{
                    transform: 'translateX(2px)',
                    boxShadow: 'sm'
                  }}
                >
                  <Heading size="sm" color={`${colorScheme}.500`} mb={1}>
                    {group.theme}
                  </Heading>
                  <Text 
                    fontSize="sm" 
                    color={useColorModeValue('gray.600', 'gray.300')}
                  >
                    {group.movies.map(m => m.text).join(' • ')}
                  </Text>
                </Box>
              );
            })}

            <Grid 
              templateColumns="repeat(4, 1fr)" 
              gap={4}
              mb={showError ? 4 : 0}
            >
              {movies.filter(m => !m.isCompleted).map(movie => (
                <MovieCard 
                  key={movie.id}
                  title={movie.text}
                  isSelected={movie.isSelected}
                  onClick={() => handleMovieClick(movie.id)}
                />
              ))}
            </Grid>

            {showError && (
              <Box
                textAlign="center"
                color={useColorModeValue("red.600", "red.300")}
                fontWeight="medium"
                fontSize="sm"
                py={2}
                px={4}
                bg={useColorModeValue("red.50", "rgba(254, 178, 178, 0.1)")}
                borderRadius="md"
              >
                {errorMessage}
              </Box>
            )}
          </Box>

          <HStack spacing={4} width="100%" justify="center" mt={2}>
            <Button
              leftIcon={<RepeatIcon />}
              colorScheme="purple"
              variant="solid"
              size="md"
              onClick={handleShuffle}
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
              onClick={handleSubmit}
              isDisabled={movies.filter(m => m.isSelected).length !== 4}
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

      <Modal isOpen={isGameOver} onClose={() => {}} isCentered closeOnOverlayClick={false}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Game Over!</ModalHeader>
          <ModalBody pb={6}>
            <Text mb={4}>
              You've run out of attempts. Here are the groups you found:
            </Text>
            {completedGroups.length > 0 ? (
              completedGroups.map(group => (
                <Box key={group.groupId} mb={3}>
                  <Text fontWeight="bold">{group.theme}</Text>
                  <Text fontSize="sm">{group.movies.map(m => m.text).join(', ')}</Text>
                </Box>
              ))
            ) : (
              <Text fontStyle="italic">No groups found</Text>
            )}
            
            <Text mt={4}>The remaining groups were:</Text>
            {puzzleData.groups
              .filter(g => !completedGroups.find(cg => cg.groupId === g.id))
              .map(group => (
                <Box key={group.id} mb={3}>
                  <Text fontWeight="bold">{group.theme}</Text>
                  <Text fontSize="sm">
                    {puzzleData.items
                      .filter(item => item.group_id === group.id)
                      .map(m => m.text)
                      .join(', ')}
                  </Text>
                </Box>
              ))}
          </ModalBody>
          <Button colorScheme="blue" m={5} onClick={restartGame}>
            Play Again
          </Button>
        </ModalContent>
      </Modal>
    </Box>
  );
};

export default GameBoard;