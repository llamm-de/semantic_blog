import React, { useEffect, useState } from 'react';
import { Box, VStack, Input, Button, Text, Heading, HStack, Badge } from '@chakra-ui/react';
import { getPosts, searchPosts } from '../../services/posts';
import { useNavigate } from 'react-router-dom';

function PostList() {
  const [posts, setPosts] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    loadPosts();
  }, []);

  const loadPosts = async () => {
    const data = await getPosts();
    setPosts(data.sort((a, b) => new Date(b.created_at) - new Date(a.created_at)));
  };

  const handleSearch = async () => {
    if (searchQuery.trim()) {
      const results = await searchPosts(searchQuery);
      // Sort results by similarity score and take top 5
      const sortedResults = results
        .sort((a, b) => b.similarity_score - a.similarity_score)
        .slice(0, 5);
      setPosts(sortedResults.map(result => ({
        ...result.post,
        similarity_score: result.similarity_score
      })));
    } else {
      loadPosts();
    }
  };

  const renderPostPreview = (post) => {
    const createdAt = new Date(post.created_at).toLocaleDateString();
    const previewContent = post.content.length > 200 
      ? post.content.substring(0, 200) + '...'
      : post.content;

    return (
      <Box 
        key={post.id}
        p={5}
        shadow="md"
        borderWidth="1px"
        borderRadius="md"
        cursor="pointer"
        onClick={() => navigate(`/posts/${post.id}`)}
        _hover={{ shadow: 'lg' }}
      >
        <Heading size="md" mb={2}>{post.title}</Heading>
        <Text color="gray.600" mb={3}>{previewContent}</Text>
        <HStack spacing={4}>
          <Badge colorScheme="blue">By {post.author?.username || 'Unknown'}</Badge>
          <Text fontSize="sm" color="gray.500">{createdAt}</Text>
          {post.similarity_score !== undefined && (
            <Badge colorScheme="green">
              {(post.similarity_score * 100).toFixed(1)}% match
            </Badge>
          )}
        </HStack>
      </Box>
    );
  };

  return (
    <Box>
      <Box mb={4}>
        <Input
          placeholder="Search posts..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          mr={2}
        />
        <Button onClick={handleSearch}>Search</Button>
      </Box>
      <VStack spacing={4} align="stretch">
        {posts.map(renderPostPreview)}
      </VStack>
    </Box>
  );
}

export default PostList; 