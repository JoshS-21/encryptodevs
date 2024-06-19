import React, {useEffect, useState} from "react";
import { useSearchParams } from 'react-router-dom';

const ChatPage = () => {
  const [searchParams] = useSearchParams();
  const user1 = searchParams.get('user1');
  const user2 = searchParams.get('user2');

  // Use user1 and user2 to render the chat interface

  return (
    <div>
      <h1>Chat Page</h1>
      <p>User 1: {user1}</p>
      <p>User 2: {user2}</p>
      {/* Render chat interface */}
    </div>
  );
};

export default ChatPage;