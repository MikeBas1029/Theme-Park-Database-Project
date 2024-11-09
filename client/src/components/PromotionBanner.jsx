// components/PromotionBanner.js
import { Box, Typography, Button } from "@mui/material";

const PromotionBanner = ({ title, ctaText, ctaLink = "/promotions" }) => (
	<Box
		sx={{
			backgroundColor: "#FF5722",
			color: "white",
			p: 3,
			display: "flex",
			alignItems: "center",
			justifyContent: "space-between",
			borderRadius: "8px",
			mb: 4,
		}}
	>
		<Typography variant="h5">{title}</Typography>
		<Button variant="contained" color="secondary" href={ctaLink}>
			{ctaText}
		</Button>
	</Box>
);

export default PromotionBanner;
