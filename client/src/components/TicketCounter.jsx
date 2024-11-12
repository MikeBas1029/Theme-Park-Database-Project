// TicketCounter.js
import React from "react";
import { Box, Typography, IconButton } from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
import RemoveIcon from "@mui/icons-material/Remove";

const TicketCounter = ({ label, price, count, setCount }) => (
	<Box
		display="flex"
		alignItems="center"
		justifyContent="space-between"
		my={2}
	>
		<Box>
			<Typography>{label}</Typography>
			<Typography variant="subtitle2" color="text.secondary">
				Starting From ${price} Per Day
			</Typography>
		</Box>
		<Box display="flex" alignItems="center">
			<IconButton onClick={() => setCount(Math.max(0, count - 1))}>
				<RemoveIcon />
			</IconButton>
			<Typography>{count}</Typography>
			<IconButton onClick={() => setCount(count + 1)}>
				<AddIcon />
			</IconButton>
		</Box>
	</Box>
);

export default TicketCounter;
