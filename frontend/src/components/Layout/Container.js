import React from 'react';
import { Container as ChakraContainer } from '@chakra-ui/react';

function Container({ children }) {
  return (
    <ChakraContainer maxW="container.xl" py={4}>
      {children}
    </ChakraContainer>
  );
}

export default Container; 