import React from 'react';
import { Navigate } from 'react-router-dom';
import { useUser } from './context/UserContext';

const ProtectedRoute = ({ children }) => {
    const { user } = useUser();

    
    // Check if `user` is being determined or logged in
    if (user === null) {
        return <div>Loading...</div>; // Add a loading indicator if `user` is still `null`
    }

    // If no user or no userType, send to login
    if (!user || !user.userType) {
        return <Navigate to="/emplogin" />;
    }

    // If the user is a customer (has a userType but no role), send to customer home
    if (user.userType === 'customer' && !user.role) {
        return <Navigate to="/customerhome" />;
    }

    // If user is authenticated and has the necessary role or permissions, render children
    return children;
};

export default ProtectedRoute;
