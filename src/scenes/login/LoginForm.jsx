import React from 'react'
import './LoginForm.css'
import PersonOutlinedIcon from "@mui/icons-material/PersonOutlined";
import LockIcon from '@mui/icons-material/Lock';

const LoginForm = () => {

    return (
        <div className='wrapper' >
            <form action="">
                <h1>Login</h1>

                <div className="input-box"> 
                    <PersonOutlinedIcon className='icon'/>
                    <input type="text" placeholder='Email or Username' required />
                </div>

                <div className="input-box">
                    <LockIcon className='icon' />
                    <input type="password" placeholder='Password' required/>
                </div>

                <div className="remember-forgot">
                    <label>
                        <input type="checkbox"/>
                        Remember me
                    </label>
                    <a href="#">Forgot Passowrd? </a>
                </div>

                <button type="submit">Login</button>
            </form>
        </div>

    );
};

export default LoginForm;
