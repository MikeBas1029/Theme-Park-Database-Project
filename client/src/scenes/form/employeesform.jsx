import { Box, Button, IconButton, TextField, MenuItem, Select, FormControl, InputLabel } from "@mui/material";
import { Formik } from "formik";
import * as yup from "yup";
import useMediaQuery from "@mui/material/useMediaQuery";
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import Header from "../../components/Header";
import { useNavigate } from 'react-router-dom';
import axios from "axios";
import BasicDateTimePicker from "../../components/DateTime";
;
const initialValues = {
    ssn: "",
    first_name: "", 
    last_name: "",
    middle_initial: "",
    phone_number: "",
    email: "",
    address_line1: "",
    address_line2: "",
    city: "",
    state: "",
    zip_code: "",
    country: "",
    dob: "",
    start_date: "",
    employee_type: "",
    hourly_wage: "",
    salary: "",
    job_function: "",
    gender: "",
    title: "",
};


const phoneRegExp =
  /^((\+[1-9]{1,4}[ -]?)|(\([0-9]{2,3}\)[ -]?)|([0-9]{2,4})[ -]?)*?[0-9]{3,4}[ -]?[0-9]{3,4}$/; {/*highly comprehensive regExp (?) works for international nums */}

  const formatPhoneNumber = (value) => {
    if (!value) return value;
    // Remove non-numeric characters
    const cleaned = ('' + value).replace(/\D/g, '');
    //Format as xxx-xxx-xxxx
    const match = cleaned.match(/^(\d{0,3})(\d{0,3})(\d{0,4})$/);
    if (match) {
        return `${match[1]}${match[2] ? '-' : ''}${match[2]}${match[3] ? '-' : ''}${match[3]}`;
    }
    return value;
};

const formatSSN = (value) => {
    if (!value) return value;
    // Remove non-numeric characters
    const cleaned = ('' + value).replace(/\D/g, '');
    //Format as xx-xx-xxxx
    const match = cleaned.match(/^(\d{0,3})(\d{0,2})(\d{0,4})$/);
    if (match) {
        return `${match[1]}${match[2] ? '-' : ''}${match[2]}${match[3] ? '-' : ''}${match[3]}`;
    }
    return value;
};

const formatDate = (value) => {
    if (!value) return value;
    // Remove non-numeric characters
    const cleaned = ('' + value).replace(/\D/g, '');
    //Format as MM/DD/YYYY
    const match = cleaned.match(/(\d{0,4})(\d{0,2})(\d{0,2})/);
    if (match) {
        const month = match[1];
        const day = match[2];
        const year = match[3];
        
        return `${month}${month && day ? '-' : ''}${day}${day && year ? '-' : ''}${year}`;
    }
    return value;
};

const formatHourlyWage = (value) => {
    if (!value) return "0.00"; // Start from 0.00
    // Remove non-numeric characters
    const cleaned = ('' + value).replace(/\D/g, '');
    const numericValue = parseFloat(cleaned) / 100; // Shift left
    return numericValue.toLocaleString('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
    });
};


const formatSalary = (value) => {
    if (!value) return "$0"; // Return "$0" for no input
    const cleaned = ('' + value).replace(/\D/g, ''); // Remove non-numeric characters
    const numericValue = parseFloat(cleaned); // Convert to a number

    if (isNaN(numericValue)) return "$0"; // Handle NaN

    return `$${numericValue.toLocaleString('en-US', {
        style: 'decimal',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0,
    })}`;
};




const userSchema = yup.object().shape({
    first_name: yup.string().required("required"),
    middle_initial: yup.string().required("required"),
    last_name: yup.string().required("required"),
    ssn: yup.string().required("required"),
    email: yup.string().email("Invalid email").required("required"),
    phone_number: yup.string().matches(phoneRegExp, "Phone number is not valid").required("required"),
    address_line1: yup.string().required("required"),
    address_line2: yup.string(),
    city: yup.string().required("required"),
    state: yup.string().required("required"),
    country: yup.string().required("required"),
    zip_code: yup.string().required("required"),
    dob: yup.string().required("required"),
    employee_type: yup.string().required("required"),
    /*hourly_wage: yup.number().when('employee_type', {
        is: 'Hourly',
        then: yup.number()
            .required("Hourly wage is required")
            .positive("Hourly wage must be a positive number")
            .typeError("Hourly wage must be a number"),
        otherwise: yup.number().nullable(),
    }),
    salary: yup.number().when('employee_type', {
        is: 'Salary',
        then: yup.number()
            .required("Salary is required")
            .positive("Salary must be a positive number")
            .typeError("Salary must be a number"),
        otherwise: yup.number().nullable(),
    }),*/
    hourly_wage: yup.number().nullable(),
    salary: yup.number().nullable(),
    job_function: yup.string().required("Job function is required"),
    gender: yup.string(),

});









