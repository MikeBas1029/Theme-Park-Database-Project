// CartContext.js
import React, { createContext, useContext, useState } from "react";

const CartContext = createContext();

export const useCart = () => useContext(CartContext);

export const CartProvider = ({ children }) => {
	const [cartItems, setCartItems] = useState([]);

	const addItem = (newItem) => {
		setCartItems((prevItems) => [
			...prevItems,
			{
				...newItem,
				quantity: newItem.quantity || 1,
				name: newItem.name || "Ticket",
				type: newItem.type || "Adult",
				price: newItem.price || 0,
				totalPrice: (newItem.quantity || 1) * (newItem.price || 0),
			},
		]);
	};

	const removeItem = (itemId) => {
		setCartItems((prevItems) =>
			prevItems.filter((item) => item.id !== itemId)
		);
	};

	const updateItemQuantity = (itemId, newQuantity) => {
		setCartItems((prevItems) =>
			prevItems.map((item) =>
				item.id === itemId
					? {
							...item,
							quantity: newQuantity,
							totalPrice: newQuantity * item.price,
						}
					: item
			)
		);
	};

	const calculateTotal = () => {
		return cartItems.reduce((total, item) => total + item.totalPrice, 0);
	};

	return (
		<CartContext.Provider
			value={{
				cartItems,
				addItem,
				removeItem,
				updateItemQuantity,
				calculateTotal,
			}}
		>
			{children}
		</CartContext.Provider>
	);
};

export default CartContext;
