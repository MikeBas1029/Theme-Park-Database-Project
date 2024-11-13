// MyTickets.js
import React, { useEffect, useState } from "react";
import { Box, Typography, Tab, Tabs, Paper, Divider } from "@mui/material";
import { useUser } from "../../components/context/UserContext";

const MyTickets = () => {
	const { user } = useUser();
	const [tickets, setTickets] = useState([]);
	const [activeTab, setActiveTab] = useState(0);
	const [activeTickets, setActiveTickets] = useState([]);
	const [expiredTickets, setExpiredTickets] = useState([]);

	useEffect(() => {
		const fetchTickets = async () => {
			if (user?.customer_id) {
				try {
					const response = await fetch(
						`https://theme-park-backend.ambitioussea-02dd25ab.eastus.azurecontainerapps.io/api/v1/tickets/user/${user.customer_id}`
					);
					if (response.ok) {
						const data = await response.json();
						setTickets(data);
						// Separate tickets by status
						setActiveTickets(
							data.filter((ticket) => ticket.status === "ACTIVE")
						);
						setExpiredTickets(
							data.filter((ticket) => ticket.status === "EXPIRED")
						);
					} else {
						console.error("Failed to fetch tickets.");
					}
				} catch (error) {
					console.error("Error fetching tickets:", error);
				}
			}
		};
		fetchTickets();
	}, [user]);

	const handleTabChange = (event, newValue) => {
		setActiveTab(newValue);
	};

	return (
		<Box p={3} maxWidth="md" mx="auto">
			<Typography variant="h3" gutterBottom align="center">
				My Tickets
			</Typography>
			<Divider />

			<Box mt={3}>
				<Tabs value={activeTab} onChange={handleTabChange} centered>
					<Tab label="Active Tickets" sx={{ fontSize: "1rem" }} />
					<Tab label="Expired Tickets" sx={{ fontSize: "1rem" }} />
				</Tabs>

				{activeTab === 0 ? (
					<TicketsList tickets={activeTickets} />
				) : (
					<TicketsList tickets={expiredTickets} />
				)}
			</Box>
		</Box>
	);
};

const TicketsList = ({ tickets }) => (
	<Box mt={2}>
		{tickets.length > 0 ? (
			tickets.map((ticket, index) => (
				<Paper
					key={ticket.ticket_id}
					elevation={3}
					sx={{ p: 2, mb: 2 }}
				>
					<Typography variant="h4">Park Pass</Typography>
					<Typography variant="h6">
						Ticket ID: {ticket.ticket_id}
					</Typography>
					<Typography variant="body2" color="textSecondary">
						Purchase Date: {ticket.purchase_date}
					</Typography>
					<Typography variant="body2" color="textSecondary">
						Start Date: {ticket.start_date}
					</Typography>
					<Typography variant="body2" color="textSecondary">
						Expiration Date: {ticket.expiration_date}
					</Typography>
					<Typography variant="body2" color="textSecondary">
						Price: ${ticket.price.toFixed(2)}
					</Typography>
					<Typography variant="body2" color="textSecondary">
						Status: {ticket.status}
					</Typography>
				</Paper>
			))
		) : (
			<Typography align="center" color="textSecondary">
				No tickets found.
			</Typography>
		)}
	</Box>
);

export default MyTickets;
