import {
	Routes,
	Route,
	Link,
	useLocation,
	useNavigate,
} from "react-router-dom";
import { DisplayModeContext, useMode } from "./theme";
import { CssBaseline, ThemeProvider, Box, Button } from "@mui/material";
import React, { createContext, useContext, useState } from "react";
import Navbar from "./scenes/global/Navbar";
import Sidebar from "./scenes/global/Sidebar";
//import Calendar from "./scenes/Calendar";
import Dashboard from "./scenes/dashboard";
import LoginForm from "./scenes/login2/LoginForm";
import Employees from "./scenes/employees";
import Vendors from "./scenes/vendors";
import TransactionSelection from "./scenes/transactions/transactionSelection";
import Invoices from "./scenes/invoices";
import EmployeeForm from "./scenes/form/employeesform";
import Maintenance from "./scenes/maintenance";
import Shops from "./scenes/shops";
import Supplies from "./scenes/supplies";
import Customers from "./scenes/customers";
import Facilities from "./scenes/facilities";
import VendorSelection from "./scenes/vendorsandorders/vendorSelection";
import Safety from "./scenes/safety";
import InventoryForm from "./scenes/inventoryform/inventoryform";
import Rides from "./scenes/rides";
import CustomerVisitSelection from "./scenes/customervisits/customervisitselection";
import LoginPage from "./scenes/login/loginPage";
import SignUpPage from "./scenes/login/signupPage";
import SidebarCust from "./scenes/global/Sidebar2";
import CustomerSidebar from "./scenes/customerscreens/customerglobal/CustomerSidebar";
import CustomerDashboard from "./scenes/customerscreens/customerdashboard";
import CustomerTickets from "./scenes/customerscreens/customertickets/customerTickets";
import CustomerAppBar from "./scenes/customerscreens/customerglobal/CustomerAppBar";
import Tickets from "./scenes/tickets/Tickets";
import VisitForm from "./scenes/form/visitsform";
import RideForm from "./scenes/form/rideform";
import OrderForm from "./scenes/form/orderform";
import SafetyForm from "./scenes/form/safetyform";
import MaintenanceForm from "./scenes/form/maintenanceform";
import FacilitiesForm from "./scenes/form/facilitiesform";
import ProtectedRoute from "./components/ProtectedRoute";
import NewCustForm from "./scenes/form/newcustomerform";
import { useUser } from "./components/context/UserContext";
import MapPage from "./scenes/map";

