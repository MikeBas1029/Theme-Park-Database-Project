import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';

// Create a context for user data
const UserContext = createContext(null);

// Create a custom hook to access the user context
export const useUser = () => useContext(UserContext);



export const UserProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  

  // Function to log in and set user data
  const login = useCallback((userData) => {
    const formattedUserData = {
      email: userData.email,
      uid: userData.uid,
      customer_id: userData.customer_id, // Store customer ID
      first_name: userData.first_name,  //Store user's name
      last_name: userData.last_name, 
  };

  setUser(formattedUserData);
  localStorage.setItem('user_data', JSON.stringify(formattedUserData)); // Store user data in local storage

    // Other login logic
}, []);



  // Function to log out and clear user data
  const logout = () => {
    setUser(null);
    localStorage.removeItem('user_data'); // Clear user data from local storage
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  };


  useEffect(() => {
    const storedUserData = localStorage.getItem('user_data');
    if (storedUserData) {
        const userData = JSON.parse(storedUserData);
        login(userData); // Set user data in your context or state
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