const EmployeeForm = ({isOpen}) => {
    const isNonMobile = useMediaQuery("(min-width:600px)");
    const navigate = useNavigate();

    

    const handleFormSubmit = async (values) => {
        // Create a request body that matches the expected API schema
        const requestBody = {
            employee_id: '1125', // Generate or fetch a unique ID if necessary
            ssn: values.ssn,
            first_name: values.first_name,
            last_name: values.last_name,
            middle_initial: values.middle_initial,
            phone_number: values.phone_number,
            email: values.email,
            address_line1: values.address_line1,
            address_line2: values.address_line2 || " ", 
            city: values.city,
            state: values.state,
            zip_code: values.zip_code,
            country: values.country,
            dob: values.dob, // Ensure this is in 'YYYY-MM-DD' format
            start_date: values.start_date || new Date().toISOString().split('T')[0], // Default to today if not provided
            employee_type: values.employee_type,
            hourly_wage: values.employee_type === 'Hourly' ? parseFloat(values.hourly_wage.replace(/[^0-9.-]+/g, "")) || 0 : 0, // Ensure it's a number
            salary: values.employee_type === 'Salary' ? parseFloat(values.salary.replace(/[^0-9.-]+/g, "")) || 0 : 0, // Ensure it's a number
            job_function: values.job_function,
            gender: values.gender,
            
        };
        console.log(requestBody); 


    
        // Check for any missing or incorrect values
        const missingFields = [];
        Object.entries(requestBody).forEach(([key, value]) => {
            if (value === '' || value === undefined) {
                missingFields.push(key);
            }
        });
    
        if (missingFields.length > 0) {
            console.error('Missing fields:', missingFields);
            alert(`Please fill in the following fields: ${missingFields.join(', ')}`);
            return; // Stop submission if there are missing fields
        }
    
        try {
            const response = await axios.post('https://theme-park-backend.ambitioussea-02dd25ab.eastus.azurecontainerapps.io/api/v1/employees/', requestBody);
            console.log(Date().toISOString().split('T')[0]); 
            console.log('Response data:', response.data); // Handle the response as needed
            navigate('/employees'); // Navigate after successful submission
        } catch (error) {
            console.error('Error submitting form:', error); // Handle the error appropriately
            if (error.response) {
                console.error('Response data:', error.response.data); // Log the response data
                alert('Submission failed. Please check the console for more details.'); // Notify user
            }
        }
    };

    return (
		<Box
			m="20px"
			ml={isOpen ? "250px" : "80px"} // Adjust left margin based on isOpen
			transition="margin 0.3s ease" // Smooth transition for margin
		>
			<IconButton onClick={() => navigate("/employees")}>
				<ArrowBackIcon sx={{ fontSize: "30px", color: "grey" }} />
			</IconButton>

			<Header
				title="ADD NEW EMPLOYEE"
				subtitle="Add a profile for a NEW employee"
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
								label="First Name"
								onBlur={handleBlur}
								onChange={handleChange}
								value={values.first_name}
								name="first_name"
								error={
									!!touched.first_name && !!errors.first_name
								}
								helperText={
									touched.first_name && errors.first_name
								}
								sx={{
									gridColumn: "span 1",
								}}
							/>
							<TextField
								fullWidth
								variant="filled"
								type="text"
								label="Middle Initial"
								inputProps={{ maxLength: 1 }}
								onBlur={handleBlur}
								onChange={handleChange}
								value={values.middle_initial}
								name="middle_initial"
								error={
									!!touched.middle_initial &&
									!!errors.middle_initial
								}
								helperText={
									touched.middle_initial &&
									errors.dmiddle_initialb
								}
								sx={{
									gridColumn: "span 1",
								}}
							/>
							<TextField
								fullWidth
								variant="filled"
								type="text"
								label="Last Name"
								onBlur={handleBlur}
								onChange={handleChange}
								value={values.last_name}
								name="last_name"
								error={
									!!touched.last_name && !!errors.last_name
								}
								helperText={
									touched.last_name && errors.last_name
								}
								sx={{
									gridColumn: "span 1",
								}}
							/>

							<FormControl
								fullWidth
								variant="filled"
								sx={{ gridColumn: "span 1" }}
							>
								<InputLabel>Title</InputLabel>
								<Select
									name="title"
									value={values.title}
									onChange={handleChange}
									onBlur={handleBlur}
									error={!!touched.title && !!errors.title}
								>
									<MenuItem value="">None</MenuItem>{" "}
									{/* Option for no title */}
									<MenuItem value="Mr.">Mr.</MenuItem>
									<MenuItem value="Mrs.">Mrs.</MenuItem>
									<MenuItem value="Ms.">Ms.</MenuItem>
									<MenuItem value="Dr.">Dr.</MenuItem>
									<MenuItem value="Prof.">Prof.</MenuItem>
									<MenuItem value="Mx.">Mx.</MenuItem>
								</Select>
								{touched.title && errors.title && (
									<div
										style={{
											color: "red",
											fontSize: "12px",
										}}
									>
										{errors.title}
									</div>
								)}
							</FormControl>

							<TextField
								fullWidth
								variant="filled"
								type="text"
								label="Social Security Number"
								inputProps={{ maxLength: 11 }}
								onBlur={handleBlur}
								onChange={(e) => {
									const formattedValue = formatSSN(
										e.target.value
									);
									handleChange({
										target: {
											name: "ssn",
											value: formattedValue,
										},
									});
								}}
								value={values.ssn}
								name="ssn"
								error={!!touched.ssn && !!errors.ssn}
								helperText={touched.ssn && errors.ssn}
								sx={{
									gridColumn: "span 2",
								}}
							/>

							<BasicDateTimePicker label="Date of Birth" />

							<TextField
								fullWidth
								variant="filled"
								type="text"
								label="Data of Birth"
								inputProps={{ maxLength: 10 }} // Format like MM/DD/YYYY
								onBlur={handleBlur}
								onChange={(e) => {
									const formattedValue = formatDate(
										e.target.value
									);
									handleChange({
										target: {
											name: "dob",
											value: formattedValue,
										},
									});
								}}
								value={values.dob}
								name="dob"
								error={!!touched.dob && !!errors.dob}
								helperText={touched.dob && errors.dob}
								sx={{
									gridColumn: "span 1",
								}}
							/>

							<FormControl
								fullWidth
								variant="filled"
								sx={{ gridColumn: "span 1" }}
							>
								<InputLabel>Gender</InputLabel>
								<Select
									name="gender"
									value={values.gender}
									onChange={handleChange}
									onBlur={handleBlur}
									error={!!touched.gender && !!errors.gender}
								>
									<MenuItem value="M">Male</MenuItem>
									<MenuItem value="F">Female</MenuItem>
									<MenuItem value="N">Non-binary</MenuItem>
								</Select>
								{touched.gender && errors.gender && (
									<div
										style={{
											color: "red",
											fontSize: "12px",
										}}
									>
										{errors.gender}
									</div>
								)}
							</FormControl>

							{/*Emmployee Type selection + user auth passage ?? */}
							<FormControl
								fullWidth
								variant="filled"
								sx={{ gridColumn: "span 1" }}
							>
								<InputLabel>Employee Type</InputLabel>
								<Select
									name="employee_type"
									value={values.employee_type}
									onChange={handleChange}
									onBlur={handleBlur}
									error={
										!!touched.employee_type &&
										!!errors.employee_type
									}
								>
									<MenuItem value="Hourly">Hourly</MenuItem>
									<MenuItem value="Salary">Salary</MenuItem>
								</Select>
								{touched.employee_type &&
									errors.employee_type && (
										<div
											style={{
												color: "red",
												fontSize: "12px",
											}}
										>
											{errors.employee_type}
										</div>
									)}
							</FormControl>

							{/* Payment field managemenet, depending on dropdown (if) selection*/}
							{values.employee_type === "" && (
								<Box
									sx={{
										gridColumn: "span 1",
										height: "56px",
									}}
								/>
							)}
							{values.employee_type === "Hourly" && (
								<TextField
									fullWidth
									variant="filled"
									type="text"
									label="Hourly Wage"
									onBlur={handleBlur}
									onChange={(e) => {
										const inputValue = e.target.value;
										// Allow the user to type while starting from 0.00
										handleChange({
											target: {
												name: "hourly_wage",
												value: inputValue,
											},
										});
									}}
									value={formatHourlyWage(values.hourly_wage)}
									name="hourly_wage"
									error={
										!!touched.hourly_wage &&
										!!errors.hourly_wage
									}
									helperText={
										touched.hourly_wage &&
										errors.hourly_wage
									}
									sx={{ gridColumn: "span 1" }}
								/>
							)}

							{values.employee_type === "Salary" && (
								<TextField
									fullWidth
									variant="filled"
									type="text"
									label="Salary"
									onBlur={handleBlur}
									onChange={(e) => {
										const inputValue = e.target.value;
										handleChange({
											target: {
												name: "salary",
												value: inputValue,
											},
										});
									}}
									value={formatSalary(values.salary)}
									name="salary"
									error={!!touched.salary && !!errors.salary}
									helperText={touched.salary && errors.salary}
									sx={{ gridColumn: "span 1" }}
								/>
							)}
							<TextField
								fullWidth
								variant="filled"
								type="text"
								label="Job Function"
								onBlur={handleBlur}
								onChange={handleChange}
								value={values.job_function}
								name="job_function"
								error={
									!!touched.job_function &&
									!!errors.job_function
								}
								helperText={
									touched.job_function && errors.job_function
								}
								sx={{
									gridColumn: "span 2",
								}}
							/>
							<TextField
								fullWidth
								variant="filled"
								type="text"
								label="Phone Number"
								inputProps={{ maxLength: 12 }}
								onBlur={handleBlur}
								onChange={(e) => {
									const formattedValue = formatPhoneNumber(
										e.target.value
									);
									handleChange({
										target: {
											name: "phone_number",
											value: formattedValue,
										},
									});
								}}
								value={values.phone_number}
								name="phone_number"
								error={
									!!touched.phone_number &&
									!!errors.phone_number
								}
								helperText={
									touched.phone_number && errors.phone_number
								}
								sx={{
									gridColumn: "span 1",
								}}
							/>
							<TextField
								fullWidth
								variant="filled"
								type="text"
								label="Email"
								onBlur={handleBlur}
								onChange={handleChange}
								value={values.email}
								name="email"
								error={!!touched.email && !!errors.email}
								helperText={touched.email && errors.email}
								sx={{
									gridColumn: "span 3",
								}}
							/>

							<TextField
								fullWidth
								variant="filled"
								type="text"
								label="Adress 1"
								onBlur={handleBlur}
								onChange={handleChange}
								value={values.address_line1}
								name="address_line1"
								error={
									!!touched.address_line1 &&
									!!errors.address_line1
								}
								helperText={
									touched.address_line1 &&
									errors.address_line1
								}
								sx={{
									gridColumn: "span 3",
								}}
							/>
							<TextField
								fullWidth
								variant="filled"
								type="text"
								label="Adress 2"
								onBlur={handleBlur}
								onChange={handleChange}
								value={values.address_line2}
								name="address_line2"
								error={
									!!touched.address_line2 &&
									!!errors.address_line2
								}
								helperText={
									touched.address_line2 &&
									errors.address_line2
								}
								sx={{
									gridColumn: "span 1",
								}}
							/>
							<TextField
								fullWidth
								variant="filled"
								type="text"
								label="City"
								onBlur={handleBlur}
								onChange={handleChange}
								value={values.city}
								name="city"
								error={!!touched.city && !!errors.city}
								helperText={touched.city && errors.city}
								sx={{
									gridColumn: "span 1",
								}}
							/>
							<TextField
								fullWidth
								variant="filled"
								type="text"
								label="State"
								onBlur={handleBlur}
								onChange={handleChange}
								value={values.state}
								name="state"
								error={!!touched.state && !!errors.state}
								helperText={touched.state && errors.state}
								sx={{
									gridColumn: "span 1",
								}}
							/>
							<TextField
								fullWidth
								variant="filled"
								type="text"
								label="Country"
								onBlur={handleBlur}
								onChange={handleChange}
								value={values.country}
								name="country"
								error={!!touched.country && !!errors.country}
								helperText={touched.country && errors.country}
								sx={{
									gridColumn: "span 1",
								}}
							/>
							<TextField
								fullWidth
								variant="filled"
								type="text"
								label="Zip Code"
								inputProps={{ maxLength: 5 }}
								onBlur={handleBlur}
								onChange={handleChange}
								value={values.zip_code}
								name="zip_code"
								error={!!touched.zip_code && !!errors.zip_code}
								helperText={touched.zip_code && errors.zip_code}
								sx={{
									gridColumn: "span 1",
								}}
							/>
						</Box>
						<Box display="flex" justifyContent="end" mt="20px">
							<Button
								type="submit"
								color="secondary"
								variant="contained"
							>
								Create Employee Profile
							</Button>
						</Box>
					</form>
				)}
			</Formik>
		</Box>
	);
}

export default EmployeeForm;
