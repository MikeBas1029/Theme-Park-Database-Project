import { createContext, useState, useMemo } from "react";
import { createTheme } from "@mui/material/styles";

export const tokens = (mode) => ({
	...(mode === "dark"
		? {
				text: "#F5F5F5",
				background: "#101010",
				primary: {
					main: "#2D81F7",
					light: "#3F8FFB",
					dark: "#204C92",
				},
				navbar: {
					main: "#1C1C1C",
				},
				secondary: {
					main: "#F77A72",
					light: "#FFAEA2",
				},
				accent: {
					main: "#E3C567",
				},
				neutral: {
					light: "#525252",
					main: "#424242",
					dark: "#303030",
				},
			}
		: {
				text: "#1C1C1C",
				background: "#F3F9FF",
				primary: {
					main: "#3A7DE0",
					light: "#4C9AF0",
					dark: "#2857A0",
				},
				navbar: {
					main: "#4C9AF0", // Sky blue color for a vibrant light mode navbar
				},
				secondary: {
					main: "#F5A623",
					light: "#F7B84A",
				},
				accent: {
					main: "#FFBB55",
				},
				neutral: {
					light: "#E0E0E0",
					main: "#C2C2C2",
					dark: "#8A8A8A",
				},
			}),
});

export const themeSettings = (mode) => {
	const colors = tokens(mode);

	return {
		palette: {
			mode: mode,
			text: {
				primary: colors.text,
			},
			background: {
				default: colors.background,
			},
			primary: {
				main: colors.primary.main,
				light: colors.primary.light,
				dark: colors.primary.dark,
			},
			secondary: {
				main: colors.secondary.main,
				light: colors.secondary.light,
			},
			accent: {
				main: colors.accent.main,
			},
			neutral: {
				light: colors.neutral.light,
				main: colors.neutral.main,
				dark: colors.neutral.dark,
			},
			navbar: {
				main:
					mode === "dark" ? colors.primary.dark : colors.primary.main,
			},
			// Define a lighter navbar text color for improved contrast in light mode
			navbarText: {
				main: mode === "dark" ? colors.text : "#ffffff",
			},
		},
		typography: {
			fontFamily: ["Source Sans Pro", "sans-serif"].join(","),
			fontSize: 12,
			h1: {
				fontFamily: ["Source Sans Pro", "sans-serif"].join(","),
				fontSize: 40,
			},
			h2: {
				fontFamily: ["Source Sans Pro", "sans-serif"].join(","),
				fontSize: 32,
			},
			h3: {
				fontFamily: ["Source Sans Pro", "sans-serif"].join(","),
				fontSize: 24,
			},
			h4: {
				fontFamily: ["Source Sans Pro", "sans-serif"].join(","),
				fontSize: 20,
			},
			h5: {
				fontFamily: ["Source Sans Pro", "sans-serif"].join(","),
				fontSize: 16,
			},
			h6: {
				fontFamily: ["Source Sans Pro", "sans-serif"].join(","),
				fontSize: 14,
			},
		},
	};
};

// Context for managing and toggling the display mode (light/dark)
export const DisplayModeContext = createContext({
	toggleDisplayMode: () => {},
});

// Custom hook to provide the theme and toggle functionality
export const useMode = () => {
	const [mode, setMode] = useState("light");

	const colorMode = useMemo(
		() => ({
			toggleDisplayMode: () =>
				setMode((prevMode) =>
					prevMode === "light" ? "dark" : "light"
				),
		}),
		[]
	);

	const theme = useMemo(() => createTheme(themeSettings(mode)), [mode]);

	return [theme, colorMode];
};
