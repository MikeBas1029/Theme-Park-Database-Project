import React from "react";
import {
	Card,
	CardContent,
	CardActions,
	Button,
	Typography,
} from "@mui/material";
import { styled } from "@mui/material/styles";

const StyledCard = styled(Card)({
	width: 200,
	height: 250,
	margin: "20px",
	borderRadius: "15px",
	boxShadow: "0 4px 8px rgba(0,0,0,0.2)",
	display: "flex",
	flexDirection: "column",
	justifyContent: "space-between",
});

const TicketCard = ({ ticket }) => {
	return (
		<StyledCard>
			<CardContent>
				<Typography variant="h5" component="div" fontWeight="bold">
					{ticket.ticket_type}
				</Typography>
				<Typography
					variant="body2"
					color="text.secondary"
					sx={{ mt: 1 }}
				>
					{ticket.description}
				</Typography>
				<Typography variant="h6" component="div" sx={{ mt: 2 }}>
					From ${ticket.base_price}
				</Typography>
				<Typography variant="caption" color="text.secondary">
					Prices per ticket vary by day. + Tax
				</Typography>
			</CardContent>
			<CardActions style={{ justifyContent: "center" }}>
				<Button size="small" variant="outlined">
					Find Tickets
				</Button>
			</CardActions>
		</StyledCard>
	);
};

export default TicketCard;
