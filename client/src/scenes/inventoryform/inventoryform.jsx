import {
	Box,
	Button,
	TextField,
	Select,
	MenuItem,
	FormControl,
	InputLabel,
	IconButton,
} from "@mui/material";
import { Formik } from "formik";
import * as yup from "yup";
import useMediaQuery from "@mui/material/useMediaQuery";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import Header from "../../components/Header";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const initialValues = {
	sku: "",
	name: "",
	category: "Merchandise",
	price: "",
	cost: "",
	status: "Active",
	vendor_id: "",
};

const userSchema = yup.object().shape({
	sku: yup.string().required("required"),
	name: yup.string().required("required"),
	category: yup.string().required("required"),
	price: yup.string().required("required"),
	cost: yup.string().required("required"),
	vendor_id: yup.string().required("required"),
});

const Form = ({ isOpen }) => {
	const isNonMobile = useMediaQuery("(min-width:600px)");
	const navigate = useNavigate();

	const handleFormSubmit = async (values) => {
		// Create a request body that matches the expected API schema
		const requestBody = {
			sku: values.sku,
			name: values.name,
			category: "Merchandise",
			price: values.price,
			cost: values.cost,
			status: "Active", //set default status of new item to active
			vendor_id: values.vendor_id,
		};

		// Check for any missing or incorrect values
		const missingFields = [];
		Object.entries(requestBody).forEach(([key, value]) => {
			if (value === "" || value === undefined) {
				missingFields.push(key);
			}
		});

		if (missingFields.length > 0) {
			console.error("Missing fields:", missingFields);
			alert(
				`Please fill in the following fields: ${missingFields.join(", ")}`
			);
			return; // Stop submission if there are missing fields
		}

		try {
			const response = await axios.post(
				"https://theme-park-backend.ambitioussea-02dd25ab.eastus.azurecontainerapps.io/api/v1/items/",
				requestBody
			);
			console.log(response.data); // Handle the response as needed
			navigate("/"); // Navigate after successful submission
		} catch (error) {
			console.error("Error submitting form:", error); // Handle the error appropriately
			if (error.response) {
				console.error("Response data:", error.response.data); // Log the response data
				alert(
					"Submission failed. Please check the console for more details."
				); // Notify user
			}
		}
	};

	return (
		<Box
			m="20px"
			ml={isOpen ? "250px" : "80px"} // Adjust left margin based on isOpen
			transition="margin 0.3s ease" // Smooth transition for margin
		>
			<IconButton onClick={() => navigate(-1)}>
				<ArrowBackIcon sx={{ fontSize: "30px", color: "grey" }} />
			</IconButton>

			<Header
				title="ADD NEW ITEM"
				subtitle="Add a new item into inventory"
			/>
			<Formik
				onSubmit={handleFormSubmit}
				initialValues={initialValues}
				validationSchema={userSchema}
			>
				{({
					values,
					errors,
					touched,
					handleBlur,
					handleChange,
					handleSubmit,
				}) => (
					<form onSubmit={handleSubmit}>
						<Box
							display="grid"
							gap="30px"
							gridTemplateColumns="repeat(4, minmax(0, 1fr))"
							sx={{
								"& > div": {
									gridColumn: isNonMobile
										? undefined
										: "span 4",
								},
							}}
						>
							<TextField
								fullWidth
								variant="filled"
								type="text"
								label="Item ID"
								onBlur={handleBlur}
								onChange={handleChange}
								value={values.sku}
								name="sku"
								error={!!touched.sku && !!errors.sku}
								helperText={touched.sku && errors.sku}
								sx={{
									gridColumn: "span 2",
								}}
							/>

							<TextField
								fullWidth
								variant="filled"
								type="text"
								label="Vendor ID"
								onBlur={handleBlur}
								onChange={handleChange}
								value={values.vendor_id}
								name="vendor_id"
								error={
									!!touched.vendor_id && !!errors.vendor_id
								}
								helperText={
									touched.vendor_id && errors.vendor_id
								}
								sx={{
									gridColumn: "span 2",
								}}
							/>

							<FormControl
								fullWidth
								variant="filled"
								sx={{ gridColumn: "span 2" }}
							>
								<InputLabel id="category-label">
									Category
								</InputLabel>
								<Select
									labelId="category-label"
									id="category"
									name="category"
									value={values.category}
									onBlur={handleBlur}
									onChange={handleChange}
									error={
										!!touched.category && !!errors.category
									}
								>
									<MenuItem value="Merchandise">
										Merchandise
									</MenuItem>
									<MenuItem value="Concession">
										Concessions
									</MenuItem>
									<MenuItem value="Entertainment">
										Entertainment
									</MenuItem>
								</Select>
								{touched.category && errors.category && (
									<div style={{ color: "red" }}>
										{errors.category}
									</div>
								)}
							</FormControl>

							<TextField
								fullWidth
								variant="filled"
								type="text"
								label="Item Name"
								onBlur={handleBlur}
								onChange={handleChange}
								value={values.name}
								name="name"
								error={!!touched.name && !!errors.name}
								helperText={touched.name && errors.name}
								sx={{
									gridColumn: "span 2",
								}}
							/>

							<TextField
								fullWidth
								variant="filled"
								type="text"
								label="Price"
								onBlur={handleBlur}
								onChange={handleChange}
								value={values.price}
								name="price"
								error={!!touched.price && !!errors.price}
								helperText={touched.price && errors.price}
								sx={{
									gridColumn: "span 2",
								}}
							/>

							<TextField
								fullWidth
								variant="filled"
								type="text"
								label="Unit Cost"
								onBlur={handleBlur}
								onChange={handleChange}
								value={values.cost}
								name="cost"
								error={!!touched.cost && !!errors.cost}
								helperText={touched.cost && errors.cost}
								sx={{
									gridColumn: "span 2",
								}}
							/>
						</Box>

						<Box display="flex" justifyContent="end" mt="20px">
							<Button
								type="submit"
								color="secondary"
								variant="contained"
							>
								Add item into Inventory
							</Button>
						</Box>
					</form>
				)}
			</Formik>
		</Box>
	);
};

export default Form;
