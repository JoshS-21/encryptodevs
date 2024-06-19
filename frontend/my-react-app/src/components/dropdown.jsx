import React, {useState} from 'react';
import './dropdown.css';
import {useNavigate} from 'react-router-dom';


const DropdownMenu = ({users, userData}) => {
    const [isOpen, setIsOpen] = useState(false);
    const navigate = useNavigate(); // initialise the useNavigate hook
    console.log(userData);
    console.log(users);

    // Toggle the dropdown menu
    const toggleDropdown = () => {
        console.log(userData);
        console.log(users);
        setIsOpen(!isOpen);
    };


    const handleItemClick = (clickedUser) => {
        console.log(`You clicked on ${clickedUser.username}`);
        setIsOpen(false);

        // Navigate to the 'chat' page with query parameters
        if (userData) {
          navigate(`/chat?user1=${userData.username}&user2=${clickedUser.username}`);
        } else {
          console.error('Current user data is not available');
        }
  };

    return (
        <div className="dropdown">
            <div className="dropdown-toggle" onClick={toggleDropdown}>
                Chat with...
                <span className="caret"/>
            </div>
            {isOpen && (
                <ul className="dropdown-menu">
                    {users
            .filter(user => user.is_online && user.username !== userData.username)
            .map((user, index) => (
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
