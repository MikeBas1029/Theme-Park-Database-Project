// TicketSelectionModal.js
import React, { useState } from "react";
import {
	Dialog,
	DialogTitle,
	DialogContent,
	DialogActions,
	Button,
	Typography,
	Box,
} from "@mui/material";
import { LocalizationProvider } from "@mui/x-date-pickers";
import { AdapterDateFns } from "@mui/x-date-pickers/AdapterDateFns";
import CalendarComponent from "./Calendar";
import TicketCounter from "./TicketCounter";

const TicketSelectionModal = ({ open, onClose, ticket }) => {
	const [selectedDate, setSelectedDate] = useState(null);
	const [adultCount, setAdultCount] = useState(1);
	const [childCount, setChildCount] = useState(0);
	const [step, setStep] = useState(1); // Step 1: Ticket Count, Step 2: Date Selection

	const handleDateSelect = (date) => {
		setSelectedDate(date);
	};

	const handleNext = () => {
		setStep(2);
	};

	const handleBack = () => {
		setStep(1);
	};

	const handleConfirm = () => {
		console.log("Selected date:", selectedDate);
		console.log("Adult tickets:", adultCount, "Child tickets:", childCount);
		onClose(); // Pass data back if needed
	};

	return (
		<LocalizationProvider dateAdapter={AdapterDateFns}>
			<Dialog open={open} onClose={onClose}>
				<DialogTitle sx={{ fontSize: "1.2rem", fontWeight: "bold" }}>
					Select Tickets
				</DialogTitle>
				<DialogContent dividers>
					<Box
						display="flex"
						flexDirection="column"
						alignItems="center"
					>
						{step === 1 ? (
							<>
								<Typography
									variant="body1"
									align="center"
									gutterBottom
								>
									Select the number of tickets
								</Typography>
								<TicketCounter
									label="Adult Ticket"
									price={ticket.base_price}
									count={adultCount}
									setCount={setAdultCount}
								/>
								<TicketCounter
									label="Child Ticket"
									price={(ticket.base_price * 0.8).toFixed(2)}
									count={childCount}
									setCount={setChildCount}
								/>
							</>
						) : (
							<>
								<Typography
									variant="h5"
									align="center"
									gutterBottom
								>
									Choose the date for your visit
								</Typography>
								<CalendarComponent
									onDateSelect={handleDateSelect}
								/>

								{/* Display selected details */}
								<Box mt={2} textAlign="center">
									<Typography
										variant="body2"
										color="textSecondary"
									>
										<strong>Selected Tickets:</strong>{" "}
										{adultCount} Adult, {childCount} Child
									</Typography>
									{selectedDate && (
										<Typography
											variant="body2"
											color="textSecondary"
										>
											<strong>Selected Date:</strong>{" "}
											{selectedDate.toDateString()}
										</Typography>
									)}
								</Box>
							</>
						)}
					</Box>
				</DialogContent>
				<DialogActions>
					{step === 2 && (
						<Button onClick={handleBack} color="secondary">
							Back
						</Button>
					)}
					<Button onClick={onClose} color="secondary">
						Cancel
					</Button>
					{step === 1 ? (
						<Button
							onClick={handleNext}
							color="primary"
							variant="contained"
						>
							Next
						</Button>
					) : (
						<Button
							onClick={handleConfirm}
							color="primary"
							variant="contained"
						>
							Confirm
						</Button>
					)}
				</DialogActions>
			</Dialog>
		</LocalizationProvider>
	);
};

export default TicketSelectionModal;
