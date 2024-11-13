// Cart.js
import React from "react";
import { IconButton, Badge } from "@mui/material";
import ShoppingCartOutlinedIcon from "@mui/icons-material/ShoppingCartOutlined";
import { useCart } from "./context/CartContext";
import { useNavigate } from "react-router-dom";

const Cart = () => {
	const navigate = useNavigate();
	const { cartItems } = useCart();

	const cartItemCount = cartItems.reduce(
		(total, item) => total + (item.quantity || 1),
		0
	);

	return (
		<IconButton onClick={() => navigate("/shopping-cart")}>
			<Badge badgeContent={cartItemCount} color="error">
				<ShoppingCartOutlinedIcon />
			</Badge>
		</IconButton>
	);
};

export default Cart;
