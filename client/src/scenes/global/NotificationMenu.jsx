import React, { useEffect, useState, useContext } from "react";
import {
	Box,
	IconButton,
	Typography,
	Divider,
	Badge,
	useTheme,
} from "@mui/material";
import NotificationsOutlinedIcon from "@mui/icons-material/NotificationsOutlined";
import CloseIcon from "@mui/icons-material/Close";
import { DisplayModeContext } from "../../theme";
import { useUser } from "../../components/context/UserContext";

const NotificationMenu = ({ buttonStyle, dropdownStyle }) => {
	const [notifications, setNotifications] = useState([]);
	const [isOpen, setIsOpen] = useState(false);
	const theme = useTheme();
	const { user } = useUser();
	const { userType, customer_id, employee_id } = user || {};

	useEffect(() => {
		const userId = userType === "customer" ? customer_id : employee_id;
		if (!userType || !userId) return;

		const fetchNotifications = async () => {
			const endpoint =
				userType === "customer"
					? `https://theme-park-backend.ambitioussea-02dd25ab.eastus.azurecontainerapps.io/api/v1/cust-notifs/cust/${userId}`
					: `https://theme-park-backend.ambitioussea-02dd25ab.eastus.azurecontainerapps.io/api/v1/emp-notifs/${userId}`;

			try {
				const response = await fetch(endpoint, {
					method: "GET",
					headers: { "Content-Type": "application/json" },
				});

				if (!response.ok) {
					setNotifications([]);
					return;
				}

				const data = await response.json();
				setNotifications(data);
			} catch (error) {
				console.error("Error fetching notifications:", error);
			}
		};

		fetchNotifications();
	}, [userType, customer_id, employee_id]);

	const toggleMenu = () => {
		setIsOpen(!isOpen);
	};

	const clearNotification = (id) => {
		setNotifications((prev) => prev.filter((notif) => notif.id !== id));
	};

	const unseenCount = notifications.filter((notif) => !notif.seen).length;
	const textColor = theme.palette.text.primary;

	return (
		<Box position="relative">
			<IconButton
				onClick={toggleMenu}
				sx={{
					...buttonStyle,
					"&:hover": {
						backgroundColor: "transparent",
						opacity: 1,
					},
				}}
			>
				<Badge badgeContent={unseenCount} color="error">
					<NotificationsOutlinedIcon />
				</Badge>
			</IconButton>
			{isOpen && (
				<Box
					sx={{
						position: "absolute",
						zIndex: 1000,
						bgcolor: theme.palette.background.paper,
						border: "1px solid #ccc",
						borderRadius: "8px",
						width: "280px",
						right: "10px",
						marginTop: "10px",
						boxShadow: "0px 4px 12px rgba(0, 0, 0, 0.1)",
						color: textColor,
						overflow: "hidden",
					}}
				>
					<Box
						sx={{
							maxHeight: "300px",
							overflowY: "auto",
							bgcolor: theme.palette.background.paper,
							padding: "8px 0",
						}}
					>
						{notifications.length === 0 ? (
							<Box
								sx={{
									padding: "12px",
									color: textColor,
									textAlign: "center",
									fontSize: "0.875rem",
								}}
							>
								No notifications for{" "}
								{userType === "customer"
									? "customer"
									: "employee"}
								.
							</Box>
						) : (
							notifications.map((notification, index) => (
								<Box
									key={notification.id}
									sx={{
										position: "relative",
										padding: "8px 12px",
										bgcolor: theme.palette.background.paper,
										borderRadius: "4px",
										margin: "6px 12px",
										boxShadow:
											"0px 2px 4px rgba(0, 0, 0, 0.1)",
										overflowWrap: "break-word",
									}}
								>
									<IconButton
										size="small"
										onClick={() =>
											clearNotification(notification.id)
										}
										sx={{
											position: "absolute",
											top: "4px",
											right: "4px",
											color: theme.palette.text.secondary,
											padding: 0,
										}}
									>
										<CloseIcon fontSize="small" />
									</IconButton>
									<Typography
										variant="body2"
										sx={{
											color: textColor,
											marginRight: "20px",
											fontSize: "0.875rem",
										}}
									>
										{notification.message}
									</Typography>
									{index < notifications.length - 1 && (
										<Divider sx={{ my: 0.5 }} />
									)}
								</Box>
							))
						)}
					</Box>
				</Box>
			)}
		</Box>
	);
};

export default NotificationMenu;
