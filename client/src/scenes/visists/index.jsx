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
import FileDownloadOutlinedIcon from '@mui/icons-material/FileDownloadOutlined';
import DownloadButton from "../../components/DownloadButton";

const Visits = () => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);
    const navigate = useNavigate();


    const [visitData, setvisitData] = useState([]); {/*State for storing employee data*/}
    const [loading, setLoading] = useState(true); // Loading state


    {/*Fetch item data */}
    useEffect(() => {
        const fetchvisitData = async () => {
            try {
                const response = await axios.get("http://127.0.0.1:8000/api/v1/visits/");
                console.log("Fetched visits:", response.data);
                setvisitData(response.data);
            } catch (error) {
                console.error("Error fetching visits:", error);
            } finally {
                setLoading(false);
            }
        };
    
        fetchvisitData();
        }, []);

    const columns = [
        {field: "visit_id", headerName: "Visit ID", headerAlign: "center" , align: "center", flex: 0.2},
        {field: "customer_id", headerName: "Customer ID", headerAlign: "center" , align: "center", flex: 0.2},
        {field: "visit_date", headerName: "Visit Date", headerAlign: "left", align: "left", flex: 0.2} ,
        {field: "visit_feedback", headerName: "Visit Feedback", headerAlign: "left", align: "left", flex: 0.2},
        {field: "visit_rating", headerName: "Visit Rating", flex: 0.2},

    ]; {/*field: value/data grabbed from  colName: column title in table */}

    return(


        <Box m="20px">
              <Box display="flex" justifyContent="space-between" alignItems="center">
              <Header title="Visits✅" subtitle="View details related to customer visits"/>
                {/*Employee creation form button + linking */}
                
                <DownloadButton 
                 apiUrl="http://127.0.0.1:8000/api/v1/visits/" 
                fileName="visits_report.csv"
                columns={columns} 
                />

                <IconButton onClick={() => navigate("/inventoryform")}>
                    <AddCircleOutlineIcon sx={{ fontSize: "30px", color: colors.greenAccent[600]}} />
                </IconButton>
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
            getRowId={(row) => row.visit_id}/>
            </Box>


        </Box>
    );
}

export default Visits;




