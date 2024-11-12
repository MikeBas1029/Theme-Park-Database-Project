// Checkout.js
import React, { useState } from "react";
import {
	Box,
	Typography,
	TextField,
	Button,
	Divider,
	Paper,
	Grid,
} from "@mui/material";
import { useCart } from "../../components/context/CartContext";
import { useNavigate } from "react-router-dom";

const Checkout = () => {
	const { cartItems, calculateTotal } = useCart();
	const navigate = useNavigate();

	const [formData, setFormData] = useState({
		name: "",
		email: "",
		address: "",
		city: "",
		state: "",
		zip: "",
		cardNumber: "",
		expirationDate: "",
		cvc: "",
	});

	const handleChange = (e) => {
		setFormData({
			...formData,
			[e.target.name]: e.target.value,
		});
	};

	const handlePlaceOrder = () => {
		console.log("Order placed with data:", formData);
		navigate("/confirmation"); // Redirect to a confirmation page
	};

	const total = calculateTotal();

	return (
		<Box p={3} maxWidth="md" mx="auto">
			<Typography variant="h4" gutterBottom align="center">
				Checkout
			</Typography>
			<Divider />

			<Box
				mt={3}
				component={Paper}
				elevation={3}
				p={3}
				borderRadius="8px"
			>
				{/* Order Summary */}
				<Typography variant="h6" gutterBottom>
					Order Summary
				</Typography>
				<Box mt={1} mb={3}>
					{cartItems.length > 0 ? (
						cartItems.map((item, index) => (
							<Box
								key={index}
								display="flex"
								justifyContent="space-between"
								mb={1}
							>
								{/* Display item name, type, quantity, and individual price */}
								<Typography>
									{item.quantity} x {item.name}- $
									{item.price
										? item.price.toFixed(2)
										: "0.00"}
								</Typography>
								{/* Display the total price for the item (price * quantity) */}
								<Typography>
									$
									{item.price
										? (item.price * item.quantity).toFixed(
												2
											)
										: "0.00"}
								</Typography>
							</Box>
						))
					) : (
						<Typography variant="body2" color="textSecondary">
							No items in cart.
						</Typography>
					)}
					<Divider sx={{ my: 2 }} />
					<Typography variant="h6" align="right">
						Total: ${total.toFixed(2)}
					</Typography>
				</Box>

				{/* Customer Information */}
				<Typography variant="h6" gutterBottom>
					Customer Information
				</Typography>
				<Grid container spacing={2}>
					<Grid item xs={12} sm={6}>
						<TextField
							fullWidth
							label="Full Name"
							name="name"
							value={formData.name}
							onChange={handleChange}
						/>
					</Grid>
					<Grid item xs={12} sm={6}>
						<TextField
							fullWidth
							label="Email"
							name="email"
							type="email"
							value={formData.email}
							onChange={handleChange}
						/>
					</Grid>
				</Grid>

				{/* Billing Address */}
				<Typography variant="h6" gutterBottom mt={3}>
					Billing Address
				</Typography>
				<Grid container spacing={2}>
					<Grid item xs={12}>
						<TextField
							fullWidth
							label="Address"
							name="address"
							value={formData.address}
							onChange={handleChange}
						/>
					</Grid>
					<Grid item xs={12} sm={6}>
						<TextField
							fullWidth
							label="City"
							name="city"
							value={formData.city}
							onChange={handleChange}
						/>
					</Grid>
					<Grid item xs={6} sm={3}>
						<TextField
							fullWidth
							label="State"
							name="state"
							value={formData.state}
							onChange={handleChange}
						/>
					</Grid>
					<Grid item xs={6} sm={3}>
						<TextField
							fullWidth
							label="ZIP Code"
							name="zip"
							value={formData.zip}
							onChange={handleChange}
							type="number"
						/>
					</Grid>
				</Grid>

				{/* Payment Information */}
				<Typography variant="h6" gutterBottom mt={3}>
					Payment Information
				</Typography>
				<Grid container spacing={2}>
					<Grid item xs={12}>
						<TextField
							fullWidth
							label="Card Number"
							name="cardNumber"
							value={formData.cardNumber}
							onChange={handleChange}
							type="number"
						/>
					</Grid>
					<Grid item xs={6}>
						<TextField
							fullWidth
							label="Expiration Date (MM/YY)"
							name="expirationDate"
							value={formData.expirationDate}
							onChange={handleChange}
							placeholder="MM/YY"
						/>
					</Grid>
					<Grid item xs={6}>
						<TextField
							fullWidth
							label="CVC"
							name="cvc"
							value={formData.cvc}
							onChange={handleChange}
							type="number"
						/>
					</Grid>
				</Grid>

				{/* Buttons */}
				<Box mt={4} display="flex" justifyContent="space-between">
					<Button
						variant="outlined"
						color="secondary"
						onClick={() => navigate("/shopping-cart")}
					>
						Back to Shopping Cart
					</Button>
					<Button
						variant="contained"
						color="primary"
						onClick={handlePlaceOrder}
					>
						Place Order
					</Button>
				</Box>
			</Box>
		</Box>
	);
};

export default Checkout;
