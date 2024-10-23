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


const Rides = () => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);
    const navigate = useNavigate();

    const [rides, setRides] = useState([]); // State for storing customers data
    const [loading, setLoading] = useState(true); // State for loading indicator

    const columns = [
        {field: "ride_id", headerName: "Ride ID", flex: 0.1},
        {field: "section_id", headerName: "Section ID", flex: 0.1},
        {field: "name", headerName: "Name", flex: 0.3, cellClassName: "name-column--cell"},
        {field: "ride_type", headerName: "Ride Type", flex: 0.1},
        {field: "last_inspected", headerName: "Last Inspected", flex: 0.1},
        {field: "height_requirement", headerName: "Height Req.", flex: 0.1},
        {field: "capacity", headerName: "Capacity", type: "number", align: "left"},
        {field: "status", headerName: "Status", flex: 0.1}
    ]; {/*field: value/data grabbed from  colName: column title in table */}


        // Fetch customers from the backend
        useEffect(() => {
            const fetchRides = async () => {
                try {
                    const response = await axios.get("http://127.0.0.1:8000/api/v1/rides/");
                    console.log("Fetched rides:", response.data);
                    setRides(response.data);
                } catch (error) {
                    console.error("Error fetching rides:", error);
                } finally {
                    setLoading(false);
                }
            };
    
            fetchRides();
        }, []);

    return(


        <Box m="20px">
              <Box display="flex" justifyContent="space-between" alignItems="center">
                <Header title="Rides💻" subtitle="View rides information and maintenance status"/>

                {/*Employee creation form button + linking */}
                <IconButton onClick={() => navigate("/inventoryform")}>
                    <AddCircleOutlineIcon sx={{ fontSize: "30px", color: colors.greenAccent[600] }} />
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
            rows={rides} 
            columns={columns} 
            components={{Toolbar: GridToolbar}}
            loading={loading} 
            getRowId={(row) => row.ride_id}/>
            </Box>


        </Box>
    );
}

export default Rides;



