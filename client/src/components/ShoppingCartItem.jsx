// ShoppingCartItem.js
import React from "react";
import { Box, Typography, IconButton, Divider } from "@mui/material";
import TicketCounter from "./TicketCounter";
import DeleteIcon from "@mui/icons-material/Delete";

const ShoppingCartItem = ({ item, onRemove, onUpdateQuantity }) => {
	const { name, type, date, totalPrice, quantity, price } = item;

	const handleQuantityChange = (newQuantity) => {
		onUpdateQuantity(item.id, newQuantity);
	};

	return (
		<Box
			sx={{
				display: "flex",
				flexDirection: "column",
				p: 2,
				borderBottom: "1px solid #ddd",
			}}
		>
			{/* Header with Ticket Type and Delete Button */}
			<Box
				sx={{
					display: "flex",
					justifyContent: "space-between",
					alignItems: "center",
				}}
			>
				<Typography variant="h6">
					{quantity} x {name}
				</Typography>
				<IconButton color="error" onClick={() => onRemove(item)}>
					<DeleteIcon />
				</IconButton>
			</Box>

			{/* Display Date and Total Price */}
			<Typography variant="body2" color="textSecondary">
				Date:{" "}
				{date ? new Date(date).toLocaleDateString() : "Not selected"}
			</Typography>
			<Typography variant="body2">
				Total Price: ${totalPrice.toFixed(2)}
			</Typography>

			{/* Ticket Counters for Adult and Child Tickets */}
			<Box mt={2}>
				<TicketCounter
					label={`${type} Tickets`}
					price={price}
					count={quantity}
					setCount={handleQuantityChange}
				/>
			</Box>

			<Divider sx={{ mt: 2 }} />
		</Box>
	);
};

export default ShoppingCartItem;
