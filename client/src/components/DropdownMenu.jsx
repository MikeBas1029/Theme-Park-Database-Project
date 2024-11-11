import * as React from "react";
import Menu from "@mui/material/Menu";
import MenuItem from "@mui/material/MenuItem";
import { Box, Typography, useTheme } from "@mui/material";
import { useNavigate, useLocation } from "react-router-dom";

export default function DropdownMenu({ title, menuItems, icon }) {
	const [anchorEl, setAnchorEl] = React.useState(null);
	const open = Boolean(anchorEl);
	const navigate = useNavigate();
	const location = useLocation();
	const theme = useTheme();

	const handleClick = (event) => {
		setAnchorEl(event.currentTarget);
	};

	const handleClose = () => {
		setAnchorEl(null);
	};

	const handleMenuItemClick = (path) => {
		navigate(path);
		handleClose();
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
					color: theme.palette.navbarText.main,
				}}
			>
				{icon && (
					<Box
						sx={{
							marginRight: "8px",
							color: isTitleActive
								? theme.palette.secondary.main
								: theme.palette.navbarText.main,
						}}
					>
						{icon}
					</Box>
				)}
				<Typography
					sx={{
						fontSize: "1rem",
						color: theme.palette.navbarText.main,
					}}
				>
					{title}
				</Typography>
			</Box>
			<Menu
				id="basic-menu"
				anchorEl={anchorEl}
				open={open}
				onClose={handleClose}
				MenuListProps={{
					"aria-labelledby": "basic-button",
				}}
				sx={{
					"& .MuiPaper-root": {
						backgroundColor: theme.palette.background.default,
						color: theme.palette.text.primary,
					},
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
									? "rgba(0, 102, 153, 0.1)"
									: "transparent",
								color: theme.palette.text.primary,
								"&:hover": {
									backgroundColor:
										theme.palette.action.selected,
								},
							}}
						>
							{item.icon && (
								<Box
									sx={{
										marginRight: "8px",
										color: isActive
											? theme.palette.secondary.main
											: theme.palette.navbarText.main,
									}}
								>
									{item.icon}
								</Box>
							)}
							<Typography variant="body2">
								{item.label}
							</Typography>
						</MenuItem>
					);
				})}
			</Menu>
		</div>
	);
}
