import {Routes, Route, Link, useLocation} from "react-router-dom"
import { DisplayModeContext, useMode } from "./theme";
import { CssBaseline, ThemeProvider } from "@mui/material";
import Navbar from "./scenes/global/Navbar";
import Sidebar from "./scenes/global/Sidebar";
//import Rides from "./scenes/Rides";
//import Calendar from "./scenes/Calendar";
import Dashboard from "./scenes/dashboard";
import LoginForm from "./scenes/login2/LoginForm"
import Employees from "./scenes/employees";
import Vendors from "./scenes/vendors";
import TransactionSelection from "./scenes/transactions/transactionSelection";
import Invoices from "./scenes/invoices";
import Form from "./scenes/form";
import Maintenance from "./scenes/maintenance";
import Shops from "./scenes/shops";
import Supplies from "./scenes/supplies";
import Customers from "./scenes/customers";
import Facilities from "./scenes/facilities";
import VendorSelection from "./scenes/vendorsandorders/vendorSelection";
import Safety from "./scenes/safety";
import InventoryForm from "./scenes/inventoryform";
import Rides from "./scenes/rides";
import CustomerVisitSelection from "./scenes/customervisits/customervisitselection";
import LoginPage from "./scenes/login/loginPage";
import SignUpPage from "./scenes/login/signupPage";
import CustomerLanding from "./scenes/customerscreens/customerlanding";






function App() {
  

  /*diplay state management */
  const [theme, colorMode] = useMode();

  //keep track of pages for limiting ui
  const location = useLocation();
  const isLoginPage = location.pathname === "/login" ;
  const isSignUpPage = location.pathname === "/signup" ;
  const isSignUpPageSub = location.pathname === "/" ;
  const isCustomerLanding = location.pathname = "/customerlanding"







  return ( 
  <DisplayModeContext.Provider value={colorMode}>
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <div className="app">
      {!isLoginPage && !isSignUpPage && !isSignUpPageSub && <Sidebar />}
      <main className="content">
      {!isLoginPage && !isSignUpPage && !isSignUpPageSub &&<Navbar />}
        <Routes>
          <Route path="/" element={<SignUpPage />}/> {/* Dashboard routing */}
          <Route path="/employees" element={<Employees />} />   {/*Employee page routing */}
          <Route path="/vendors" element={<Vendors />} />   {/*Vendors page routing */}
          <Route path="/login2" element={<LoginForm />} />   {/*Login page routing */}
          <Route path="/transactions" element={<TransactionSelection />} />   {/*Transactions tab routing */}
          <Route path="/invoices" element={<Invoices />} />   {/*Invoice page routing */}
          <Route path="/form" element={<Form />} />   {/*Employee creation form routing */}
          <Route path="/shops" element={<Shops />} />   {/*Shops page pagerouting */}
          <Route path="/maintenance" element={<Maintenance />} />   {/*Maintenance page routing */}
          <Route path="/supplies" element={<Supplies />} />   {/*Shops&Inventory tab routing */}
          <Route path="/customers" element={<Customers />} />   {/*Customers page routing */}
          <Route path="/facilities" element={<Facilities />} />   {/*Facilities page routing */}
          <Route path="/vendorsandorders" element={<VendorSelection />} />   {/*Vendors&Orders tab form routing */}
          <Route path="/safety" element={<Safety />} />   {/*Safety page routing */}
          <Route path="/inventoryForm" element={<InventoryForm />} /> {/*Inventory's form page routing */}
          <Route path="/rides" element={<Rides />} /> {/*Inventory's form page routing */}
          <Route path="/customervisits" element={<CustomerVisitSelection />} /> {/*Inventory's form page routing */}
          <Route path="/login" element={<LoginPage />} /> {/*Inventory's form page routing */}
          <Route path="/signup" element={<SignUpPage />} /> {/*Inventory's form page routing */}
          <Route path="/customerlanding" element={<CustomerLanding />} /> {/*Inventory's form page routing */}



        </Routes>


      </main>
      </div>
    </ThemeProvider>
  </DisplayModeContext.Provider>
  );
}

export default App;
