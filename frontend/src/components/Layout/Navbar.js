import React from 'react';
import { Box, Button, Flex, Heading, Spacer } from '@chakra-ui/react';
import { Link, useNavigate } from 'react-router-dom';

function Navbar() {
  const navigate = useNavigate();
  const token = localStorage.getItem('token');

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('userId');
    navigate('/login');
  };

  return (
    <Box bg="gray.100" px={4} py={4}>
      <Flex maxW="container.xl" mx="auto" alignItems="center">
        <Box cursor="pointer" onClick={() => navigate('/')}>
          <Heading size="md">Semantic Blog</Heading>
        </Box>
        <Spacer />
        {token ? (
          <Flex gap={4}>
            <Button as={Link} to="/profile">Profile</Button>
            <Button as={Link} to="/posts/create" colorScheme="blue">
              Create Post
            </Button>
            <Button onClick={handleLogout}>Logout</Button>
          </Flex>
        ) : (
          <Flex gap={4}>
            <Button as={Link} to="/login">Login</Button>
            <Button as={Link} to="/register" colorScheme="blue">Register</Button>
          </Flex>
        )}
      </Flex>
    </Box>
  );
}

export default Navbar; 