import { Box, useTheme, IconButton} from "@mui/material";
import { DataGrid, GridToolbar } from "@mui/x-data-grid";
import { tokens } from "../../theme";
import {sampleDataRoster} from "../../data/sampleData"
import  AdminPanelSettingsOutlinedIcon from "@mui/icons-material/AdminPanelSettingsOutlined";
import  LockOpenOutlinedIcon  from "@mui/icons-material/LockOpenOutlined";
import  SecurityOutlinedIcon  from "@mui/icons-material/SecurityOutlined";
import  Header from "../../components/Header"
import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import axios from "axios";
import DownloadButton from "../../components/DownloadButton";
import PrintButton from "../../components/PrintButton";
import AddButton from "../../components/AddButton";

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
        { field: "email", headerName: "Email", flex: 1 },
        { field: "phone_number", headerName: "Phone Number", flex: 1 },
        { field: "address_line1", headerName: "Address Line 1" },
        { field: "address_line2", headerName: "Address Line 2" },
        { field: "city", headerName: "City" },
        { field: "state", headerName: "State" },
        { field: "zip_code", headerName: "Zip Code" },
        { field: "country", headerName: "Country" },
        { field: "date_of_birth", headerName: "Date of Birth" },
        { field: "membership_type", headerName: "Membership Type" },
        { field: "registration_date", headerName: "Registration Date" },
        { field: "renewal_date", headerName: "Renewal Date" },
        ]; {/*field: value/data grabbed from  colName: column title in table */}


        // Fetch customers from the backend
    useEffect(() => {
        const fetchCustomers = async () => {
            try {
                const response = await axios.get("https://theme-park-backend.ambitioussea-02dd25ab.eastus.azurecontainerapps.io/api/v1/customers/");
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
            {/* Print | Export | Add  */}
            <Box display="flex" justifyContent="space-between" alignItems="center">
                <Header title="Customers✅" subtitle="View registered member information(?) *@team, wb no registered customers who just buy ticket*"/>
                    <Box display="flex" alignItems="center">
                        <PrintButton apiUrl="https://theme-park-backend.ambitioussea-02dd25ab.eastus.azurecontainerapps.io/api/v1/customers/" columns={columns} />
                        <DownloadButton
                            apiUrl="https://theme-park-backend.ambitioussea-02dd25ab.eastus.azurecontainerapps.io/api/v1/customers/"
                            fileName="customers_report.csv"
                            columns={columns}
                            />
                        <AddButton navigateTo={'/customerform'} />
                    </Box>
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



