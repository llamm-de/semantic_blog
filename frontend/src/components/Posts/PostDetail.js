import React, { useState, useEffect } from 'react';
import { 
  Box, 
  Heading, 
  Text, 
  Button, 
  VStack,
  HStack,
  Badge,
  Divider 
} from '@chakra-ui/react';
import { useParams, useNavigate } from 'react-router-dom';
import { getPost } from '../../services/posts';

function PostDetail() {
  const [post, setPost] = useState(null);
  const { id } = useParams();
  const navigate = useNavigate();
  const isAuthor = post?.author_id === parseInt(localStorage.getItem('userId'));

  useEffect(() => {
    loadPost();
  }, [id]);

  const loadPost = async () => {
    try {
      const data = await getPost(id);
      setPost(data);
    } catch (error) {
      navigate('/');
    }
  };

  if (!post) return null;

  const createdAt = new Date(post.created_at).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });

  return (
    <Box maxW="3xl" mx="auto">
      <VStack align="stretch" spacing={6}>
        <Box>
          <Heading size="2xl">{post.title}</Heading>
          <HStack mt={4} spacing={4}>
            <Badge colorScheme="blue">By {post.author?.username || 'Unknown'}</Badge>
            <Text color="gray.600">{createdAt}</Text>
          </HStack>
        </Box>
        
        <Divider />
        
        <Text fontSize="lg" whiteSpace="pre-wrap">
          {post.content}
        </Text>

        <HStack spacing={4}>
          <Button onClick={() => navigate('/')}>Back to Posts</Button>
          {isAuthor && (
            <>
              <Button 
                colorScheme="blue"
                onClick={() => navigate(`/posts/edit/${post.id}`)}
              >
                Edit
              </Button>
            </>
          )}
        </HStack>
      </VStack>
    </Box>
  );
}

export default PostDetail; 