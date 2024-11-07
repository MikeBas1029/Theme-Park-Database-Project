import React, { useEffect, useState, useContext } from 'react';
import { Box, IconButton, useTheme } from '@mui/material';
import NotificationsOutlinedIcon from "@mui/icons-material/NotificationsOutlined";
import { DisplayModeContext, tokens } from '../../theme';
import { useUser } from '../../components/context/UserContext';

const NotificationMenu = ({ buttonStyle, dropdownStyle, itemStyle }) => {
    const [notifications, setNotifications] = useState([]);
    const [isOpen, setIsOpen] = useState(false);
    const theme = useTheme();
    const colors = tokens(theme.palette.mode); 
    const colorMode = useContext(DisplayModeContext);
    const {user} = useUser();
    const { userType, customer_id, employee_id } = user || {}; // Destructure customer_id and employee_id based on userType


    useEffect(() => {
        const userId = userType === 'customer' ? customer_id : employee_id;
        if (!userType || !userId) return; // Ensure userType and userId exist before fetching

        const fetchNotifications = async () => {
            const endpoint = userType === 'customer'
                ? `https://theme-park-backend.ambitioussea-02dd25ab.eastus.azurecontainerapps.io/api/v1/cust-notifs/${userId}`
                : `https://theme-park-backend.ambitioussea-02dd25ab.eastus.azurecontainerapps.io/api/v1/emp-notifs/${userId}`;
            
            try  {
                const response = await fetch(endpoint, {
                    method: 'GET', 
                    headers: {
                        'Content-Type': 'application/json', 
                    },
                });
                
                if (!response.ok) {
                    if (response.status === 404) {
                        console.error('No notifications found for', userId);
                        setNotifications([]);
                    } else {
                        throw new Error(`Error: ${response.statusText}`);
                    }
                    return;
                }
    
                const data = await response.json();
                console.log("Data: ", data);
                setNotifications(data);
            } catch (error) {
                console.error('Error fetching notifications:', error);
            }
        };

        fetchNotifications();
    }, [userType, customer_id, employee_id]);


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
                            No notifications for {user.customer_id}
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