// components/EventCard.js
import { Card, CardContent, Typography, Button, Box } from "@mui/material";

const EventCard = ({
	title,
	date,
	description = "Join us for an unforgettable experience!",
}) => (
	<Card
		sx={{
			width: 250,
			mb: 2,
			bgcolor: "#AEB7B3", // Add background color here
			// Other style options:
			// bgcolor: '#f0f7ff', // Light blue
			// bgcolor: '#fafafa', // Very light gray
			// bgcolor: 'rgba(25, 118, 210, 0.05)', // Light primary color
			transition: "all 0.2s ease",
			"&:hover": {
				boxShadow: 3,
			},
		}}
	>
		<CardContent>
			<Box sx={{ mb: 2 }}>
				<Typography variant="h5" component="div" color="#160C28">
					{title}
				</Typography>
				<Typography variant="subtitle2" color="black">
					{date}
				</Typography>
			</Box>
			<Typography variant="body2" color="black">
				{description}
			</Typography>
			<Button
				size="small"
				variant="contained"
				sx={{
					mt: 2,
					backgroundColor: "#2344A1",
					color: "white", // set the text color if needed
					"&:hover": {
						backgroundColor: "#3A5BC7", // optional: set a hover color
					},
				}}
			>
				Get Tickets
			</Button>
		</CardContent>
	</Card>
);

export default EventCard;
