
import React from 'react';


import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import SignUp from './pages/signup/signup';
import Login from './pages/login/login';
import HomePage from './pages/homepage/homepage';
import Landing from './pages/landing_page/landing';

import ForgotPassword from './components/password/forgottenPassword/forgottenPassword.jsx';

import ResetPassword from './components/password/resetPassword/resetPassword.jsx';
import PrivateMessageForm from "./components/privateMessageForm.jsx";



import "./App.css";




// docs: https://reactrouter.com/en/main/start/overview

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<SignUp />} />
        <Route path="/test" element={<PrivateMessageForm />} />
        <Route path="/landing" element={<Landing />} />
        <Route path="/forgot_password" element={<ForgotPassword />} />
        <Route path="/reset/:token" element={<ResetPassword />} />
        

      </Routes>
    </Router>
  );
};


export default App