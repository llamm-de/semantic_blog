import React, { useEffect, useState } from 'react';
import { Box, VStack, Input, Button, Text, Heading, HStack, Badge, Alert, AlertIcon } from '@chakra-ui/react';
import { getPosts, searchPosts } from '../../services/posts';
import { useNavigate } from 'react-router-dom';

function PostList() {
  const [posts, setPosts] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [isSearching, setIsSearching] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    loadPosts();
  }, []);

  const loadPosts = async () => {
    const data = await getPosts();
    setPosts(data.sort((a, b) => new Date(b.created_at) - new Date(a.created_at)));
    setIsSearching(false);
  };

  const handleSearch = async () => {
    if (searchQuery.trim()) {
      setIsSearching(true);
      const results = await searchPosts(searchQuery);
      const filteredResults = results
        .sort((a, b) => b.similarity_score - a.similarity_score)
        .map(result => ({
          ...result.post,
          similarity_score: result.similarity_score
        }));
      setPosts(filteredResults);
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
            <Badge colorScheme={post.similarity_score >= 0.75 ? 'green' : 
                              post.similarity_score >= 0.5 ? 'yellow' : 
                              post.similarity_score >= 0.25 ? 'orange' : 'red'}>
              {(post.similarity_score*100).toFixed(2)} % relevant
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
        {isSearching && posts.length === 0 ? (
          <Alert status="info">
            <AlertIcon />
            No similar posts found
          </Alert>
        ) : (
          posts.map(renderPostPreview)
        )}
      </VStack>
    </Box>
  );
}

export default PostList; 