// CartContext.js
import React, { createContext, useContext, useState } from "react";

const CartContext = createContext();

export const useCart = () => useContext(CartContext);

export const CartProvider = ({ children }) => {
	const [cartItems, setCartItems] = useState([]);

	const addItem = (newItem) => {
		setCartItems((prevItems) => {
			const existingItemIndex = prevItems.findIndex(
				(item) => item.id === newItem.id
			);

			if (existingItemIndex !== -1) {
				// If item exists, increase the quantity
				const updatedItems = [...prevItems];
				const existingItem = updatedItems[existingItemIndex];
				updatedItems[existingItemIndex] = {
					...existingItem,
					quantity:
						(existingItem.quantity || 1) + (newItem.quantity || 1),
				};
				return updatedItems;
			} else {
				// If item does not exist, add it to the cart with initial quantity
				return [
					...prevItems,
					{ ...newItem, quantity: newItem.quantity || 1 },
				];
			}
		});
	};

	const removeItem = (itemId) => {
		setCartItems((prevItems) =>
			prevItems.filter((item) => item.id !== itemId)
		);
	};

	const updateItemQuantity = (itemId, newValues) => {
		setCartItems((prevItems) =>
			prevItems.map((item) =>
				item.id === itemId ? { ...item, ...newValues } : item
			)
		);
	};

	const calculateTotal = () => {
		return cartItems.reduce(
			(total, item) => total + item.totalPrice * (item.quantity || 1),
			0
		);
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
