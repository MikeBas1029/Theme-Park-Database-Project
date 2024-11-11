// components/RideCard.js
import {
	Card,
	CardContent,
	CardMedia,
	Typography,
	useTheme,
} from "@mui/material";

const RideCard = ({ title, image, description }) => {
	const theme = useTheme();

	return (
		<Card
			sx={{
				width: 250,
				mb: 2,
				bgcolor: theme.palette.background.paper, // Use theme's background color
				color: theme.palette.text.primary, // Use theme's primary text color
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
				<Typography
					variant="h5"
					component="div"
					color={theme.palette.text.primary} // Use theme's text color for title
				>
					{title}
				</Typography>
				<Typography
					variant="body2"
					color={theme.palette.text.secondary}
				>
					{description}
				</Typography>
			</CardContent>
		</Card>
	);
};

export default RideCard;
