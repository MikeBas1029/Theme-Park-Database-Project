import { Box, Button, TextField } from "@mui/material";
import { Formik } from "formik";
import * as yup from "yup";
import useMediaQuery from "@mui/material/useMediaQuery";
import Header from "../../components/Header";

const initialValues = {
    itemID: "",
    itemName: "",
    vendorID: "",
    category: "",
    price: "",
    unitPrice: "",
};

const userSchema = yup.object().shape({
    itemID: yup.string().required("required"),
    itemName: yup.string().required("required"),
    vendorID: yup.string().required("required"),
    category: yup.string().required("required"),
    price: yup.string().required("required"),
    unitPrice: yup.string().required("required"),

})

const Form = () => {
    const isNonMobile = useMediaQuery("(min-width:600px)")

    const handleFormSubmit = (values) => {
        console.log(values) /*FORM IS ONLY CONSOLE LOGGING */
    }

    return(
    
    <Box  m="20px">
        <Header title="ADD NEW ITEM" subtitle="Add a new item into inventory" />
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
                        label="Item ID"
                        onBlur={handleBlur}
                        onChange={handleChange}
                        value={values.firstName}
                        name="Vendor ID"
                        error={!!touched.itemID && !!errors.itemID}
                        helperText={touched.itemID && errors.itemID}
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
                        name="lastName"
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
                            gridColumn: "span 3"
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
                            gridColumn: "span 2"
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
                            gridColumn: "span 3"
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
