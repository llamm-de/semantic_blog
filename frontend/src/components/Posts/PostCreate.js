import React, { useState } from 'react';
import { Box, Button, FormControl, FormLabel, Input, Textarea, VStack } from '@chakra-ui/react';
import { useNavigate } from 'react-router-dom';
import { createPost } from '../../services/posts';

function PostCreate() {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await createPost({ title, content });
      navigate('/');
    } catch (error) {
      alert('Failed to create post');
    }
  };

  return (
    <Box maxW="2xl" mx="auto">
      <form onSubmit={handleSubmit}>
        <VStack spacing={4}>
          <FormControl isRequired>
            <FormLabel>Title</FormLabel>
            <Input
              value={title}
              onChange={(e) => setTitle(e.target.value)}
            />
          </FormControl>
          <FormControl isRequired>
            <FormLabel>Content</FormLabel>
            <Textarea
              value={content}
              onChange={(e) => setContent(e.target.value)}
              minH="200px"
            />
          </FormControl>
          <Button type="submit" colorScheme="blue">Create Post</Button>
        </VStack>
      </form>
    </Box>
  );
}

export default PostCreate; 