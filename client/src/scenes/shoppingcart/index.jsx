// ShoppingCart.js
import React from "react";
import { Box, Typography, Button, Divider } from "@mui/material";
import ShoppingCartItem from "../../components/ShoppingCartItem";
import { useCart } from "../../components/context/CartContext";

const ShoppingCart = () => {
	const { cartItems, removeItem, updateItemQuantity, calculateTotal } =
		useCart();

	const handleRemoveItem = (item) => removeItem(item.id);
	const handleUpdateQuantity = (item, newValues) =>
		updateItemQuantity(item.id, newValues);

	const total = calculateTotal();

	return (
		<Box p={3}>
			<Typography variant="h4" gutterBottom>
				Shopping Cart
			</Typography>
			<Divider />

			{cartItems.length > 0 ? (
				cartItems.map((item) => (
					<ShoppingCartItem
						key={item.id}
						item={item}
						onRemove={handleRemoveItem}
						onUpdateQuantity={handleUpdateQuantity}
					/>
				))
			) : (
				<Typography variant="body1" mt={2}>
					Your cart is empty.
				</Typography>
			)}

			{cartItems.length > 0 && (
				<Box mt={3}>
					<Typography variant="h6">
						Total: ${total.toFixed(2)}
					</Typography>
					<Button variant="contained" color="primary" sx={{ mt: 2 }}>
						Proceed to Checkout
					</Button>
				</Box>
			)}
		</Box>
	);
};

export default ShoppingCart;
