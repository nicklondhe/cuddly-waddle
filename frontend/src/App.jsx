import { Box, ChakraProvider } from '@chakra-ui/react';
import GameBoard from './components/GameBoard';

function App() {
  return (
    <ChakraProvider>
      <Box bg="white" minH="100vh">
        <GameBoard />
      </Box>
    </ChakraProvider>
  );
}

export default App;