// components/RideCard.js
import {
	Card,
	CardContent,
	CardMedia,
	Typography,
	Button,
} from "@mui/material";

const RideCard = ({ title, image, description }) => (
	<Card
		sx={{
			width: 250,
			mb: 2,
			bgcolor: "#AEB7B3",
			transition: "all 0.2s ease",
			"&:hover": {
				boxShadow: 3,
			},
		}}
	>
		<CardMedia
			component="img"
			alt={title}
			height="140"
			image={image}
			title={title}
		/>
		<CardContent>
			<Typography variant="h5" component="div" color="#160C28">
				{title}
			</Typography>
			<Typography variant="body2" color="black">
				{description}
			</Typography>
			{/* <Button size="small" color="black" sx={{ mt: 1 }}>
				Learn More
			</Button> */}
		</CardContent>
	</Card>
);

export default RideCard;
