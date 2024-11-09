import {
	Box,
	IconButton,
	useTheme,
	Typography,
	useMediaQuery,
} from "@mui/material";
import { useContext } from "react";
import { DisplayModeContext } from "../../theme";
import { useLocation, Link, useNavigate } from "react-router-dom";
import LightModeOutlinedIcon from "@mui/icons-material/LightModeOutlined";
import DarkModeOutlinedIcon from "@mui/icons-material/DarkModeOutlined";
import CalendarTodayOutlinedIcon from "@mui/icons-material/CalendarTodayOutlined";
import HomeOutlinedIcon from "@mui/icons-material/HomeOutlined";
import LocalActivityIcon from "@mui/icons-material/LocalActivity";
import MapOutlinedIcon from "@mui/icons-material/MapOutlined";
import AttractionsOutlinedIcon from "@mui/icons-material/AttractionsOutlined";
import StoreOutlinedIcon from "@mui/icons-material/StoreOutlined";
import NotificationMenu from "./NotificationMenu";
import AccountMenu from "../../components/AccountMenu";
import DropdownMenu from "../../components/DropdownMenu";

const Item = ({ title, to, icon }) => {
	const location = useLocation();
	const isActive = location.pathname === to;

	return (
		<Link to={to} style={{ textDecoration: "none", color: "inherit" }}>
			<Box
				sx={{
					display: "flex",
					alignItems: "center",
					padding: "10px 20px",
					backgroundColor: isActive
						? "rgba(255, 255, 255, 0.1)"
						: "transparent",
					borderRadius: "8px",
				}}
			>
				<Box
					sx={{
						color: isActive ? "#FFD700" : "inherit",
						marginRight: "8px",
					}}
				>
					{icon}
				</Box>
				<Typography
					sx={{
						marginLeft: "8px",
						fontSize: "1.1rem",
						// color: isActive ? "#3A5BC7" : "inherit",
					}}
				>
					{title}
				</Typography>
			</Box>
		</Link>
	);
};

const Navbar = ({ userType }) => {
	const theme = useTheme();
	const colorMode = useContext(DisplayModeContext);
	const isSmallScreen = useMediaQuery(theme.breakpoints.down("md"));
	const navigate = useNavigate();

	return (
		<Box
			display="flex"
			alignItems="center"
			p={1}
			position="sticky" // Make navbar sticky
			top={0} // Stick to the top of the viewport
			zIndex={10} // Ensure it stays above other content when scrolling
			backgroundColor="black" // Set background color to avoid transparency issues
			boxShadow="0px 2px 5px rgba(0, 0, 0, 0.1)" // Add a shadow for better visibility
		>
			{/* Left Spacer */}
			<Box
				flex="1"
				display="flex"
				alignItems="center"
				justifyContent="center"
			>
				<img
					src="assets/logo.png"
					alt="Logo"
					style={{ maxHeight: "50px", cursor: "pointer" }}
					onClick={() => navigate("/")}
				/>
			</Box>

			{/* Centered Navbar Content */}
			<Box
				display="flex"
				justifyContent="center"
				alignItems="center"
				flex="2"
				mx="auto"
			>
				{userType === "customer" && (
					<Box
						display="flex"
						justifyContent="center"
						alignItems="center"
						flexWrap={isSmallScreen ? "wrap" : "nowrap"}
						gap={1}
						maxWidth="800px"
					>
						<Item
							title="Home"
							to="/customerhome"
							icon={<HomeOutlinedIcon />}
						/>
						<DropdownMenu
							title="Tickets"
							menuItems={[
								{
									label: "My Tickets",
									path: "/customertickets",
								},
								{
									label: "Purchase Tickets",
									path: "/purchaseTickets",
								},
							]}
							icon={<LocalActivityIcon />}
						/>
						<Item
							title="Map"
							to="/parkmap"
							icon={<MapOutlinedIcon />}
						/>
						<DropdownMenu
							title="Amusement"
							menuItems={[
								{ label: "Rides", path: "/customer-rides" },
								// {
								// 	label: "Attractions",
								// 	path: "/customerattractions",
								// },
								{ label: "Events", path: "/customer-events" },
							]}
							icon={<AttractionsOutlinedIcon />}
						/>
						<DropdownMenu
							title="Services"
							menuItems={[
								{ label: "Dining", path: "/customerdining" },
								{
									label: "Facilities",
									path: "/customerfacilities",
								},
								{ label: "Shopping", path: "/customershops" },
							]}
							icon={<StoreOutlinedIcon />}
						/>
					</Box>
				)}
			</Box>

			{/* Right-aligned Icon Section */}
			<Box
				display="flex"
				alignItems="center"
				flex="1"
				justifyContent="flex-end"
			>
				<IconButton onClick={colorMode.toggleDisplayMode}>
					{theme.palette.mode === "dark" ? (
						<DarkModeOutlinedIcon />
					) : (
						<LightModeOutlinedIcon />
					)}
				</IconButton>
				{userType !== "customer" && (
					<IconButton>
						<CalendarTodayOutlinedIcon />
					</IconButton>
				)}
				<IconButton>
					<NotificationMenu />
				</IconButton>
				<AccountMenu userType={userType} />
			</Box>
		</Box>
	);
};

export default Navbar;
