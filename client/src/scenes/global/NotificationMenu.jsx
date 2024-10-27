import React, { useEffect, useState, useContext } from 'react';
import { Box, IconButton, useTheme } from '@mui/material';
import NotificationsOutlinedIcon from "@mui/icons-material/NotificationsOutlined";
import { DisplayModeContext, tokens } from '../../theme';

const NotificationMenu = ({ endpoint, buttonStyle, dropdownStyle, itemStyle }) => {
    const [notifications, setNotifications] = useState([]);
    const [isOpen, setIsOpen] = useState(false);
    const theme = useTheme();
    const colors = tokens(theme.palette.mode); 
    const colorMode = useContext(DisplayModeContext);

    useEffect(() => {
        const fetchNotifications = async () => {
            try {
                const response = await fetch(endpoint);
                const data = await response.json();
                setNotifications(data);
            } catch (error) {
                console.error('Error fetching notifications:', error);
            }
        };

        fetchNotifications();
    }, [endpoint]);

    const toggleMenu = () => {
        setIsOpen(!isOpen);
    };

    return (
        <Box position="relative">
            <IconButton onClick={toggleMenu} sx={{
                ...buttonStyle,
                '&:hover': {
                    backgroundColor: 'transparent', // disable hover bg
                    opacity: 1,
                },
            }}>
                <NotificationsOutlinedIcon /> 
            </IconButton>
            {isOpen && (
                <Box
                    sx={{
                        ...dropdownStyle,
                        position: 'absolute',
                        zIndex: 1000,
                        bgcolor: 'white',
                        border: '1px solid #ccc',
                        borderRadius: '5px',
                        width: '300px',
                        right: '100%', // Position to the left of the button
                        marginRight: '10px', // Optional: adds space between button and dropdown
                    }}
                >
                    {notifications.length === 0 ? (
                        <Box sx={{ padding: '10px', bgcolor: theme.palette.mode === 'dark' ? colors.primary[400] : 'white' }}>
                            No notifications
                        </Box>
                    ) : (
                        notifications.map((notification) => (
                            <Box key={notification.id} sx={itemStyle}>
                                <p>{notification.message}</p>
                                <small>{new Date(notification.date).toLocaleString()}</small>
                            </Box>
                        ))
                    )}
                </Box>
            )}
        </Box>
    );
};

export default NotificationMenu;
