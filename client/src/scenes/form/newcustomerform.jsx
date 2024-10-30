import { Box, Button, TextField, Select, MenuItem, FormControl, InputLabel, IconButton } from "@mui/material";
import { Formik } from "formik";
import * as yup from "yup";
import useMediaQuery from "@mui/material/useMediaQuery";
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import Header from "../../components/Header";
import { useNavigate } from 'react-router-dom';
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

})




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


const NewCustForm = () => {
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
            const response = await axios.post('https://theme-park-backend.ambitioussea-02dd25ab.eastus.azurecontainerapps.io/api/v1/items/', requestBody);
            console.log(response.data); // Handle the response as needed
            navigate('/'); // Navigate after successful submission
        } catch (error) {
            console.error('Error submitting form:', error); // Handle the error appropriately
            if (error.response) {
                console.error('Response data:', error.response.data); // Log the response data
                alert('Submission failed. Please check the console for more details.'); // Notify user
            }
        }
    };

    return(
    
    <Box  m="20px">
        <IconButton onClick={() => navigate(-1)}>
            <ArrowBackIcon sx={{ fontSize: "30px", color: "grey" }} />
        </IconButton>

        <Header title="Finish Creating your Profile" subtitle="Add remaining profile details to complete your account" />
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
                        label="Phone Number"
                        onBlur={handleBlur}
                        onChange={handleChange}
                        value={values.vendor_id}
                        name="vendor_id"
                        error={!!touched.vendor_id && !!errors.vendor_id}
                        helperText={touched.vendor_id && errors.vendor_id}
                        sx={{
                            gridColumn: "span 2"
                        }}/>


                        
                        <TextField 
                        fullWidth
                        variant="filled"
                        type="text"
                        label="Data of Birth"
                        inputProps={{ maxLength: 10 }} // Format like MM/DD/YYYY
                        onBlur={handleBlur}
                        onChange={(e) => {
                            const formattedValue = formatDate(e.target.value);
                            handleChange({ target: { name: 'dob', value: formattedValue } });
                        }}
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
                        label="Adress 1"
                        onBlur={handleBlur}
                        onChange={handleChange}
                        value={values.address_line1}
                        name="address_line1"
                        error={!!touched.address_line1 && !!errors.address_line1}
                        helperText={touched.address_line1 && errors.address_line1}
                        sx={{
                            gridColumn: "span 3"
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
                            gridColumn: "span 1"
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
                        inputProps={{ maxLength: 5 }}
                        onBlur={handleBlur}
                        onChange={handleChange}
                        value={values.zip_code}
                        name="zip_code"
                        error={!!touched.zip_code && !!errors.zip_code}
                        helperText={touched.zip_code && errors.zip_code}
                        sx={{
                            gridColumn: "span 1"
                        }}/>
                    </Box>

                    <Box display="flex" justifyContent="end" mt="20px">
                        <Button type="submit" color="secondary" variant="contained">
                            Finish Creating Profile
                        </Button>
                    </Box>
                </form>
            )}
        </Formik>
    </Box>
    )
}

export default NewCustForm;
