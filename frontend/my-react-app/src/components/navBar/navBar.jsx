import { useLocation, Link } from 'react-router-dom';
import './navBar.css';

const NavBar = () => {
    const location = useLocation();

    return (
        <div className="simple-navbar">
            <div className="heading-banner">
                <h1>Encryptodevs</h1>
            </div>
            <div className='signup-login'>
                {location.pathname !== '/signup' && (
                    <button className="signup-login-btn">
                        <Link to="/signup">Signup</Link>
                    </button>
                )}
                {location.pathname !== '/login' && (
                    <button className="signup-login-btn">
                        <Link to="/login">Login</Link>
                    </button>
                )}
            </div>
        </div>
    );
}

export default NavBar;
