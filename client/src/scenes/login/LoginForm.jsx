import React from 'react';
import './LoginForm.css';
import PersonOutlinedIcon from "@mui/icons-material/PersonOutlined";
import LockIcon from '@mui/icons-material/Lock';
import CloseIcon from '@mui/icons-material/Close';

const LoginForm = ({ onClose }) => {
    return (
        <div className='wrapper'>
            <button className='close-button' onClick={onClose}>
                <CloseIcon /> {/* Close button with icon */}
            </button>

            <form action="">
                <h1>Login</h1>

                <div className="input-box">
                    <PersonOutlinedIcon className='icon' />
                    <input type="text" placeholder='Email or Username' required />
                </div>

                <div className="input-box">
                    <LockIcon className='icon' />
                    <input type="password" placeholder='Password' required />
                </div>

                <div className="remember-forgot">
                    <label>
                        <input type="checkbox" />
                        Remember me
                    </label>
                    <a href="#">Forgot Password? </a>
                </div>

                <button type="submit">Login</button>
            </form>
        </div>
    );
};

export default LoginForm;
