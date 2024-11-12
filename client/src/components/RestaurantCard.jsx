import React from "react";
import { Card, CardContent, Typography, Box, Button } from "@mui/material";

export default function RestaurantCard({ restaurant, onClick, image }) {
	return (
		<Card
			onClick={onClick}
			sx={{
				position: "relative",
				cursor: "pointer",
				transition: "transform 0.3s, box-shadow 0.3s",
				"&:hover": {
					transform: "scale(1.05)",
					boxShadow: 6,
				},
				display: "flex",
				flexDirection: "row", // Align content and image horizontally
			}}
		>
			<CardContent sx={{ flex: 1 }}>
				<Typography variant="h4" fontWeight="bold" gutterBottom>
					{restaurant.restaurant_name}
				</Typography>
				<Typography variant="h6" fontWeight="bold" gutterBottom>
					{restaurant.cuisine_type}
				</Typography>
				<Box
					sx={{
						display: "flex",
						flexDirection: "column",
						alignItems: "flex-start",
						mt: 2,
						gap: 1,
					}}
				>
					<Typography variant="body2" color="text.secondary">
						Opening Time: {restaurant.opening_time}
					</Typography>
					<Typography variant="body2" color="text.secondary">
						Closing Time: {restaurant.closing_time}
					</Typography>
					<Button
						variant="outlined"
						color="primary"
						size="small"
						onClick={(e) => {
							e.stopPropagation();
							onClick();
						}}
					>
						See more
					</Button>
				</Box>
			</CardContent>
			<Box
				component="img"
				src={image || "/assets/default-restaurant.jpg"}
				alt={restaurant.restaurant_name}
				sx={{
					width: 180,
					height: "100%",
					objectFit: "cover",
					borderRadius: "0 4px 4px 0",
				}}
			/>
		</Card>
	);
}
