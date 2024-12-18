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
import EmployeePayroll from "./scenes/employees/payroll";
import ManageStaff from "./scenes/managestaff/managestaffselection";
import MaintenanceReports from "./scenes/insights/workorderreports";
import Insights from "./scenes/insights";
import Charts from "./scenes/charts";
import Finances from "./scenes/finances";
import ManagerDashboard from "./scenes/dashboard/managerdashboard";
import CustomerRides from "./scenes/customerrides";
import CustomerEvents from "./scenes/customerevents";

function App() {
	const navigate = useNavigate();

	/*user state management */
	const { user } = useUser();

	/*diplay state management */
	const [theme, colorMode] = useMode();

	//keep track of pages for limiting ui
	const location = useLocation();
	const isCustLogin = location.pathname === "/custlogin";
	const isEmpLogin = location.pathname === "/emplogin";
	const isSignUpPage = location.pathname === "/signup";
	const isSignUpPageSub = location.pathname === "/sub";

	return (
		<DisplayModeContext.Provider value={colorMode}>
			<ThemeProvider theme={theme}>
				<CssBaseline />
				<div className="app">
					{!isCustLogin &&
						!isSignUpPage &&
						!isEmpLogin &&
						user?.userType === "employee" && <Sidebar />}
					<main className="content">
						{!isCustLogin && !isSignUpPage && !isEmpLogin && (
							<Navbar />
						)}
						<Routes>
							{/*User Authentication pages */}
							<Route
								path="/"
								element={<CustomerDashboard />}
							/>{" "}
							<Route path="/emplogin" element={<LoginForm />} />{" "}
							{/*Login page routing */}
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
							{/*Access controlled routes */}
							{/* Dashboard routing */}
							<Route
								path="/dashboard"
								element={
									<ProtectedRoute allowedRoles={["admin"]}>
										<Dashboard />
									</ProtectedRoute>
								}
							/>{" "}
							{/* Dashboard routing */}
							<Route
								path="/managerdashboard"
								element={
									<ProtectedRoute allowedRoles={["manager"]}>
										<ManagerDashboard />
									</ProtectedRoute>
								}
							/>{" "}
							{/* Dashboard routing */}
							<Route
								path="/employees"
								element={
									<ProtectedRoute
										allowedRoles={["admin", "manager"]}
									>
										<Employees />
									</ProtectedRoute>
								}
							/>{" "}
							{/*Employee page routing */}
							<Route
								path="/payroll"
								element={
									<ProtectedRoute
										allowedRoles={["admin", "manager"]}
									>
										<EmployeePayroll />
									</ProtectedRoute>
								}
							/>{" "}
							{/*Employee page routing */}
							<Route path="/rides" element={<Rides />} />{" "}
							<Route
								path="/customer-rides"
								element={<CustomerRides />}
							/>{" "}
							<Route
								path="/customer-events"
								element={<CustomerEvents />}
							/>{" "}
							{/*Inventory's form page routing */}
							<Route
								path="/vendors"
								element={
									<ProtectedRoute>
										<Vendors />
									</ProtectedRoute>
								}
							/>{" "}
							{/*Vendors page routing */}
							<Route
								path="/customers"
								element={
									<ProtectedRoute allowedRoles={["admin"]}>
										<Customers />
									</ProtectedRoute>
								}
							/>{" "}
							{/*Customers page routing */}
							<Route
								path="/invoices"
								element={
									<ProtectedRoute allowedRoles={["admin"]}>
										<Invoices />
									</ProtectedRoute>
								}
							/>{" "}
							{/*Invoice page routing */}
							<Route path="/shops" element={<Shops />} />{" "}
							{/*Shops page pagerouting */}
							<Route
								path="/maintenance"
								element={
									<ProtectedRoute>
										<Maintenance />
									</ProtectedRoute>
								}
							/>{" "}
							{/*Maintenance page routing */}
							<Route path="/safety" element={<Safety />} />{" "}
							{/*Safety page routing */}
							<Route
								path="/tickets"
								element={
									<ProtectedRoute>
										<Tickets />
									</ProtectedRoute>
								}
							/>{" "}
							{/*Inventory's form page routing */}
							<Route
								path="/facilities"
								element={
									<ProtectedRoute>
										<Facilities />
									</ProtectedRoute>
								}
							/>{" "}
							{/*Facilities page routing */}
							<Route
								path="/managestaff"
								element={
									<ProtectedRoute allowedRoles={["admin"]}>
										<ManageStaff />
									</ProtectedRoute>
								}
							/>{" "}
							{/*Staff management page routing */}✅
							<Route
								path="/transactions"
								element={
									<ProtectedRoute allowedRoles={["admin"]}>
										<TransactionSelection />
									</ProtectedRoute>
								}
							/>{" "}
							{/*Transactions tab routing */} ✅
							<Route
								path="/insights"
								element={
									<ProtectedRoute allowedRoles={["admin"]}>
										<Insights />
									</ProtectedRoute>
								}
							/>{" "}
							{/*Transactions tab routing */} ✅
							{/*Report pages */}
							<Route
								path="/workorderreports"
								element={
									<ProtectedRoute allowedRoles={["admin"]}>
										<MaintenanceReports />
									</ProtectedRoute>
								}
							/>{" "}
							{/*Transactions tab routing */} ✅
							<Route
								path="/charts"
								element={
									<ProtectedRoute allowedRoles={["admin"]}>
										<Charts />
									</ProtectedRoute>
								}
							/>{" "}
							{/*Transactions tab routing */} ✅
							<Route
								path="/finances"
								element={
									<ProtectedRoute allowedRoles={["admin"]}>
										<Finances />
									</ProtectedRoute>
								}
							/>{" "}
							{/*Transactions tab routing */} ✅
							{/*Creation forms*/}
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
							<Route
								path="/inventoryForm"
								element={<InventoryForm />}
							/>{" "}
							{/*Inventory's form page routing */}
							{/*Customer side routes*/}
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
							<Route path="/parkmap" element={<MapPage />} />{" "}
							{/*Inventory's form page routing */}
							{/*Sidebar page routes*/}
							<Route
								path="/vendorsorders"
								element={
									<ProtectedRoute>
										<VendorSelection />{" "}
									</ProtectedRoute>
								}
							/>{" "}
							{/*Vendors & Orders tab form routing */}
							<Route
								path="/customervisits"
								element={
									<ProtectedRoute>
										<CustomerVisitSelection />
									</ProtectedRoute>
								}
							/>{" "}
							{/*Inventory's form page routing */}
							<Route
								path="/supplies"
								element={
									<ProtectedRoute>
										<Supplies />
									</ProtectedRoute>
								}
							/>{" "}
							{/*Shops&Inventory tab routing */}
						</Routes>
					</main>
				</div>
			</ThemeProvider>
		</DisplayModeContext.Provider>
	);
}

export default App;
