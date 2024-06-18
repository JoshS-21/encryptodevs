import React, { useState } from 'react';
import './dropdown.css';


const DropdownMenu = ({ users }) => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleDropdown = () => {
    setIsOpen(!isOpen);
  };


  const handleItemClick = (user) => {
    console.log(`You clicked on ${user.username}`);
    setIsOpen(false);
  };

  return (
    <div className="dropdown">
      <div className="dropdown-toggle" onClick={toggleDropdown}>
        Chat with...
        <span className="caret"/>
      </div>
      {isOpen && (
        <ul className="dropdown-menu">
          {users.filter(user => user.is_online).map((user, index) => (
            <li key={index} onClick={() => handleItemClick(user)}>
              {user.username}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default DropdownMenu;
