import React from 'react';
import { ChakraProvider } from '@chakra-ui/react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Layout/Navbar';
import Container from './components/Layout/Container';
import PostList from './components/Posts/PostList';
import PostCreate from './components/Posts/PostCreate';
import PostEdit from './components/Posts/PostEdit';
import PostDetail from './components/Posts/PostDetail';
import Login from './components/Auth/Login';
import Register from './components/Auth/Register';
import Profile from './components/Auth/Profile';

function App() {
  return (
    <ChakraProvider>
      <Router>
        <Navbar />
        <Container>
          <Routes>
            <Route path="/" element={<PostList />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/profile" element={<Profile />} />
            <Route path="/posts/create" element={<PostCreate />} />
            <Route path="/posts/edit/:id" element={<PostEdit />} />
            <Route path="/posts/:id" element={<PostDetail />} />
          </Routes>
        </Container>
      </Router>
    </ChakraProvider>
  );
}

export default App; 