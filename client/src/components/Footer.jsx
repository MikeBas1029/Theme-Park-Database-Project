// components/Footer.js
import { Box, Typography, Link } from "@mui/material";

const Footer = () => (
	<Box
		sx={{
			mt: 5,
			py: 3,
			backgroundColor: "#333",
			color: "white",
			textAlign: "center",
		}}
	>
		<Typography variant="body2">
			&copy; {new Date().getFullYear()} Shasta Land. All Rights Reserved.
		</Typography>
		<Box sx={{ mt: 1 }}>
			<Link href="/privacy" color="inherit" sx={{ mx: 1 }}>
				Privacy Policy
			</Link>
			<Link href="/terms" color="inherit" sx={{ mx: 1 }}>
				Terms of Service
			</Link>
			<Link href="/contact" color="inherit" sx={{ mx: 1 }}>
				Contact Us
			</Link>
		</Box>
	</Box>
);

export default Footer;
