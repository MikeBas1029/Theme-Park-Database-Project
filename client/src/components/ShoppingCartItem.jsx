// ShoppingCartItem.js
import React from "react";
import { Box, Typography, IconButton, Divider } from "@mui/material";
import TicketCounter from "./TicketCounter";
import DeleteIcon from "@mui/icons-material/Delete";

const ShoppingCartItem = ({ item, onRemove, onUpdateQuantity }) => {
	const { ticketType, date, adultCount, childCount, totalPrice } = item;

	return (
		<Box
			sx={{
				display: "flex",
				flexDirection: "column",
				p: 2,
				borderBottom: "1px solid #ddd",
			}}
		>
			<Box
				sx={{
					display: "flex",
					justifyContent: "space-between",
					alignItems: "center",
				}}
			>
				<Typography variant="h6">{ticketType}</Typography>
				<IconButton color="error" onClick={() => onRemove(item)}>
					<DeleteIcon />
				</IconButton>
			</Box>
			<Typography variant="body2" color="textSecondary">
				Date: {new Date(date).toLocaleDateString()}
			</Typography>
			<Typography variant="body2">
				Total Price: ${totalPrice.toFixed(2)}
			</Typography>

			<Box mt={2}>
				<TicketCounter
					label="Adult Tickets"
					price={item.adultPrice}
					count={adultCount}
					setCount={(newCount) =>
						onUpdateQuantity(item, { adultCount: newCount })
					}
				/>
				<TicketCounter
					label="Child Tickets"
					price={item.childPrice}
					count={childCount}
					setCount={(newCount) =>
						onUpdateQuantity(item, { childCount: newCount })
					}
				/>
			</Box>
			<Divider sx={{ mt: 2 }} />
		</Box>
	);
};

export default ShoppingCartItem;
