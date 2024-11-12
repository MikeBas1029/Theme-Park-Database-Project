import * as React from "react";
import Menu from "@mui/material/Menu";
import MenuItem from "@mui/material/MenuItem";
import { Box, Typography } from "@mui/material";
import { useNavigate, useLocation } from "react-router-dom";

export default function DropdownMenu({ title, menuItems, icon }) {
	const [anchorEl, setAnchorEl] = React.useState(null);
	const open = Boolean(anchorEl);
	const navigate = useNavigate();
	const location = useLocation();

	const handleClick = (event) => {
		setAnchorEl(event.currentTarget);
	};

	const handleClose = () => {
		setAnchorEl(null);
	};

	const handleMenuItemClick = (path) => {
		navigate(path);
		handleClose(); // Close the menu after navigation
	};

	// Determine if the dropdown title is active (any dropdown item matches current path)
	const isTitleActive = menuItems.some(
		(item) => location.pathname === item.path
	);

	return (
		<div>
			<Box
				onClick={handleClick}
				sx={{
					display: "flex",
					alignItems: "center",
					padding: "10px 20px",
					cursor: "pointer",
				}}
			>
				{icon && (
					<Box
						sx={{
							marginRight: "8px",
							color: isTitleActive ? "#FFD700" : "inherit",
						}}
					>
						{icon}
					</Box>
				)}
				<Typography sx={{ fontSize: "1rem" }}>{title}</Typography>
			</Box>
			<Menu
				id="basic-menu"
				anchorEl={anchorEl}
				open={open}
				onClose={handleClose}
				MenuListProps={{
					"aria-labelledby": "basic-button",
				}}
			>
				{menuItems.map((item) => {
					const isActive = location.pathname === item.path;
					return (
						<MenuItem
							key={item.label}
							onClick={() => handleMenuItemClick(item.path)}
							sx={{
								backgroundColor: isActive
									? "rgba(255, 255, 255, 0.1)"
									: "transparent",
							}}
						>
							{item.icon && (
								<Box
									sx={{
										marginRight: "8px",
										color: isActive ? "#FFD700" : "inherit",
									}}
								>
									{item.icon}
								</Box>
							)}
							{item.label}
						</MenuItem>
					);
				})}
			</Menu>
		</div>
	);
}