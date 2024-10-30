import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';

// Context for user data
const UserContext = createContext(null);

// Custom hook to access the user context
export const useUser = () => useContext(UserContext);



export const UserProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  

  // Function to log in and set user data
  const login = useCallback((userData, userType) => {
    const formattedUserData = {
      email: userData.email,
      uid: userData.uid,
      customer_id: userData.customer_id, // Store customer ID
      first_name: userData.first_name,  //Store user's name
      last_name: userData.last_name, 
      userType, // Add userType here
  };

  setUser(formattedUserData);
  localStorage.setItem('user_data', JSON.stringify(formattedUserData)); // Store user data in local storage

}, []);



  // Function to log out and clear user data
  const logout = () => {
    setUser(null);
    // Clear user data from local storage
    localStorage.removeItem('user_data'); 
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  };


  useEffect(() => {
    const storedUserData = localStorage.getItem('user_data');
    if (storedUserData) {
        const userData = JSON.parse(storedUserData);
        login(userData); //set userData in context
    }
},
 [login]
);


  return (
    <UserContext.Provider value={{ user, login, logout }}>
      {children}
    </UserContext.Provider>
  );
};
