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


    const [itemData, setitemData] = useState([]); {/*State for storing employee data*/}
    const [loading, setLoading] = useState(true); // Loading state


    {/*Fetch item data */}
    useEffect(() => {
        const fetchitemData = async () => {
            try {
                const response = await axios.get("http://127.0.0.1:8000/api/v1/items/");
                console.log("Fetched items:", response.data);
                setitemData(response.data);
            } catch (error) {
                console.error("Error fetching items:", error);
            } finally {
                setLoading(false);
            }
        };
    
        fetchitemData();
        }, []);

    const columns = [
        {field: "sku", headerName: "SKU", headerAlign: "center" , align: "center", flex: 0.2},
        {field: "name", headerName: "Item Name", headerAlign: "center" , align: "center", flex: 0.8}, 
        {field: "category", headerName: "Category", flex: 0.5},
        {field: "price", headerName: "Price", type: "number", headerAlign: "left", align: "left", flex: 0.2} ,
        {field: "cost", headerName: "Unit Cost", type: "number", headerAlign: "left", align: "left", flex: 0.2},
        {field: "status", headerName: "Status", flex: .3},
        {field: "vendor_id", headerName: "Vendor(ID)", flex: 0.2},

    ]; {/*field: value/data grabbed from  colName: column title in table */}

 

    return(


        <Box m="20px">
              <Box display="flex" justifyContent="space-between" alignItems="center">
                <Header title="Inventory" subtitle="Manage & view Inventory"/>

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
            rows={itemData} 
            columns={columns} 
            components={{Toolbar: GridToolbar}}
            getRowId={(row) => row.sku}/>
            </Box>


        </Box>
    );
}

export default Inventory;



