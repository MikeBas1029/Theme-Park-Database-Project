import React, { useEffect, useState } from 'react';
import { Navigate } from 'react-router-dom';
import { useUser } from './context/UserContext';
import { Box, CircularProgress } from '@mui/material';
import Header from './Header';

const ProtectedRoute = ({ children }) => {
    const { user } = useUser();
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        // Simulate loading time or wait for user data to be populated
        if (user) {
            setIsLoading(false);
        }
    }, [user]);

    // Show a loading indicator until user data is loaded
    if (isLoading) {
        return (
            <Box display="flex" justifyContent="center" alignItems="center" height="100vh">
                <CircularProgress />
            </Box>
        );
    }

    

    // Redirect to login if no user is found
    if (!user) {
        return <Navigate to="/emplogin" />;
    }

    // If no user or no userType, send to login
    if (!user || !user.userType) {
        return <Navigate to="/emplogin" />;
    }

    // If the user is a customer (has a userType but no role), send to customer home
    if (user.userType === 'customer' && !user.role) {
        return <Navigate to="/customerhome" />;
    }

        // If the user is a customer (has a userType but no role), send to customer home
    if (user.userType === 'employee' && user.role !== "admin") {
        return (
            <Box m="20px">
                <Header title="Access Denied" subtitle="You do not have permission to view this page." />
                You are just a {user.role}
            </Box>
        );;
    }

    // If user is authenticated and has the necessary role or permissions, render children
    return children;
};

export default ProtectedRoute;
