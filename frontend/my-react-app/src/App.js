import React from 'react';
<<<<<<< HEAD

import { createBrowserRouter, RouterProvider } from "react-router-dom";
import "./App.css";

import  SignUp  from "./pages/signup/signup.jsx";
import  Login  from "./pages/login/login.jsx";
import HomePage  from "./pages/homepage/homepage.jsx";
import PrivateMessageForm from "./components/privateMessageForm.jsx";

// docs: https://reactrouter.com/en/main/start/overview
const router = createBrowserRouter([
  {
    path: "/",
    element: 
    <>
      <HomePage/>
      
    </>
  },
  {
    path: "/test",
    element: 
    <>
      <PrivateMessageForm/>
      
    </>
  },
  {
    path: "/login",
    element: 
    <>
      <Login/>
      
    </>,
  },
  {
    path: "/signup",
    element: 
    <>
      
      <SignUp/>
    </>,
  },

]);
=======
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import SignUp from './pages/signup/signup';
import Login from './pages/login/login';
import HomePage from './pages/homepage/homepage';
import Landing from './pages/landing_page/landing';
>>>>>>> main

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<SignUp />} />
        <Route path="/landing" element={<Landing />} />
      </Routes>
    </Router>
  );
};

export default App;
