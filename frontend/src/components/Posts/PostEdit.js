import React, { useState, useEffect } from 'react';
import { Box, Button, FormControl, FormLabel, Input, Textarea, VStack } from '@chakra-ui/react';
import { useNavigate, useParams } from 'react-router-dom';
import { updatePost } from '../../services/posts';

function PostEdit() {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const navigate = useNavigate();
  const { id } = useParams();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await updatePost(id, { title, content });
      navigate('/');
    } catch (error) {
      alert('Failed to update post');
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
          <Button type="submit" colorScheme="blue">Update Post</Button>
        </VStack>
      </form>
    </Box>
  );
}

export default PostEdit; 