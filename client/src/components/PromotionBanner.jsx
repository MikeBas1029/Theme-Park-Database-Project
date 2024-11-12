// components/PromotionBanner.js
import { Box, Typography, Button, useTheme } from "@mui/material";

const PromotionBanner = ({ title, ctaText, ctaLink = "/promotions" }) => {
	const theme = useTheme();

	return (
		<Box
			sx={{
				backgroundColor: theme.palette.primary.main, // Use primary color from theme
				color: theme.palette.primary.contrastText, // Use contrast text for readability
				p: 3,
				display: "flex",
				alignItems: "center",
				justifyContent: "space-between",
				borderRadius: "8px",
				mb: 4,
			}}
		>
			<Typography variant="h5">{title}</Typography>
			<Button
				variant="contained"
				color="secondary"
				href={ctaLink}
				sx={{
					backgroundColor: theme.palette.secondary.main, // Secondary color for button
					color: theme.palette.secondary.contrastText, // Ensure text is readable
					"&:hover": {
						backgroundColor: theme.palette.secondary.dark,
					},
				}}
			>
				{ctaText}
			</Button>
		</Box>
	);
};

export default PromotionBanner;
