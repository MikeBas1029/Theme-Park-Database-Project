import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import App from "./App";
import { BrowserRouter } from "react-router-dom";
import { UserProvider } from "./components/context/UserContext";
import { CartProvider } from "./components/context/CartContext";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
	<React.StrictMode>
		<UserProvider>
			<CartProvider>
				<BrowserRouter>
					<App />
				</BrowserRouter>
			</CartProvider>
		</UserProvider>
	</React.StrictMode>
);
