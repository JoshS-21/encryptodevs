import React, { useState } from 'react';
import axios from 'axios';

const SignUp = () => {
    const [formData, setFormData] = useState({
        username: '',
        name: '',
        email: '',
        phone_number: '',
        password: ''
    });

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const signUp = (e) => {
        e.preventDefault();
        axios.post(`${process.env.REACT_APP_API_URL}/signup`, formData)
            .then(response => {
                alert(response.data.message);
                setFormData({
                    username: '',
                    name: '',
                    email: '',
                    phone_number: '',
                    password: ''
                });
            })
            .catch(error => {
                console.error('There was an error signing up the user!', error);
            });
    };

    return (
        <div>
            <h2>Sign Up</h2>
            <form onSubmit={signUp}>
                <input type="text" name="username" placeholder="Username" value={formData.username} onChange={handleChange} required />
                <input type="text" name="name" placeholder="Name" value={formData.name} onChange={handleChange} required />
                <input type="email" name="email" placeholder="Email" value={formData.email} onChange={handleChange} required />
                <input type="text" name="phone_number" placeholder="Phone Number" value={formData.phone_number} onChange={handleChange} required />
                <input type="password" name="password" placeholder="Password" value={formData.password} onChange={handleChange} required />
                <button type="submit">Sign Up</button>
            </form>
        </div>
    );
};

export default SignUp;