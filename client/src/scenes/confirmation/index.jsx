// ConfirmationPage.js
import React, { useEffect, useState } from "react";
import { Box, Typography, Divider, Paper, Button } from "@mui/material";
import { useNavigate } from "react-router-dom";

const ConfirmationPage = () => {
	const navigate = useNavigate();
	const [purchasedItems, setPurchasedItems] = useState([]);
	const [total, setTotal] = useState(0);

	useEffect(() => {
		// Retrieve purchased items from local storage
		const storedItems = JSON.parse(localStorage.getItem("purchasedItems"));
		if (storedItems) {
			setPurchasedItems(storedItems);

			// Calculate the total from stored items
			const calculatedTotal = storedItems.reduce(
				(acc, item) => acc + item.price * item.quantity,
				0
			);
			setTotal(calculatedTotal);
		}
		// Clear local storage after retrieving for security and to avoid stale data
		localStorage.removeItem("purchasedItems");
	}, []);

	return (
		<Box p={3} maxWidth="md" mx="auto">
			<Typography variant="h4" gutterBottom align="center">
				Order Confirmation
			</Typography>
			<Typography
				variant="body1"
				color="textSecondary"
				align="center"
				mb={2}
			>
				Thank you for your purchase! Here are the details of your order.
			</Typography>
			<Divider />

			{purchasedItems.length > 0 ? (
				<Box
					mt={3}
					component={Paper}
					elevation={3}
					p={3}
					borderRadius="8px"
				>
					{purchasedItems.map((item, index) => (
						<Box key={index} mb={2}>
							<Typography variant="h6">{item.name}</Typography>
							<Typography variant="body2" color="textSecondary">
								Type: {item.type} - Quantity: {item.quantity} -
								Price: ${item.price.toFixed(2)}
							</Typography>
							<Typography variant="body2" color="textSecondary">
								Date:{" "}
								{item.date
									? new Date(item.date).toLocaleDateString()
									: "Not selected"}
							</Typography>
							<Typography variant="body2" color="textSecondary">
								Subtotal: $
								{(item.price * item.quantity).toFixed(2)}
							</Typography>
							{index < purchasedItems.length - 1 && (
								<Divider sx={{ my: 2 }} />
							)}
						</Box>
					))}
					<Divider sx={{ my: 2 }} />
					<Box display="flex" justifyContent="space-between">
						<Typography variant="h6">Total:</Typography>
						<Typography variant="h6">
							${total.toFixed(2)}
						</Typography>
					</Box>
				</Box>
			) : (
				<Typography
					variant="body1"
					color="textSecondary"
					align="center"
					mt={4}
				>
					No items in the order.
				</Typography>
			)}

			<Box textAlign="center" mt={4}>
				<Button
					variant="contained"
					color="primary"
					onClick={() => navigate("/")}
				>
					Return to Home
				</Button>
			</Box>
		</Box>
	);
};

export default ConfirmationPage;
