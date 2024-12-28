import React from 'react';
import { Box, Heading, Text, Button, HStack } from '@chakra-ui/react';
import { useNavigate } from 'react-router-dom';
import { deletePost } from '../../services/posts';

function PostCard({ post, similarity_score, onDelete }) {
  const navigate = useNavigate();
  const isAuthor = post.author_id === parseInt(localStorage.getItem('userId'));

  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete this post?')) {
      await deletePost(post.id);
      onDelete();
    }
  };

  return (
    <Box borderWidth="1px" borderRadius="lg" p={4}>
      <Heading size="md">{post.title}</Heading>
      <Text mt={2}>{post.content}</Text>
      {similarity_score !== undefined && (
        <Text mt={2} color="gray.600" fontSize="sm">
          Relevance: {(similarity_score * 100).toFixed(1)}%
        </Text>
      )}
      {isAuthor && (
        <HStack mt={4}>
          <Button onClick={() => navigate(`/posts/edit/${post.id}`)}>Edit</Button>
          <Button onClick={handleDelete} colorScheme="red">Delete</Button>
        </HStack>
      )}
    </Box>
  );
}

export default PostCard; 