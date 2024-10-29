import React from 'react';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Typography from '@mui/material/Typography';
import Checkbox from '@mui/material/Checkbox';
import FormControlLabel from '@mui/material/FormControlLabel';
import PersonOutlinedIcon from "@mui/icons-material/PersonOutlined";
import LockIcon from '@mui/icons-material/Lock';
import InputAdornment from '@mui/material/InputAdornment';
import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';

export default function LoginForm() {


    //Get cust credentials
    const navigate = useNavigate();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    //Handle cust login authentication
    const handleLogin = async (e) => {
        console.log({ email, password });
        e.preventDefault();
        try {
            const response = await fetch('https://theme-park-backend.ambitioussea-02dd25ab.eastus.azurecontainerapps.io/api/v1/emp-auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email, password }),
            });

            if (response.ok) {
                const data = await response.json();
                console.log('Login successful:', data);
                navigate('/employees');
            } else {
                const errorData = await response.json();
                console.error('Login failed with status:', response.status);
                console.error('Error details:', errorData);//see specifcc errors
                alert('Error message:', errorData.message || 'Unknown error'); //view error
            }
        } catch (error) {
            console.error('Login failed:', error);
            alert('An error occurred while logging in. Please try again later.');
        }
    };






    return (
        <Box 
            sx={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                height: '100vh', // Fill the viewport height for vertical centering
            }}
        >
            <Box 
                className='wrapper'
                sx={{
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    justifyContent: 'center',
                    width: '100%',
                    maxWidth: 700,
                    margin: '0 auto', // Center horizontally
                    padding: 6,
                    border: '1px solid #ccc',
                    borderRadius: 2,
                    boxShadow: 3,
                }}
            >
                <Typography variant="h4" gutterBottom marginBottom="35px">
                    Employee Sign In
                </Typography>

                <form onSubmit={handleLogin}>
                    <Box sx={{ mb: 2 }}>
                        <TextField
                            type="email"
                            placeholder='Email'
                            required
                            fullWidth
                            variant="outlined"
                            value={email} 
                            onChange={(e) => setEmail(e.target.value)}
                            InputProps={{
                                startAdornment: (
                                    <InputAdornment position="start">
                                        <PersonOutlinedIcon />
                                    </InputAdornment>
                                ),
                            }}
                            sx={{ mb: 2 }}
                        />

                        <TextField
                            type="password"
                            placeholder='Password'
                            required
                            fullWidth
                            variant="outlined"
                            value={password} //Bind to typing state
                            onChange={(e) => setPassword(e.target.value)} //update as typed
                            InputProps={{
                                startAdornment: (
                                    <InputAdornment position="start">
                                        <LockIcon />
                                    </InputAdornment>
                                ), 
                                inputProps: {
                                    minLength: 8, //Force min length requirement
                                },
                            }}
                            sx={{ mb: 2 }}
                        />
                    </Box>

                    <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                        <FormControlLabel
                            control={<Checkbox />}
                            label="Remember me"
                        />
                        <a href="#">Forgot Password?</a>
                    </Box>

                    <Box sx={{ mb: 2, display: 'flex', justifyContent: 'center'}}>
                    <Typography variant="h4" gutterBottom >
                        <Link to="#">Sign-in with OTP</Link>
                    </ Typography >
                    </Box>

                    <Button type="submit" variant="contained" fullWidth >
                        Sign In
                    </Button>
                </form>
            </Box>
        </Box>
    );
};
