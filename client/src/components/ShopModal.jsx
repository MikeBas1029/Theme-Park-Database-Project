// // components/ShopsModal.js
// import React from "react";
// import {
// 	Dialog,
// 	DialogContent,
// 	DialogTitle,
// 	Typography,
// 	Box,
// } from "@mui/material";

// export default function ShopsModal({ open, onClose, shop, image }) {
// 	return (
// 		<Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
// 			<DialogTitle>{shop.shop_name}</DialogTitle>
// 			<DialogContent>
// 				<Box
// 					component="img"
// 					src={image}
// 					alt={shop.shop_name}
// 					sx={{
// 						width: "60%",
// 						borderRadius: 2,
// 						mb: 2,
// 						maxWidth: 300,
// 					}}
// 				/>
// 				<Typography variant="body1" gutterBottom>
// 					{shop.full_description ||
// 						"No additional details available."}
// 				</Typography>
// 				<Typography variant="body2" color="text.secondary">
// 					Rating: {shop.rating || "N/A"}
// 				</Typography>
// 			</DialogContent>
// 		</Dialog>
// 	);
// }

import React from "react";
import {
	Dialog,
	DialogTitle,
	DialogContent,
	DialogActions,
	Typography,
	Box,
	Button,
} from "@mui/material";

export default function ShopsModal({ open, onClose, shop, image }) {
	return (
		<Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
			<DialogTitle>
				<Typography variant="h3" fontWeight="bold">
					{shop.shop_name}
				</Typography>
			</DialogTitle>
			<DialogContent>
				<Box
					display="flex"
					flexDirection="column"
					alignItems="center"
					gap={2}
				>
					<Box
						component="img"
						src={image}
						alt={shop.shop_name}
						sx={{
							width: "100%",
							maxWidth: 300, // Set max width for the image
							borderRadius: 2,
							objectFit: "cover",
							mb: 2,
						}}
					/>
					<Typography variant="h5" color="text.primary">
						About us
					</Typography>
					<Typography variant="body1" color="text.secondary">
						{shop.description || "Come check us Out!"}
					</Typography>
				</Box>
			</DialogContent>
			<DialogActions>
				<Button onClick={onClose} variant="contained" color="primary">
					Close
				</Button>
			</DialogActions>
		</Dialog>
	);
}