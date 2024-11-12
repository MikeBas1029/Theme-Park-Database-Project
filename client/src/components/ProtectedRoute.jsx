import React, { useEffect, useState } from 'react';
import { Navigate } from 'react-router-dom';
import { useUser } from './context/UserContext';
import { Box, CircularProgress } from '@mui/material';
import Header from './Header';

const ProtectedRoute = ({ children, allowedRoles }) => {
    const { user } = useUser();
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
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

    // If the user doesn't have the necessary role, show an access denied message
    if (allowedRoles && !allowedRoles.includes(user.role)) {
        return (
            <Box m="20px">
                <Header title="Access Denied" subtitle="You do not have permission to view this page." />
                <p>Warning: ({user.role})s are not allowed access to this page. Any attempt at unathourized access will be kept note of ⚠️</p>
            </Box>
        );
    }
    

    // If user is authenticated and has the necessary roles render children
    return children;
};

export default ProtectedRoute;
