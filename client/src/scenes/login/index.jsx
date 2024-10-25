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

export default function LoginPage() {
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
                    Customer Login
                </Typography>

                <form action="">
                    <Box sx={{ mb: 2 }}>
                        <TextField
                            type="email"
                            placeholder='Email'
                            required
                            fullWidth
                            variant="outlined"
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
                            InputProps={{
                                startAdornment: (
                                    <InputAdornment position="start">
                                        <LockIcon />
                                    </InputAdornment>
                                ),
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
                            <a href="#">Employee Sign in</a>
                    </ Typography >
                    </Box>

                    <Button type="submit" variant="contained" fullWidth  sx={{marginBottom: '10px', marginTop: '10px'}}>
                        Login
                    </Button>
                </form>
            </Box>
        </Box>
    );
};
