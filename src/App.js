import {Routes, Route, Link} from "react-router-dom"
import { DisplayModeContext, useMode } from "./theme";
import { CssBaseline, ThemeProvider } from "@mui/material";
import Navbar from "./scenes/global/Navbar";
import Sidebar from "./scenes/global/Sidebar";
//import Rides from "./scenes/Rides";
//import Security from "./scenes/Security";
//import Calendar from "./scenes/Calendar";
import Dashboard from "./scenes/dashboard";
import LoginForm from "./scenes/login/LoginForm"
import Employees from "./scenes/employees";
import Vendors from "./scenes/vendors";
import TransactionSelection from "./scenes/transactions/transactionSelection";
import Invoices from "./scenes/invoices";
import Form from "./scenes/form";





function App() {
  const [theme, colorMode] = useMode();
  return ( 
  <DisplayModeContext.Provider value={colorMode}>
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <div className="app">
        <Sidebar />
       <main className="content">
        <Navbar />
        <Routes>
          <Route path="/" element={<Dashboard />}/> {/* Dashboard routing */}
          <Route path="/employees" element={<Employees />} />   {/*Employee page routing */}
          <Route path="/vendors" element={<Vendors />} />   {/*Vendors page routing */}
          <Route path="/login" element={<LoginForm />} />   {/*Login form routing */}
          <Route path="/transactions" element={<TransactionSelection />} />   {/*Transactions main page routing */}
          <Route path="/invoices" element={<Invoices />} />   {/*Invoice page  routing */}
          <Route path="/form" element={<Form />} />   {/*Employee creation form routing */}
        </Routes>

      </main>
      </div>
    </ThemeProvider>
  </DisplayModeContext.Provider>
  );
}

export default App;
