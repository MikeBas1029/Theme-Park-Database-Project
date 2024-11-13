import { useState } from "react";
import { Box, Typography, Button, useTheme } from "@mui/material";
import PromoModal from "./PromoModal";

const PromotionBanner = ({ title, ctaText }) => {
	const theme = useTheme();
	const [isPromoOpen, setIsPromoOpen] = useState(false);

	const handleOpenPromo = () => {
		setIsPromoOpen(true);
	};

	const handleClosePromo = () => {
		setIsPromoOpen(false);
	};

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
				onClick={handleOpenPromo} // Open modal on button click
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

			{/* Promo Modal */}
			<PromoModal open={isPromoOpen} onClose={handleClosePromo} />
		</Box>
	);
};

export default PromotionBanner;
