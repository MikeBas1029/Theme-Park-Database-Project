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


const Inventory = () => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);
    const navigate = useNavigate();
    const [rows, setRows] = useState([]);

    const columns = [
        {field: "id", headerName: "ID", flex: 0.2},
        {field: "name", headerName: "Name", flex: 1, cellClassName: "name-column--cell"},
        {field: "status", headerName: "Status", flex: .3},
        {field: "category", headerName: "Category", flex: 1},
        {field: "price", headerName: "Price", type: "number", headerAlign: "left", align: "left"},
        {field: "cost", headerName: "Unit Cost", type: "number", headerAlign: "left", align: "left"}

    ]; {/*field: value/data grabbed from  colName: column title in table */}

    //Fetching data from FastAPI(back-end)
    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await axios.get('http://127.0.0.1:8000/items');
                console.log(response.data); //log the response data
                setRows(response.data);
            } catch (error) {
                console.error("Error fetching data:", error);
            }
        };
        fetchData();
    }, []); // Empty dependency array to run once on component mount

    return(


        <Box m="20px">
            <Header title="Shops & Inventory" subtitle="Manage Inventory"/>

            {/*Employee creation form button + linking */}
            <Box display="flex" justifyContent="flex-end" mb="20px">
                <IconButton onClick={() => navigate("/inventoryform")}>
                    <AddCircleOutlineIcon sx={{ fontSize: "30px", color: colors.greenAccent[600] }} />
                </IconButton>
            </Box>

            {/*To display inventory*/}
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

                <DataGrid rows={rows} columns={columns} components={{Toolbar: GridToolbar}}/>
            </Box>


        </Box>
    );
}

export default Inventory;



