import React, { useState, useEffect } from 'react';
import {
  Box,
  Button,
  FormControl,
  FormLabel,
  Input,
  VStack,
  Heading,
  Text,
  SimpleGrid,
  useToast,
} from '@chakra-ui/react';
import { useNavigate } from 'react-router-dom';
import { getUserProfile, updatePassword } from '../../services/auth';
import { getUserPosts, deletePost } from '../../services/posts';
import PostCard from '../Posts/PostCard';

function Profile() {
  const [profile, setProfile] = useState(null);
  const [posts, setPosts] = useState([]);
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const navigate = useNavigate();
  const toast = useToast();

  useEffect(() => {
    loadProfile();
    loadUserPosts();
  }, []);

  const loadProfile = async () => {
    try {
      const data = await getUserProfile();
      setProfile(data);
    } catch (error) {
      navigate('/login');
    }
  };

  const loadUserPosts = async () => {
    try {
      const data = await getUserPosts();
      setPosts(data);
    } catch (error) {
      console.error('Failed to load posts:', error);
    }
  };

  const handlePasswordChange = async (e) => {
    e.preventDefault();
    if (newPassword !== confirmPassword) {
      toast({
        title: 'Error',
        description: 'Passwords do not match',
        status: 'error',
        duration: 3000,
      });
      return;
    }

    try {
      await updatePassword({ password: newPassword });
      toast({
        title: 'Success',
        description: 'Password updated successfully',
        status: 'success',
        duration: 3000,
      });
      setNewPassword('');
      setConfirmPassword('');
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to update password',
        status: 'error',
        duration: 3000,
      });
    }
  };

  const handleDeletePost = async (postId) => {
    try {
      await deletePost(postId);
      loadUserPosts();
      toast({
        title: 'Success',
        description: 'Post deleted successfully',
        status: 'success',
        duration: 3000,
      });
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to delete post',
        status: 'error',
        duration: 3000,
      });
    }
  };

  if (!profile) return null;

  return (
    <Box>
      <VStack spacing={8} align="stretch">
        <Box>
          <Heading size="lg" mb={4}>Profile</Heading>
          <Text><strong>Email:</strong> {profile.email}</Text>
          <Text><strong>Username:</strong> {profile.username}</Text>
        </Box>

        <Box>
          <Heading size="md" mb={4}>Change Password</Heading>
          <form onSubmit={handlePasswordChange}>
            <VStack spacing={4} maxW="md">
              <FormControl isRequired>
                <FormLabel>New Password</FormLabel>
                <Input
                  type="password"
                  value={newPassword}
                  onChange={(e) => setNewPassword(e.target.value)}
                />
              </FormControl>
              <FormControl isRequired>
                <FormLabel>Confirm Password</FormLabel>
                <Input
                  type="password"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                />
              </FormControl>
              <Button type="submit" colorScheme="blue">
                Update Password
              </Button>
            </VStack>
          </form>
        </Box>

        <Box>
          <Heading size="md" mb={4}>My Posts</Heading>
          <SimpleGrid columns={[1, 2, 3]} spacing={4}>
            {posts.map((post) => (
              <PostCard
                key={post.id}
                post={post}
                onDelete={() => handleDeletePost(post.id)}
                showEditButton
              />
            ))}
          </SimpleGrid>
        </Box>
      </VStack>
    </Box>
  );
}

export default Profile; 