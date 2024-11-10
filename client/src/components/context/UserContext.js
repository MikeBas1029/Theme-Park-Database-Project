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
      customer_id: userType === 'customer' ? userData.customer_id : null, // Store customer ID if customers
      first_name: userData.first_name,  
      last_name: userData.last_name, 
      userType, // "employee" or "customer"
      role: userType === 'employee' ? userData.role : null, // Set role only for employees
      employee_id: userType === 'employee' ? userData.employee_id : null, // Employee ID/department if employee
      department: userType === 'employee' ? userData.department : null, 

  };

  setUser(formattedUserData);
  localStorage.setItem('user_data', JSON.stringify(formattedUserData)); // Store user data in local storage
  localStorage.setItem('user_type', userType); // Store type
}, []);



  // Function to log out and clear user data
  const logout = () => {
    setUser(null);
    // Clear user data from local storage
    localStorage.removeItem('user_data'); 
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user_type');
  };


  useEffect(() => {
    const storedUserData = localStorage.getItem('user_data');
    const storedUserType = localStorage.getItem('user_type');
    
    if (storedUserData && storedUserType) {
        const userData = JSON.parse(storedUserData);
        login(userData, storedUserType); // Set user data in context
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
