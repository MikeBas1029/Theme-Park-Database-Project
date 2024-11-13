import * as React from "react";
import Box from "@mui/material/Box";
import Avatar from "@mui/material/Avatar";
import EmojiEventsIcon from "@mui/icons-material/EmojiEvents";
import Menu from "@mui/material/Menu";
import MenuItem from "@mui/material/MenuItem";
import ListItemIcon from "@mui/material/ListItemIcon";
import Divider from "@mui/material/Divider";
import IconButton from "@mui/material/IconButton";
import Tooltip from "@mui/material/Tooltip";
import PersonAdd from "@mui/icons-material/PersonAdd";
import Settings from "@mui/icons-material/Settings";
import Logout from "@mui/icons-material/Logout";
import { useUser } from "./context/UserContext";
import { useNavigate } from "react-router-dom";

export default function AccountMenu({ userRole }) {
	const [anchorEl, setAnchorEl] = React.useState(null);
	const open = Boolean(anchorEl);
	const navigate = useNavigate();
	const { user, logout } = useUser(); // Get the user context

	const handleClick = (event) => {
		setAnchorEl(event.currentTarget);
	};

	const handleClose = () => {
		setAnchorEl(null);
	};

	const handleLogout = () => {
		handleClose();
		localStorage.removeItem("user_data");
		localStorage.removeItem("access_token");
		localStorage.removeItem("refresh_token");
		user.userType === "employee" ? navigate("/emplogin") : navigate("/");
		logout();
	};

	const handleProfileClick = () => {
		handleClose();
		navigate("/profile"); // Navigate to the profile page
	};

	const avatarSrc =
		user.userType === "employee"
			? "../../assets/user.png"
			: "../../assets/user2.jpeg"; // Replace with your actual paths

	// Define colors for different membership types
	const membershipColors = {
		Bronze: "#cd7f32",
		Silver: "#c0c0c0",
		Gold: "#ffd700",
		Platinum: "#e5e4e2",
	};

	// Get the color for the membership type, defaulting to "Gold" if undefined
	const trophyColor = membershipColors[user.membership_type] || "#cd7f32";

	return (
		<React.Fragment>
			<Box
				sx={{
					display: "flex",
					alignItems: "center",
					textAlign: "center",
				}}
			>
				<IconButton
					onClick={handleClick}
					size="small"
					sx={{ ml: 2 }}
					aria-controls={open ? "account-menu" : undefined}
					aria-haspopup="true"
					aria-expanded={open ? "true" : undefined}
				>
					<Box position="relative" display="inline-block">
						{/* Profile Picture with Trophy Overlay */}
						<Tooltip title="Profile Settings">
							<Avatar
								src={avatarSrc}
								alt="Profile Picture"
								sx={{ width: 40, height: 40 }}
							/>
						</Tooltip>
						<EmojiEventsIcon
							sx={{
								position: "absolute",
								top: -7,
								right: -9,
								color: trophyColor,
								fontSize: 22,
								borderRadius: "50%",
								padding: "2px",
								zIndex: 99,
							}}
						/>
					</Box>
				</IconButton>
			</Box>

			<Menu
				anchorEl={anchorEl}
				id="account-menu"
				open={open}
				onClose={handleClose}
				onClick={handleClose}
				slotProps={{
					paper: {
						elevation: 0,
						sx: {
							overflow: "visible",
							filter: "drop-shadow(0px 2px 8px rgba(0,0,0,0.32))",
							mt: 1.5,
							"& .MuiAvatar-root": {
								width: 32,
								height: 32,
								ml: -0.5,
								mr: 1,
							},
							"&::before": {
								content: '""',
								display: "block",
								position: "absolute",
								top: 0,
								right: 14,
								width: 10,
								height: 10,
								bgcolor: "background.paper",
								transform: "translateY(-50%) rotate(45deg)",
								zIndex: 0,
							},
						},
					},
				}}
				transformOrigin={{ horizontal: "right", vertical: "top" }}
				anchorOrigin={{ horizontal: "right", vertical: "bottom" }}
			>
				{/* Profile Settings Tab */}
				<MenuItem onClick={handleClose}>
					<Avatar src={avatarSrc} alt="Profile Picture" />
					{user
						? `${user.first_name} ${user.last_name}`
						: `${user.email}`}
				</MenuItem>

				<Divider />

				<MenuItem onClick={handleProfileClick}>
					<ListItemIcon>
						<PersonAdd fontSize="small" />
					</ListItemIcon>
					Profile
				</MenuItem>

				<MenuItem onClick={handleClose}>
					<ListItemIcon>
						<Settings fontSize="small" />
					</ListItemIcon>
					Settings
				</MenuItem>

				<MenuItem onClick={handleLogout}>
					<ListItemIcon>
						<Logout fontSize="small" />
					</ListItemIcon>
					Logout
				</MenuItem>
			</Menu>
		</React.Fragment>
	);
}
