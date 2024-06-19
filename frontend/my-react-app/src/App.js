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
        {/*<Route path="/chat" element={<ChatPage />} />*/}
      </Routes>
    </Router>
  );
};

export default App;

