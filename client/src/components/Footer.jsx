// components/Footer.js
import { Box, Typography, Link, useTheme } from "@mui/material";

const Footer = () => {
	const theme = useTheme();

	return (
		<Box
			sx={{
				mt: 5,
				py: 3,
				backgroundColor: theme.palette.background.default, // Use theme's default background color
				color: theme.palette.text.primary, // Use theme's primary text color
				textAlign: "center",
			}}
		>
			<Typography variant="body2">
				&copy; {new Date().getFullYear()} Shasta Land. All Rights
				Reserved.
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
};

export default Footer;
