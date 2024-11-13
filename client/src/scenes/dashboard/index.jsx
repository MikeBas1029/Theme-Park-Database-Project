import React, { useEffect, useState } from "react";
import {
	Box,
	Button,
	Typography,
	useTheme,
	Select,
	MenuItem,
} from "@mui/material";
import Header from "../../components/Header";
import EmojiPeopleIcon from "@mui/icons-material/EmojiPeople";
import ThunderstormIcon from "@mui/icons-material/Thunderstorm";
import { tokens } from "../../theme";
import StatBox from "../../components/StatBox";
import DownloadButton from "../../components/DownloadButton";
import Leaderboard from "../../components/Leaderboard";
import LineChart from "../../components/LineChart";
import MaintenanceSummary from "../../components/MaintenanceSummary";

const Dashboard = ({ isOpen }) => {
	// Accept isOpen prop
	const theme = useTheme();
	const colors = tokens(theme.palette.mode);

	// States for customer summary
	const [totalMonthlyCustomers, setTotalMonthlyCustomers] = useState(0);
	const [averageMonthlyCustomers, setAverageMonthlyCustomers] = useState(0);
	const [customerData, setCustomerData] = useState([]);
	const [loading, setLoading] = useState(true);

	// State(s) for dropdown(s)
	const [selectedRidesMonth, setSelectedRidesMonth] = useState(
		new Date().getMonth() + 1
	); // Default to the current month

	// Function to transform the response data
	const transformDataForNivo = (data) => {
		return data.map((entry) => {
			const year = new Date().getFullYear();
			const date = new Date(year, entry.month - 1, 1);
			date.setDate(date.getDate() + (entry.week - 1) * 7);
			const formattedDate = date.toISOString().split("T")[0];
			return { value: entry.num_customers, day: formattedDate };
		});
	};

	const [data, setData] = useState([]);

	// Fetching customer summary
	useEffect(() => {
		const fetchCustomerData = async () => {
			try {
				const response = await fetch(
					"https://theme-park-backend.ambitioussea-02dd25ab.eastus.azurecontainerapps.io/api/v1/reports/customer-count"
				);
				if (!response.ok)
					throw new Error("Network response was not ok");
				const data = await response.json();

				const totalCustomers = data.reduce(
					(acc, item) => acc + item.num_customers,
					0
				);
				const average = totalCustomers / data.length || 0;
				const transformedData = transformDataForNivo(data);
				setCustomerData(customerData);

				setAverageMonthlyCustomers(Math.round(average));
				setTotalMonthlyCustomers(totalCustomers);
			} catch (error) {
				console.error("Error fetching customer data:", error);
			} finally {
				setLoading(false);
			}
		};
		fetchCustomerData();
	}, []);

	return (
		<Box
			m="20px"
			ml={isOpen ? "250px" : "80px"}
			transition="margin 0.3s ease"
		>
			{" "}
			{/* Adjust left margin based on isOpen */}
			{/* HEADER */}
			<Box
				display="flex"
				justifyContent="space-between"
				alignItems="center"
			>
				<Header
					title="DASHBOARD"
					subtitle="Welcome to your dashboard"
				/>
				<Box>
					<Button
						sx={{
							backgroundColor: colors.blueAccent[700],
							color: colors.grey[100],
							fontSize: "14px",
							fontWeight: "bold",
							padding: "10px 20px",
						}}
					>
						<DownloadButton />
						Download Reports
					</Button>
				</Box>
			</Box>
			{/* GRID & CHARTS */}
			<Box
				display="grid"
				gridTemplateColumns="repeat(12, 1fr)"
				gridAutoRows="140px"
				gap="20px"
			>
				{/* ROW 1 */}
				<Box
					gridColumn="span 3"
					backgroundColor={colors.primary[400]}
					display="flex"
					alignItems="center"
					justifyContent="center"
				>
					{loading ? (
						<Typography>Loading...</Typography>
					) : (
						<StatBox
							title={averageMonthlyCustomers.toString()}
							subtitle="Avg. Monthly Customers"
							progress="0.50"
							increase="-50%"
							icon={
								<EmojiPeopleIcon
									sx={{
										color: colors.greenAccent[100],
										fontSize: "26px",
									}}
								/>
							}
						/>
					)}
				</Box>
				<Box
					gridColumn="span 3"
					backgroundColor={colors.primary[400]}
					display="flex"
					alignItems="center"
					justifyContent="center"
				>
					<StatBox
						title="⛔️"
						subtitle="..."
						progress="0.50"
						increase="-50%"
						icon={
							<EmojiPeopleIcon
								sx={{
									color: colors.greenAccent[100],
									fontSize: "26px",
								}}
							/>
						}
					/>
				</Box>
				<Box
					gridColumn="span 3"
					backgroundColor={colors.primary[400]}
					display="flex"
					alignItems="center"
					justifyContent="center"
				>
					<StatBox
						title="⛔️"
						subtitle="Rainouts this Month"
						progress="0.50"
						increase="-20%"
						icon={
							<ThunderstormIcon
								sx={{
									color: colors.greenAccent[100],
									fontSize: "26px",
								}}
							/>
						}
					/>
				</Box>
				<Box
					gridColumn="span 3"
					backgroundColor={colors.primary[400]}
					display="flex"
					alignItems="center"
					justifyContent="center"
				>
					<Typography>Recents incidents: N/A</Typography>
				</Box>

				{/* ROW 2 */}
				<Box
					gridColumn="span 8"
					gridRow="span 2"
					backgroundColor={colors.primary[400]}
				>
					<Box
						mt="25px"
						p="0 30px"
						display="flex"
						justifyContent="space-between"
						alignItems="center"
					>
						<Box>
							<Typography
								variant="h5"
								fontWeight="600"
								color={colors.grey[100]}
							>
								Customers Statistics
							</Typography>
							<Typography
								variant="h3"
								fontWeight="bold"
								color={colors.greenAccent[500]}
							>
								{totalMonthlyCustomers} total customers
							</Typography>
						</Box>
						<Box>
							<DownloadButton />
						</Box>
					</Box>
					<Box height="250px" m="-20px 0 0 0">
						<LineChart isDashboard={true} />
					</Box>
				</Box>
				<Box
					gridColumn="span 4"
					gridRow="span 2"
					backgroundColor={colors.primary[400]}
					overflow="hidden"
				>
					<Box
						display="flex"
						justifyContent="space-between"
						alignItems="center"
						borderBottom={`4px solid ${colors.primary[500]}`}
						colors={colors.grey[100]}
						p="15px"
					>
						<Typography
							color={colors.grey[100]}
							variant="h5"
							fontWeight="600"
						>
							Popular Rides
						</Typography>
						<Select
							value={selectedRidesMonth}
							onChange={(e) =>
								setSelectedRidesMonth(e.target.value)
							}
							style={{ color: colors.grey[100] }}
						>
							{[...Array(12).keys()].map((month) => (
								<MenuItem key={month + 1} value={month + 1}>
									{`Month ${month + 1}`}
								</MenuItem>
							))}
						</Select>
					</Box>
					<Leaderboard selectedMonth={selectedRidesMonth} />
				</Box>

				{/* ROW 3 */}
				<Box
					gridColumn="span 4"
					gridRow="span 2"
					backgroundColor={colors.primary[400]}
					p="30px"
				>
					<Typography variant="h5" fontWeight="600">
						Total Revenue
					</Typography>
					<Box
						display="flex"
						flexDirection="column"
						alignItems="center"
						mt="25px"
					>
						<Typography
							variant="h5"
							color={colors.greenAccent[500]}
							sx={{ mt: "15px" }}
						>
							${40}
						</Typography>
						<Typography>(+)Income: $40</Typography>
						<Typography>(-)Expenses: $0</Typography>
					</Box>
				</Box>
				<Box
					gridColumn="span 4"
					gridRow="span 2"
					backgroundColor={colors.primary[400]}
				>
					<Typography
						variant="h5"
						fontWeight="600"
						sx={{ padding: "30px 30px 0 30px" }}
					>
						Operational Summary
					</Typography>
					<Box height="250px" mt="-20px">
						<MaintenanceSummary />
					</Box>
				</Box>
				<Box
					gridColumn="span 4"
					gridRow="span 2"
					backgroundColor={colors.primary[400]}
					padding="30px"
				>
					<Typography
						variant="h5"
						fontWeight="600"
						sx={{ marginBottom: "15px" }}
					>
						Staff & Employees
					</Typography>
					<Box height="200px"></Box>
				</Box>
			</Box>
		</Box>
	);
};

export default Dashboard;
