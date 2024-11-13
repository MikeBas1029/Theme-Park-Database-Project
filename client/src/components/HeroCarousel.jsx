// components/HeroCarousel.js
import { Box, Typography, Button } from "@mui/material";
import Carousel from "react-material-ui-carousel"; // Use any carousel package or implement your own

const HeroCarousel = () => {
	const items = [
		{
			image: "assets/hero1.jpeg",
			title: "Welcome to Shasta Land",
			subtitle: "The Adventure of a Lifetime Awaits!",
			ctaText: "Buy Tickets",
			ctaLink: "/purchase-tickets",
		},
		{
			image: "assets/hero2.jpeg",
			title: "Circus Extravaganza",
			subtitle: "Come see one of our most popular shows!",
			ctaText: "Find Dates",
			ctaLink: "/customer-events",
		},
		{
			image: "assets/hero3.jpeg",
			title: "The Galaxy Twister",
			subtitle: "Feel the Rush on Our Fastest Roller Coaster!",
			ctaText: "See Rides",
			ctaLink: "/customer-rides",
		},
	];

	return (
		<Carousel>
			{items.map((item, index) => (
				<Box
					key={index}
					sx={{
						position: "relative",
						backgroundImage: `url(${item.image})`,
						backgroundSize: "cover",
						backgroundPosition: "center",
						height: "400px",
						color: "white",
						display: "flex",
						flexDirection: "column",
						justifyContent: "center",
						alignItems: "center",
						textAlign: "center",
						overflow: "hidden",
						"&::before": {
							content: '""',
							position: "absolute",
							top: 0,
							left: 0,
							width: "100%",
							height: "100%",
							backgroundColor: "rgba(0, 0, 0, 0.3)", // Adjust opacity and color
							zIndex: 1,
						},
						"& > *": {
							position: "relative",
							zIndex: 2,
						},
					}}
				>
					<Typography
						variant="h1"
						sx={{ color: "white" }}
						gutterBottom
					>
						{item.title}
					</Typography>
					<Typography variant="h5" sx={{ color: "white" }}>
						{item.subtitle}
					</Typography>
					<Button
						variant="contained"
						href={item.ctaLink}
						sx={{
							mt: 2,
							mb: 2,
							px: 4,
							borderRadius: 1,
							backgroundColor: "#2344A1",
							color: "white",
							"&:hover": {
								backgroundColor: "#3A5BC7",
							},
						}}
					>
						{item.ctaText}
					</Button>
				</Box>
			))}
		</Carousel>
	);
};

export default HeroCarousel;
