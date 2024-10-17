import { Box, Button, TextField } from "@mui/material";
import { Formik } from "formik";
import * as yup from "yup";
import useMediaQuery from "@mui/material";
import Header from "../components/Header";

const initialValues = {
    firstName: "",
    middleInitial: "",
    lastName: "",
    email: "",
    phone: "",
    addres1: "",
    address2: "", 
    DOB: "",
};

const phoneRegExp =
  /^((\+[1-9]{1,4}[ -]?)|(\([0-9]{2,3}\)[ -]?)|([0-9]{2,4})[ -]?)*?[0-9]{3,4}[ -]?[0-9]{3,4}$/; {/*highly comprehensive regExp (?) works for international nums */}


const userSchema = yup.object().shape({
    firstName: yup.string().required("required"),
    lastName: yup.string().required("required"),
    email: yup.string().email("Invalid email").required("required"),
    phone: yup.string().matches(phoneRegExp,"Phone number is not valid").required("required"),
    addres1: yup.string().required("required"),
    address2: yup.string().required(),

})





const Form = () => {
    const isNonMobile = useMediaQuery("(min-width:600px)")

    const handleFormSubmit = (values) => {
        console.log(values) /*FORM IS ONLY CONSOLE LOGGING */
    }
    return
    
    <Box  m="20px">
        <Header title="ADD NEW EMPLOYEE PROFILE" subtitle="Add a profile for a NEW employee" />
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
                        value={values.firstName}
                        name="firstName"
                        error={!!touched.firstName && !!errors.firstName}
                        helperText={touched.firstName && errors.firstName}
                        sx={{
                            gridColumn: "span 2"
                        }}/>
                        <TextField 
                        fullWidth
                        variant="filled"
                        type="text"
                        label="Last Name"
                        onBlur={handleBlur}
                        onChange={handleChange}
                        value={values.lastName}
                        name="laststName"
                        error={!!touched.lastName && !!errors.lastName}
                        helperText={touched.lastName && errors.lastName}
                        sx={{
                            gridColumn: "span 2"
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
                            gridColumn: "span 4"
                        }}/>
                        <TextField 
                        fullWidth
                        variant="filled"
                        type="text"
                        label="Phone Number"
                        onBlur={handleBlur}
                        onChange={handleChange}
                        value={values.phone}
                        name="phone"
                        error={!!touched.phone && !!errors.phone}
                        helperText={touched.phone && errors.phone}
                        sx={{
                            gridColumn: "span 4"
                        }}/>
                        <TextField 
                        fullWidth
                        variant="filled"
                        type="text"
                        label="Adress 1"
                        onBlur={handleBlur}
                        onChange={handleChange}
                        value={values.addres1}
                        name="addres1"
                        error={!!touched.addres1 && !!errors.addres1}
                        helperText={touched.addres1 && errors.addres1}
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
                        value={values.address2}
                        name="address2"
                        error={!!touched.address2 && !!errors.address2}
                        helperText={touched.address2 && errors.address2}
                        sx={{
                            gridColumn: "span 4"
                        }}/>

                    </Box>
                </form>
            )}
        </Formik>
    </Box>
}

export default Form;
