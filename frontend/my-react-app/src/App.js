import React from 'react';

import { createBrowserRouter, RouterProvider } from "react-router-dom";
import "./App.css";

import  SignUp  from "./pages/signup/signup.jsx";
import  Login  from "./pages/login/login.jsx";
import HomePage  from "./pages/homepage/homepage.jsx";
import Chat from "./components/Chat.jsx";

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
      <Chat/>
      
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

const App = () => {
  return (
    <RouterProvider router={router} />
  );
};

export default App;
