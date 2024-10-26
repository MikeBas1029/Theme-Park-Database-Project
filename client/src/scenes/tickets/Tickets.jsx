import { Box, Typography, useTheme, IconButton } from "@mui/material";
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

const Tickets = () => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);
    const navigate = useNavigate();


    const [visitData, setvisitData] = useState([]); {/*State for storing employee data*/}
    const [loading, setLoading] = useState(true); // Loading state


    {/*Fetch item data */}
    useEffect(() => {
        const fetchvisitData = async () => {
            try {
                const response = await axios.get("http://127.0.0.1:8000/api/v1/tickets/");
                console.log("Fetched tickets:", response.data);
                setvisitData(response.data);
            } catch (error) {
                console.error("Error fetching tickets:", error);
            } finally {
                setLoading(false);
            }
        };
    
        fetchvisitData();
        }, []);

        const columns = [
            {field: "ticket_id", headerName: "Visit ID", headerAlign: "center", align: "center", flex: 0.2},
            {field: "customer_id", headerName: "Customer ID", headerAlign: "center", align: "center", flex: 0.2},
            {field: "ticket_type", headerName: "Ticket Type", headerAlign: "center", align: "center", flex: 0.2},
            {field: "purchase_date", headerName: "Purchase Date", headerAlign: "left", align: "left", flex: 0.2},
            {field: "start_date", headerName: "Start Date", headerAlign: "left", align: "left", flex: 0.2},
            {field: "expiration_date", headerName: "Expiration Date", headerAlign: "left", align: "left", flex: 0.2},
            {field: "discount", headerName: "Discount", headerAlign: "left", align: "left", flex: 0.2},
            {field: "price", headerName: "Price", headerAlign: "left", align: "left", flex: 0.2},
            {field: "special_access", headerName: "Special Access", headerAlign: "left", align: "left", flex: 0.2},
            {field: "status", headerName: "Status", headerAlign: "left", align: "left", flex: 0.2},
        ];
        
        {/*field: value/data grabbed from  colName: column title in table */}

    return(


        <Box m="20px"> 
                <Header title="Tickets✅" subtitle="View details related to customer tickets"/>
                <PrintButton
                apiUrl="http://127.0.0.1:8000/api/v1/tickets/" 
                columns={columns} />
            <DownloadButton 
                 apiUrl="http://127.0.0.1:8000/api/v1/tickets/" 
                fileName="tickets_report.csv" 
                columns={columns} 
                />
            <AddButton /> 
              <Box display="flex" justifyContent="space-between" alignItems="center">

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
            rows={visitData} 
            columns={columns} 
            components={{Toolbar: GridToolbar}}
            getRowId={(row) => row.ticket_id}/>
            </Box>


        </Box>
    );
}

export default Tickets;




