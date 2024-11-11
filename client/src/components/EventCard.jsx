// components/EventCard.js
import {
	Card,
	CardContent,
	Typography,
	Button,
	Box,
	useTheme,
} from "@mui/material";

const EventCard = ({
	title,
	date,
	description = "Join us for an unforgettable experience!",
}) => {
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
			<CardContent>
				<Box sx={{ mb: 2 }}>
					<Typography
						variant="h5"
						component="div"
						color={theme.palette.text.primary}
					>
						{title}
					</Typography>
					<Typography
						variant="subtitle2"
						color={theme.palette.text.secondary}
					>
						{date}
					</Typography>
				</Box>
				<Typography variant="body2" color={theme.palette.text.primary}>
					{description}
				</Typography>
				<Button
					size="small"
					variant="contained"
					sx={{
						mt: 2,
						backgroundColor: theme.palette.primary.main,
						color: theme.palette.primary.contrastText, // Use theme's contrast text color
						"&:hover": {
							backgroundColor: theme.palette.primary.dark, // Use theme's dark shade on hover
						},
					}}
				>
					Get Tickets
				</Button>
			</CardContent>
		</Card>
	);
};

export default EventCard;
