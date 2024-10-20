import { Box, useTheme, IconButton} from "@mui/material";
import { DataGrid, GridToolbar } from "@mui/x-data-grid";
import { tokens } from "../../theme";
import {sampleDataRoster} from "../../data/sampleData"
import  AdminPanelSettingsOutlinedIcon from "@mui/icons-material/AdminPanelSettingsOutlined";
import  LockOpenOutlinedIcon  from "@mui/icons-material/LockOpenOutlined";
import  SecurityOutlinedIcon  from "@mui/icons-material/SecurityOutlined";
import AddCircleOutlineIcon from "@mui/icons-material/AddCircleOutline"; // Import the plus icon
import  Header from "../../components/Header"
import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import axios from "axios";


const Customers = () => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);
    const navigate = useNavigate();

    const [customers, setCustomers] = useState([]); // State for storing customers data
    const [loading, setLoading] = useState(true); // State for loading indicator


    const columns = [
        { field: "customer_id", headerName: "CustomerID", flex: 0.5 },
        { field: "first_name", headerName: "First Name", flex: 1, cellClassName: "name-column--cell" },
        { field: "last_name", headerName: "Last Name", flex: 1, cellClassName: "name-column--cell" },
        { field: "phone_number", headerName: "Phone Number", flex: 1 },
        { field: "email", headerName: "Email", flex: 1 },
        ]; {/*field: value/data grabbed from  colName: column title in table */}


        // Fetch customers from the backend
    useEffect(() => {
        const fetchCustomers = async () => {
            try {
                const response = await axios.get("http://127.0.0.1:8000/api/v1/customers/");
                console.log("Fetched customers:", response.data);
                setCustomers(response.data);
            } catch (error) {
                console.error("Error fetching customers:", error);
            } finally {
                setLoading(false);
            }
        };

        fetchCustomers();
    }, []);


    return(

        <Box m="20px">
            <Header title="Customer" subtitle="View customers and track daily park history"/>

            {/*Employee creation form button + linking */}
            <Box display="flex" justifyContent="flex-end" mb="20px">
                <IconButton onClick={() => navigate("/form")}>
                <AddCircleOutlineIcon sx={{ fontSize: "30px", color: colors.greenAccent[600] }} />
                </IconButton>
            </Box>

            {/*Form fields, missing validation method linkings + user auth */}
            <Box
            m="40px 0 0 0"
            height="75vh"
            sx={{"& .MuiDataGrid-root": {
                border: "none"
                }, 
                "& .MuiDataGrid-cell": {
                borderBottom: "none"
                },
                "& .name-column--cell": {
                color: colors.greenAccent[300]
                },
                "& .MuiDataGrid-columnHeader": {
                backgroundColor: colors.blueAccent[700],
                borderBottom: "none"
                },
                "& .MuiDataGrid-virtualScroller": {
                backgroundColor: colors.primary[400]
                },
                "& .MuiDataGrid-footerContainer": {
                borderTop: "none",
                backgroundColor: colors.blueAccent[700]
                },
                "& .MuiDataGrid-toolbarContainer .MuiButton-text": {
                color: `${colors.greenAccent[100]} !important`,
                backgroundColor: colors.blueAccent[700]
                },
                }}>

                {loading ? (
                    <div>Loading...</div>
                ) : (
                    
            <DataGrid 
            rows={customers} 
            columns={columns} 
            components={{Toolbar: GridToolbar}}
            loading={loading} 
            getRowId={(row) => row.customer_id}/>
                )}
            </Box>
        </Box>
    );
}

export default Customers;



