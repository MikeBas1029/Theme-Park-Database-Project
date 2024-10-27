import { Box, useTheme, IconButton} from "@mui/material";
import { DataGrid, GridToolbar } from "@mui/x-data-grid";
import { tokens } from "../../theme";
import  AdminPanelSettingsOutlinedIcon from "@mui/icons-material/AdminPanelSettingsOutlined";
import  LockOpenOutlinedIcon  from "@mui/icons-material/LockOpenOutlined";
import  SecurityOutlinedIcon  from "@mui/icons-material/SecurityOutlined";
import AddCircleOutlineIcon from "@mui/icons-material/AddCircleOutline"; // Import the plus icon
import  Header from "../../components/Header"
import { useNavigate } from "react-router-dom";
import axios from 'axios';
import { useEffect, useState } from 'react';
import DownloadButton from "../../components/DownloadButton";
import AddButton from "../../components/AddButton";
import PrintButton from "../../components/PrintButton";


const Invoices = () => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);
    const navigate = useNavigate();


    const [invoiceData, setinvoiceData] = useState([]); {/*State for storing employee data*/}
    const [loading, setLoading] = useState(true); // Loading state


    {/*Fetch item data */}
    useEffect(() => {
        const fetchinvoiceData = async () => {
            try {
                const response = await axios.get("http://127.0.0.1:8000/api/v1/invoices/");
                console.log("Fetched invoices:", response.data);
                setinvoiceData(response.data);
            } catch (error) {
                console.error("Error fetching invoices:", error);
            } finally {
                setLoading(false);
            }
        };
    
        fetchinvoiceData();
        }, []);

    const columns = [
        {field: "invoice_id", headerName: "Invoice", headerAlign: "center" , align: "center", flex: 0.2},
        {field: "vendor_id", headerName: "Vendor ID", headerAlign: "center" , align: "center", flex: 0.5}, 
        {field: "po_number", headerName: "Policy Number ?", flex: 0.3},
        {field: "amount_due", headerName: "Amount Due", type: "number", headerAlign: "left", align: "left", flex: 0.2} ,
        {field: "issue_date", headerName: "Date Issued", type: "number", headerAlign: "left", align: "left", flex: 0.2},
        {field: "due_date", headerName: "Payment Due Date", flex: .3},
        {field: "payment_status", headerName: "Payment Status", flex: 0.2},

    ]; {/*field: value/data grabbed from  colName: column title in table */}

 

    return(


        <Box m="20px">
            <Box display="flex" justifyContent="space-between" alignItems="center">
                <Header title="Invoices💻" subtitle="Track & view vendor invoices"/>
                <Box display="flex" alignItems="center">
                    <PrintButton apiUrl="http://127.0.0.1:8000/api/v1/invoices/" columns={columns} />
                    <DownloadButton apiUrl="http://127.0.0.1:8000/api/v1/invoices/" fileName="invoices_report.csv" columns={columns} />
                    <AddButton />
                </Box>
            </Box>
            {/*To display inventory*/}
            <Box
                m="10px 0 0 0"
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

<DataGrid 
            rows={invoiceData} 
            columns={columns} 
            components={{Toolbar: GridToolbar}}
            getRowId={(row) => row.invoice_id}/>
            </Box>


        </Box>
    );
}

export default Invoices;