function App() {
	const navigate = useNavigate();

<<<<<<< HEAD
	/*user state management */
	//const [userRole, setUserRole] = useState("employee");
	const [userType, setUserType] = useState("employee");
	const { user } = useUser();
=======
  /*user state management */
  const { user } = useUser();
>>>>>>> 9f1d04b507cd9355bc0430b87f86b9a87e2eba88

	/*diplay state management */
	const [theme, colorMode] = useMode();

	//keep track of pages for limiting ui
	const location = useLocation();
	const isCustLogin = location.pathname === "/custlogin";
	const isEmpLogin = location.pathname === "/emplogin";
	const isSignUpPage = location.pathname === "/signup";
	const isSignUpPageSub = location.pathname === "/sub";

	// Simulated login functions
	const loginAsEmployee = () => {
		const hardcodedPassword = "tooShortToRide";
		const userInput = prompt("Please enter the permission password:");

		if (userInput === hardcodedPassword) {
			setUserType("employee");
			navigate("/");
		} else {
			alert("Incorrect password. Access denied.");
		}
	};

<<<<<<< HEAD
	const loginAsCustomer = () => {
		setUserType("customer");
		navigate("/customerhome");
	};

	const logout = () => {
		setUserType(null);
		navigate("/emplogin");
	};

	return (
		<DisplayModeContext.Provider value={colorMode}>
			<ThemeProvider theme={theme}>
				<CssBaseline />
				<div className="app">
					{!isCustLogin &&
						!isSignUpPage &&
						!isEmpLogin &&
						user &&
						userType === "employee" && <Sidebar />}
					<main className="content">
						{!isCustLogin && !isSignUpPage && !isEmpLogin && (
							<Navbar userType={userType} />
						)}
						{/* Simulated login buttons */}
						<Box
							m="20px"
							display="flex"
							justifyContent="flex-start"
						>
							<Box
								display="flex"
								flexDirection="row"
								justifyContent="flex-start"
								alignItems="center"
							>
								{user && userType === "employee" ? (
									<Button
										variant="contained"
										onClick={loginAsCustomer}
										sx={{ mx: 1 }}
									>
										Customer View
									</Button>
								) : user && userType === "customer" ? (
									<Button
										variant="contained"
										onClick={loginAsEmployee}
										sx={{ mx: 1 }}
									>
										Employee View
									</Button>
								) : null}
							</Box>
						</Box>

						<Routes>
							<Route path="/" element={<CustomerDashboard />} />{" "}
							<Route
								path="/dashboard"
								element={
									<ProtectedRoute>
										<Dashboard />
									</ProtectedRoute>
								}
							/>{" "}
							{/* Dashboard routing */}
							<Route
								path="/employees"
								element={
									<ProtectedRoute>
										<Employees />
									</ProtectedRoute>
								}
							/>{" "}
							{/*Employee page routing */}
							<Route path="/vendors" element={<Vendors />} />{" "}
							{/*Vendors page routing */}
							<Route
								path="/emplogin"
								element={<LoginForm />}
							/>{" "}
							{/*Login page routing */}
							<Route
								path="/transactions"
								element={<TransactionSelection />}
							/>{" "}
							{/*Transactions tab routing */}
							<Route
								path="/invoices"
								element={<Invoices />}
							/>{" "}
							{/*Invoice page routing */}
							<Route
								path="/employeeform"
								element={<EmployeeForm />}
							/>{" "}
							{/*Employee creation form routing */}
							<Route
								path="/visitform"
								element={<VisitForm />}
							/>{" "}
							{/*Login page routing */}
							<Route
								path="/orderform"
								element={<OrderForm />}
							/>{" "}
							{/*Employee creation form routing */}
							<Route
								path="/safetyform"
								element={<SafetyForm />}
							/>{" "}
							{/*Login page routing */}
							<Route
								path="/maintenanceform"
								element={<MaintenanceForm />}
							/>{" "}
							{/*Employee creation form routing */}
							<Route
								path="/facilitiesform"
								element={<FacilitiesForm />}
							/>{" "}
							{/*Login page routing */}
							<Route
								path="/ridesform"
								element={<RideForm />}
							/>{" "}
							{/*Wrong route for error dimmissal ! change to no s */}
							<Route path="/shops" element={<Shops />} />{" "}
							{/*Shops page pagerouting */}
							<Route
								path="/maintenance"
								element={<Maintenance />}
							/>{" "}
							{/*Maintenance page routing */}
							<Route
								path="/supplies"
								element={<Supplies />}
							/>{" "}
							{/*Shops&Inventory tab routing */}
							<Route
								path="/customers"
								element={<Customers />}
							/>{" "}
							{/*Customers page routing */}
							<Route
								path="/facilities"
								element={<Facilities />}
							/>{" "}
							{/*Facilities page routing */}
							<Route
								path="/vendorsorders"
								element={<VendorSelection />}
							/>{" "}
							{/*Vendors&Orders tab form routing */}
							<Route path="/safety" element={<Safety />} />{" "}
							{/*Safety page routing */}
							<Route
								path="/inventoryForm"
								element={<InventoryForm />}
							/>{" "}
							{/*Inventory's form page routing */}
							<Route path="/rides" element={<Rides />} />{" "}
							{/*Inventory's form page routing */}
							<Route
								path="/customervisits"
								element={<CustomerVisitSelection />}
							/>{" "}
							{/*Inventory's form page routing */}
							<Route
								path="/custlogin"
								element={<LoginPage />}
							/>{" "}
							{/*Inventory's form page routing */}
							<Route
								path="/signup"
								element={<SignUpPage />}
							/>{" "}
							{/*Inventory's form page routing */}
							{/* <Route
								path="/customerhome"
								element={<CustomerDashboard />}
							/>{" "} */}
							{/*Inventory's form page routing */}
							<Route
								path="/customertickets"
								element={<CustomerTickets />}
							/>{" "}
							{/*Inventory's form page routing */}
							<Route path="/tickets" element={<Tickets />} />{" "}
							{/*Inventory's form page routing */}
							<Route path="/parkmap" element={<MapPage />} />{" "}
							{/*Inventory's form page routing */}
						</Routes>
					</main>
				</div>
			</ThemeProvider>
		</DisplayModeContext.Provider>
	);
=======




  return ( 
  <DisplayModeContext.Provider value={colorMode}>
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <div className="app">
        {!isCustLogin && !isSignUpPage && !isEmpLogin && user?.userType === 'employee' && <Sidebar />}
        <main className="content">
        {!isCustLogin && !isSignUpPage && !isEmpLogin && user && <Navbar userType={user.userType} />}
          <Routes>
             {/*Login page routes */}
            <Route path="/emplogin" element={<LoginForm />} />   {/*Login page routing */}
            <Route path="/custlogin" element={<LoginPage />} /> {/*Inventory's form page routing */}
            <Route path="/signup" element={<SignUpPage />} /> {/*Inventory's form page routing */}
            
             {/*Access controlled routes */}
            <Route path="/" element={<ProtectedRoute><Dashboard /></ProtectedRoute>}/> {/* Dashboard routing */}
            <Route path="/employees" element={<ProtectedRoute><Employees userRole={user?.role} /></ProtectedRoute>}/>   {/*Employee page routing */}
            <Route path="/rides" element={<ProtectedRoute> <Rides  /> </ProtectedRoute>} /> {/*Inventory's form page routing */}
            <Route path="/vendors" element={<ProtectedRoute><Vendors  /></ProtectedRoute>} />   {/*Vendors page routing */}
            <Route path="/customers" element={<ProtectedRoute><Customers  /></ProtectedRoute>} />   {/*Customers page routing */}
            <Route path="/invoices" element={<ProtectedRoute><Invoices  /></ProtectedRoute>} />   {/*Invoice page routing */}
            <Route path="/shops" element={<ProtectedRoute><Shops  /></ProtectedRoute>} />   {/*Shops page pagerouting */}
            <Route path="/maintenance" element={<ProtectedRoute><Maintenance  /></ProtectedRoute>} />   {/*Maintenance page routing */}
            <Route path="/safety" element={<ProtectedRoute><Safety  /></ProtectedRoute>} />   {/*Safety page routing */}
            <Route path="/tickets" element={<ProtectedRoute><Tickets  /></ProtectedRoute>} /> {/*Inventory's form page routing */}
            <Route path="/facilities" element={<ProtectedRoute><Facilities  /></ProtectedRoute>} />   {/*Facilities page routing */}
            
             {/*Creation form routes*/}
            <Route path="/employeeform" element={<EmployeeForm />} />   {/*Employee creation form routing */}
            <Route path="/visitform" element={<VisitForm />} />   {/*Login page routing */}
            <Route path="/orderform" element={<OrderForm />} />   {/*Employee creation form routing */}
            <Route path="/safetyform" element={<SafetyForm />} />   {/*Login page routing */}
            <Route path="/maintenanceform" element={<MaintenanceForm />} />   {/*Employee creation form routing */}
            <Route path="/facilitiesform" element={<FacilitiesForm />} />   {/*Login page routing */}
            <Route path="/ridesform" element={<RideForm />} />   {/*Wrong route for error dimmissal ! change to no s */}
            <Route path="/inventoryForm" element={<InventoryForm />} /> {/*Inventory's form page routing */}
             
             {/*Customer side routes*/}
            <Route path="/customerhome" element={<CustomerDashboard />} /> {/*Inventory's form page routing */}
            <Route path="/customertickets" element={<CustomerTickets  />} /> {/*Inventory's form page routing */}
            <Route path="/parkmap" element={<MapPage />} /> {/*Inventory's form page routing */}
            
             {/*Sidebar page routes*/}
            <Route path="/vendorsorders" element={<VendorSelection />} />   {/*Vendors&Orders tab form routing */}
            <Route path="/customervisits" element={<CustomerVisitSelection />} /> {/*Inventory's form page routing */}
            <Route path="/supplies" element={<Supplies />} />   {/*Shops&Inventory tab routing */}
            <Route path="/transactions" element={<TransactionSelection />} />   {/*Transactions tab routing */}
          </Routes>
      </main>
      </div>
    </ThemeProvider>
  </DisplayModeContext.Provider>
  );
>>>>>>> 9f1d04b507cd9355bc0430b87f86b9a87e2eba88
}

export default App;
