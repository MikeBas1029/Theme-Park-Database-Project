import { Box, useTheme, IconButton} from "@mui/material";
import { DataGrid, GridToolbar } from "@mui/x-data-grid";
import { tokens } from "../../../theme";
import  Header from "../../../components/Header"
import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import axios from "axios";
import DownloadButton from "../../../components/DownloadButton";
import PrintButton from "../../../components/PrintButton";
import AddButton from "../../../components/AddButton";

const InvoiceReports = () => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);
    const navigate = useNavigate();

    const [customers, setCustomers] = useState([]); // State for storing customers data
    const [loading, setLoading] = useState(true); // State for loading indicator


    const columns = [
        { field: "invoice_id", headerName: "Invoice ID", flex: 0.5 },
        { field: "company_name", headerName: "Company Name", flex: 1, cellClassName: "name-column--cell" },
        { field: "supply", headerName: "Supply", flex: 1 }, 
        { field: "amount_due", headerName: "Balance Due", flex: 1, cellClassName: "name-column--cell"},
        { field: "payment_status", headerName: "Payment Status", flex: 1 },
        ]; {/*field: value/data grabbed from  colName: column title in table */}


        // Fetch customers from the backend
    useEffect(() => {
        const fetchCustomers = async () => {
            try {
                const response = await axios.get("https://theme-park-backend.ambitioussea-02dd25ab.eastus.azurecontainerapps.io/api/v1/reports/invoice-status")
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
                <Header title="Invoice Report" subtitle="View you invoice statuses"/>
                    <Box display="flex" alignItems="center">
                        <PrintButton apiUrl="https://theme-park-backend.ambitioussea-02dd25ab.eastus.azurecontainerapps.io/api/v1/reports/invoice-status
" columns={columns} />
                        <DownloadButton
                            apiUrl="https://theme-park-backend.ambitioussea-02dd25ab.eastus.azurecontainerapps.io/api/v1/reports/invoice-status
"
                            fileName="customers_report.csv"
                            columns={columns}
                            />
                        <AddButton navigateTo={'/customerform'} />
                    </Box>
            </Box>

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
            getRowId={(row) => row.invoice_id}/>
                )}
            </Box>
        </Box>
    );
}

export default InvoiceReports;



