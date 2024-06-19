<<<<<<< HEAD
import React, {useState} from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
// import { createBrowserRouter, RouterProvider } from "react-router-dom";
import "./App.css";
import  SignUp  from "./pages/signup/signup.jsx";
import  Login  from "./pages/login/login.jsx";
import HomePage  from "./pages/homepage/homepage.jsx";
import PrivateMessageForm from "./components/privateMessageForm.jsx";
import Landing from './pages/landing_page/landing';
import ChatPage from './pages/chat';
import WebSocket from './components/WebSocket.js';
=======

import React from 'react';


import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import SignUp from './pages/signup/signup';
import Login from './pages/login/login';
import HomePage from './pages/homepage/homepage';
import Landing from './pages/landing_page/landing';

import ForgotPassword from './components/password/forgottenPassword';

import ResetPassword from './components/password/resetPassword';
import PrivateMessageForm from "./components/privateMessageForm.jsx";



import "./App.css";



>>>>>>> main

// docs: https://reactrouter.com/en/main/start/overview

const App = () => {
const [showLanding, setShowLanding] = useState(true);
  const [showWebSocket, setShowWebSocket] = useState(true);
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<SignUp />} />
        <Route path="/chat" element={<PrivateMessageForm />} />
        <Route path="/landing" element={<Landing />} />
<<<<<<< HEAD
        {/*<Route path="/chat" element={<ChatPage />} />*/}
=======
        <Route path="/forgot_password" element={<ForgotPassword />} />
        <Route path="/reset/:token" element={<ResetPassword />} />
        

>>>>>>> main
      </Routes>
    </Router>
  );
};

<<<<<<< HEAD
export default App;
=======
>>>>>>> main

