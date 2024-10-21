import { Box, Button, TextField, Select, MenuItem, FormControl, InputLabel, IconButton } from "@mui/material";
import { Formik } from "formik";
import * as yup from "yup";
import useMediaQuery from "@mui/material/useMediaQuery";
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import Header from "../../components/Header";
import { useNavigate } from 'react-router-dom';

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
    const isNonMobile = useMediaQuery("(min-width:600px)");
    const navigate = useNavigate();

    const handleFormSubmit = (values) => {
        console.log(values) /*FORM IS ONLY CONSOLE LOGGING */
    }

    return(
    
    <Box  m="20px">
        <IconButton onClick={() => navigate(-1)}>
            <ArrowBackIcon sx={{ fontSize: "30px", color: "grey" }} />
        </IconButton>

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
                        name="itemID"
                        error={!!touched.itemID && !!errors.itemID}
                        helperText={touched.itemID && errors.itemID}
                        sx={{
                            gridColumn: "span 2"
                        }}/>

                        <TextField 
                        fullWidth
                        variant="filled"
                        type="text"
                        label="Vendor ID"
                        onBlur={handleBlur}
                        onChange={handleChange}
                        value={values.lastName}
                        name="vendorID"
                        error={!!touched.vendorID && !!errors.vendorID}
                        helperText={touched.vendorID && errors.vendorID}
                        sx={{
                            gridColumn: "span 2"
                        }}/>

                        <FormControl fullWidth variant="filled" sx={{ gridColumn: "span 2" }}>
                            <InputLabel id="category-label">Category</InputLabel>
                            <Select
                                labelId="category-label"
                                id="category"
                                name="category"
                                value={values.category}
                                onBlur={handleBlur}
                                onChange={handleChange}
                                error={!!touched.category && !!errors.category}
                            >
                                <MenuItem value="merchandise">Merchandise</MenuItem>
                                <MenuItem value="concessions">Concessions</MenuItem>
                                <MenuItem value="entertainment">Entertainment</MenuItem>
                            </Select>
                            {touched.category && errors.category && (
                                <div style={{ color: 'red' }}>{errors.category}</div>
                            )}
                        </FormControl>

                        <FormControl fullWidth variant="filled" sx={{ gridColumn: "span 2" }}>
                            <InputLabel id="status-label">Status</InputLabel>
                            <Select
                                labelId="status-label"
                                id="status"
                                name="Status"
                                value={values.status}
                                onBlur={handleBlur}
                                onChange={handleChange}
                                error={!!touched.status && !!errors.status}
                            >
                                <MenuItem value="active">Active</MenuItem>
                                <MenuItem value="discontiued">Discontinued</MenuItem>
                                <MenuItem value="backorder">Back Ordered</MenuItem>
                            </Select>
                            {touched.status && errors.status && (
                                <div style={{ color: 'red' }}>{errors.category}</div>
                            )}
                        </FormControl>

                        <TextField 
                        fullWidth
                        variant="filled"
                        type="text"
                        label="Price"
                        onBlur={handleBlur}
                        onChange={handleChange}
                        value={values.addres1}
                        name="price"
                        error={!!touched.price && !!errors.price}
                        helperText={touched.price && errors.price}
                        sx={{
                            gridColumn: "span 2"
                        }}/>

                        <TextField 
                        fullWidth
                        variant="filled"
                        type="text"
                        label="Unit Cost"
                        onBlur={handleBlur}
                        onChange={handleChange}
                        value={values.address2}
                        name="unitCost"
                        error={!!touched.unitCost && !!errors.unitCost}
                        helperText={touched.unitCost && errors.unitCost}
                        sx={{
                            gridColumn: "span 2"
                        }}/>
                    </Box>

                    <Box display="flex" justifyContent="end" mt="20px">
                        <Button type="submit" color="secondary" variant="contained">
                            Add item into Inventory
                        </Button>
                    </Box>
                </form>
            )}
        </Formik>
    </Box>
    )
}

export default Form;
