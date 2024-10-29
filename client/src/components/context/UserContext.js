import React, { createContext, useContext, useState } from 'react';

// Create a context for user data
const UserContext = createContext(null);

// Create a custom hook to access the user context
export const useUser = () => useContext(UserContext);



export const UserProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  

  // Function to log in and set user data
  const login = (userData) => {
    setUser({
      email: userData.email,
      uid: userData.uid,
  });
  };

  // Function to log out and clear user data
  const logout = () => {
    setUser(null);
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  };

  return (
    <UserContext.Provider value={{ user, login, logout }}>
      {children}
    </UserContext.Provider>
  );
};
