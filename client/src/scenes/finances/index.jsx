import { Box, Button, IconButton, Typography, useTheme } from "@mui/material";
import { tokens } from "../../theme";
import PointOfSaleIcon from "@mui/icons-material/PointOfSale";
import PersonAddIcon from "@mui/icons-material/PersonAdd";
import Header from "../../components/Header";
import StatBox from "../../components/StatBox";
import DownloadButton from "../../components/DownloadButton";
import LineChart from "../../components/LineChart";

const Finances = ({ isOpen }) => {
	const theme = useTheme();
	const colors = tokens(theme.palette.mode);

	return (
		<Box
			m="20px"
			ml={isOpen ? "250px" : "80px"} // Adjust left margin based on isOpen
			transition="margin 0.3s ease" // Smooth transition for margin
		>
			{/* HEADER */}
			<Box
				display="flex"
				justifyContent="space-between"
				alignItems="center"
			>
				<Header title="Finances" subtitle="Track park expenditure" />

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
						<DownloadButton sx={{ mr: "10px" }} />
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
					gridColumn="span 4"
					backgroundColor={colors.primary[400]}
					display="flex"
					alignItems="center"
					justifyContent="center"
				>
					<StatBox
						title="$1,422,331"
						subtitle="Revenue"
						progress="0.75"
						increase="+14%"
						icon={
							<PersonAddIcon
								sx={{
									color: colors.greenAccent[600],
									fontSize: "26px",
								}}
							/>
						}
					/>
				</Box>
				<Box
					gridColumn="span 4"
					backgroundColor={colors.primary[400]}
					display="flex"
					alignItems="center"
					justifyContent="center"
				>
					<StatBox
						title="$431,225"
						subtitle="Expenses"
						progress="0.50"
						increase="+21%"
						icon={
							<PersonAddIcon
								sx={{
									color: colors.greenAccent[600],
									fontSize: "26px",
								}}
							/>
						}
					/>
				</Box>
				<Box
					gridColumn="span 2"
					backgroundColor={colors.primary[400]}
					display="flex"
					alignItems="center"
					justifyContent="center"
				>
					<StatBox
						title="51"
						subtitle="Unfulfilled Invoices"
						progress="0.30"
						increase="+5%"
						icon={
							<PersonAddIcon
								sx={{
									color: colors.greenAccent[600],
									fontSize: "26px",
								}}
							/>
						}
					/>
				</Box>
				<Box
					gridColumn="span 2"
					backgroundColor={colors.primary[400]}
					display="flex"
					alignItems="center"
					justifyContent="center"
				>
					<StatBox
						title="$153,348"
						subtitle="Amount Owed"
						progress="0.80"
						increase="+43%"
						icon={
							<PersonAddIcon
								sx={{
									color: colors.greenAccent[600],
									fontSize: "26px",
								}}
							/>
						}
					/>
				</Box>

				{/* ROW 2 */}
				<Box
					gridColumn="span 8"
					gridRow="span 5"
					backgroundColor={colors.primary[400]}
				>
					<Box
						mt="25px"
						p="0 30px"
						display="flex "
						justifyContent="space-between"
						alignItems="center"
					>
						<Box>
							<Typography
								variant="h5"
								fontWeight="600"
								color={colors.grey[100]}
							>
								Budget
							</Typography>
							<Typography
								variant="h3"
								fontWeight="bold"
								color={colors.greenAccent[500]}
							>
								$4658.27 remaining
							</Typography>
							<Typography
								variant="h5"
								fontWeight="bold"
								color={colors.grey[100]}
							>
								*$59,342.32 Total this Quarter
							</Typography>
						</Box>
						<Box>
							<DownloadButton
								sx={{
									fontSize: "26px",
									color: colors.greenAccent[500],
								}}
							/>
						</Box>
					</Box>
					<Box height="250px" m="-20px 0 0 0">
						<LineChart isDashboard={true} />
					</Box>
				</Box>
				<Box
					gridColumn="span 4"
					gridRow="span 3"
					backgroundColor={colors.primary[400]}
					overflow="auto"
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
							Transaction History
						</Typography>
					</Box>
					stuff here
				</Box>

				{/* ROW 3 */}
				<Box
					gridColumn="span 4"
					gridRow="span 2"
					backgroundColor={colors.primary[400]}
					p="30px"
				>
					<Typography variant="h5" fontWeight="600">
						Stock
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
							$48,352 STOCK VALUE
						</Typography>
						<Typography>Investors unhappy with results</Typography>
					</Box>
				</Box>
			</Box>
		</Box>
	);
};

export default Finances;
