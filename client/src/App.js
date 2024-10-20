import { Routes, Route, useNavigate } from "react-router-dom"; // Added `useNavigate` import
import { DisplayModeContext, useMode } from "./theme";
import { CssBaseline, ThemeProvider } from "@mui/material";
import Navbar from "./scenes/global/Navbar";
import Sidebar from "./scenes/global/Sidebar";
import Dashboard from "./scenes/dashboard";
import LoginForm from "./scenes/login/LoginForm";
import Employees from "./scenes/employees";
import Vendors from "./scenes/vendors";
import TransactionSelection from "./scenes/transactions/transactionSelection";
import Invoices from "./scenes/invoices";
import Form from "./scenes/form";
import Inventory from "./scenes/inventory";
import React from "react";

function App() {
  const [theme, colorMode] = useMode();
  const navigate = useNavigate(); // Declare useNavigate to control navigation

  // Function to close the LoginForm and navigate away from /login
  const handleLoginClose = () => {
    navigate('/'); // Navigate back to home (dashboard)
  };

  return (
      <DisplayModeContext.Provider value={colorMode}>
        <ThemeProvider theme={theme}>
          <CssBaseline />
          <div className="app">
            <Sidebar />
            <main className="content">
              <Navbar />
              <Routes>
                <Route path="/" element={<Dashboard />} /> {/* Dashboard routing */}
                <Route path="/employees" element={<Employees />} /> {/* Employee page routing */}
                <Route path="/vendors" element={<Vendors />} /> {/* Vendors page routing */}
                <Route path="/login" element={<LoginForm onClose={handleLoginClose} />} /> {/* Login form routing */}
                <Route path="/transactions" element={<TransactionSelection />} /> {/* Transactions main page routing */}
                <Route path="/invoices" element={<Invoices />} /> {/* Invoice page routing */}
                <Route path="/form" element={<Form />} /> {/* Employee creation form routing */}
                <Route path="/inventory" element={<Inventory />} />
              </Routes>
            </main>
          </div>
        </ThemeProvider>
      </DisplayModeContext.Provider>
  );
}

export default App;
