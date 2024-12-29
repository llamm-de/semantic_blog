import React, { useState } from 'react';
import {
  Box,
  Button,
  FormControl,
  FormLabel,
  Input,
  VStack,
  Text,
  List,
  ListItem,
  ListIcon,
  useToast,
} from '@chakra-ui/react';
import { CheckIcon, CloseIcon } from '@chakra-ui/icons';
import { useNavigate } from 'react-router-dom';
import { register } from '../../services/auth';

function Register() {
  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();
  const toast = useToast();

  // Password validation criteria
  const passwordCriteria = {
    length: password.length >= 8,
    uppercase: /[A-Z]/.test(password),
    lowercase: /[a-z]/.test(password),
    number: /\d/.test(password),
    special: /[!@#$%^&*(),.?":{}|<>]/.test(password),
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await register({ email, username, password });
      toast({
        title: 'Registration successful',
        description: 'Please log in with your credentials',
        status: 'success',
        duration: 3000,
      });
      navigate('/login');
    } catch (error) {
      const errorMessage = error.response?.data?.detail || 'Registration failed';
      toast({
        title: 'Registration failed',
        description: errorMessage,
        status: 'error',
        duration: 5000,
      });
    }
  };

  const renderPasswordRequirement = (label, met) => (
    <ListItem>
      <ListIcon as={met ? CheckIcon : CloseIcon} color={met ? 'green.500' : 'red.500'} />
      {label}
    </ListItem>
  );

  return (
    <Box maxW="md" mx="auto">
      <form onSubmit={handleSubmit}>
        <VStack spacing={4}>
          <FormControl isRequired>
            <FormLabel>Email</FormLabel>
            <Input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </FormControl>
          <FormControl isRequired>
            <FormLabel>Username</FormLabel>
            <Input
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
            <Text fontSize="sm" color="gray.600">
              Username must be 3-50 characters, using only letters, numbers, underscore, and hyphen
            </Text>
          </FormControl>
          <FormControl isRequired>
            <FormLabel>Password</FormLabel>
            <Input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            <Box mt={2}>
              <Text fontSize="sm" fontWeight="bold" mb={1}>
                Password requirements:
              </Text>
              <List spacing={1} fontSize="sm">
                {renderPasswordRequirement('At least 8 characters', passwordCriteria.length)}
                {renderPasswordRequirement('One uppercase letter', passwordCriteria.uppercase)}
                {renderPasswordRequirement('One lowercase letter', passwordCriteria.lowercase)}
                {renderPasswordRequirement('One number', passwordCriteria.number)}
                {renderPasswordRequirement('One special character (!@#$%^&*(),.?":{}|<>)', passwordCriteria.special)}
              </List>
            </Box>
          </FormControl>
          <Button 
            type="submit" 
            colorScheme="blue"
            isDisabled={!Object.values(passwordCriteria).every(Boolean)}
          >
            Register
          </Button>
        </VStack>
      </form>
    </Box>
  );
}

export default Register; 