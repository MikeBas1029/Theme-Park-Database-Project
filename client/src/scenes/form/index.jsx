import {Box, Button, IconButton, TextField} from "@mui/material";
import { Formik } from "formik";
import * as yup from "yup";
import useMediaQuery from "@mui/material/useMediaQuery";
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import Header from "../../components/Header";
import { useNavigate } from 'react-router-dom';

const initialValues = {
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
};


const phoneRegExp =
  /^((\+[1-9]{1,4}[ -]?)|(\([0-9]{2,3}\)[ -]?)|([0-9]{2,4})[ -]?)*?[0-9]{3,4}[ -]?[0-9]{3,4}$/; {/*highly comprehensive regExp (?) works for international nums */}




const userSchema = yup.object().shape({
    ssn: yup.string().required("required"),
    first_name: yup.string().required("required"),
    middle_initial: yup.string(),
    last_name: yup.string().required("required"),
    email: yup.string().email("Invalid email").required("required"),
    phone_number: yup.string().matches(phoneRegExp, "Phone number is not valid").required("required"),
    address_line1: yup.string().required("required"),
    address_line2: yup.string(),
    dob: yup.string().required("required"),
});





const Form = () => {
    const isNonMobile = useMediaQuery("(min-width:600px)");
    const navigate = useNavigate();

    const handleFormSubmit = (values) => {
        console.log(values) /*FORM IS ONLY CONSOLE LOGGING */
    }

    return(
    
    <Box  m="20px">
        <IconButton onClick={() => navigate('/employees')}>
            <ArrowBackIcon sx={{ fontSize: "30px", color: "grey" }} />
        </IconButton>

        <Header title="ADD NEW EMPLOYEE" subtitle="Add a profile for a NEW employee" />
        <Formik 
        onSubmit={handleFormSubmit}
        initialValues={initialValues}
        validationSchema={userSchema}>
            {({values, errors, touched, handleBlur, handleChange, handleSubmit}) => (
                <form onSubmit={handleSubmit}>
                    <Box display="grid" gap="30px" gridTemplateColumns="repeat(4, minmax(0, 1fr))"
                    sx={{
                        "& > div": {gridColumn: isNonMobile ? undefined: "span 4"},  
                    }}>
                        <TextField 
                        fullWidth
                        variant="filled"
                        type="text"
                        label="First Name"
                        onBlur={handleBlur}
                        onChange={handleChange}
                        value={values.first_name}
                        name="first_name"
                        error={!!touched.first_name && !!errors.first_name}
                        helperText={touched.first_name && errors.first_name}
                        sx={{
                            gridColumn: "span 1"
                        }}/>
                        <TextField 
                        fullWidth
                        variant="filled"
                        type="text"
                        label="Middle Initial"
                        onBlur={handleBlur}
                        onChange={handleChange}
                        value={values.middle_initial}
                        name="middle_initial"
                        error={!!touched.middle_initial && !!errors.middle_initial}
                        helperText={touched.middle_initial && errors.dmiddle_initialb}
                        sx={{
                            gridColumn: "span 1"
                        }}/>
                        <TextField 
                        fullWidth
                        variant="filled"
                        type="text"
                        label="Last Name"
                        onBlur={handleBlur}
                        onChange={handleChange}
                        value={values.last_name}
                        name="last_name"
                        error={!!touched.last_name && !!errors.last_name}
                        helperText={touched.last_name && errors.last_name}
                        sx={{
                            gridColumn: "span 1"
                        }}/>
                        <TextField 
                        fullWidth
                        variant="filled"
                        type="text"
                        label="Title"
                        onBlur={handleBlur}
                        onChange={handleChange}
                        value={values.last_name}
                        name="last_name"
                        error={!!touched.last_name && !!errors.last_name}
                        helperText={touched.last_name && errors.last_name}
                        sx={{
                            gridColumn: "span 1"
                        }}/>
                        <TextField 
                        fullWidth
                        variant="filled"
                        type="text"
                        label="Social Security Number"
                        onBlur={handleBlur}
                        onChange={handleChange}
                        value={values.email}
                        name="ssn"
                        error={!!touched.ssn && !!errors.ssn}
                        helperText={touched.ssn && errors.ssn}
                        sx={{
                            gridColumn: "span 2"
                        }}/>   
                         <TextField 
                        fullWidth
                        variant="filled"
                        type="text"
                        label="Data of Birth"
                        onBlur={handleBlur}
                        onChange={handleChange}
                        value={values.dob}
                        name="dob"
                        error={!!touched.dob && !!errors.dob}
                        helperText={touched.dob && errors.dob}
                        sx={{
                            gridColumn: "span 1"
                        }}/>
                        <TextField 
                        fullWidth
                        variant="filled"
                        type="text"
                        label="Gender"
                        onBlur={handleBlur}
                        onChange={handleChange}
                        value={values.dob}
                        name="dob"
                        error={!!touched.dob && !!errors.dob}
                        helperText={touched.dob && errors.dob}
                        sx={{
                            gridColumn: "span 1"
                        }}/>
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
                            gridColumn: "span 2"
                        }}/>       

                        <TextField 
                        fullWidth
                        variant="filled"
                        type="text"
                        label="Phone Number"
                        onBlur={handleBlur}
                        onChange={handleChange}
                        value={values.phone_number}
                        name="phone_number"
                        error={!!touched.phone_number && !!errors.phone_number}
                        helperText={touched.phone_number && errors.phone_number}
                        sx={{
                            gridColumn: "span 2"
                        }}/>   
                        <TextField 
                        fullWidth
                        variant="filled"
                        type="text"
                        label="Adress 1"
                        onBlur={handleBlur}
                        onChange={handleChange}
                        value={values.address_line1}
                        name="address_line1"
                        error={!!touched.address_line1 && !!errors.address_line1}
                        helperText={touched.address_line1 && errors.address_line1}
                        sx={{
                            gridColumn: "span 4"
                        }}/>
                        <TextField 
                        fullWidth
                        variant="filled"
                        type="text"
                        label="Adress 2"
                        onBlur={handleBlur}
                        onChange={handleChange}
                        value={values.address_line2}
                        name="address_line2"
                        error={!!touched.address_line2 && !!errors.address_line2}
                        helperText={touched.address_line2 && errors.address_line2}
                        sx={{
                            gridColumn: "span 4"
                        }}/>
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
                            gridColumn: "span 1"
                        }}/>
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
                            gridColumn: "span 1"
                        }}/>
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
                            gridColumn: "span 1"
                        }}/>
                        <TextField 
                        fullWidth
                        variant="filled"
                        type="text"
                        label="Zip Code"
                        onBlur={handleBlur}
                        onChange={handleChange}
                        value={values.state}
                        name="zip_code"
                        error={!!touched.zip_code && !!errors.zip_code}
                        helperText={touched.zip_code && errors.zip_code}
                        sx={{
                            gridColumn: "span 1"
                        }}/>

                    </Box>
                    <Box display="flex" justifyContent="end" mt="20px">
                        <Button type="submit" color="secondary" variant="contained">
                            Create Employee Profile
                        </Button>
                    </Box>
                </form>
            )}
        </Formik>
    </Box>
    )
}

export default Form;
