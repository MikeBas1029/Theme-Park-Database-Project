import { Box, Typography, useTheme } from "@mui/material";
import { DataGrid } from "@mui/x-data-grid";
import { tokens } from "../../theme";
import  AdminPanelSettingsOutlinedIcon from "@mui/icons-material/AdminPanelSettingsOutlined";
import  LockOpenOutlinedIcon  from "@mui/icons-material/LockOpenOutlined";
import  SecurityOutlinedIcon  from "@mui/icons-material/SecurityOutlined";
import  Header from "../../components/Header"
import { sampleDataVendors } from "../../data/sampleVendorData";
import AddButton from "../../components/AddButton";
import PrintButton from "../../components/PrintButton";
import DownloadButton from "../../components/DownloadButton";
import AddCircleOutlineIcon from "@mui/icons-material/AddCircleOutline";
import IconButton from "@mui/material/IconButton";
import {useNavigate} from "react-router-dom";


const Orders = () => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);
    const navigate = useNavigate();

    const columns = [
        {field: "id", headerName: "ID"}, 
        {field: "name", headerName: "Name", flex: 1, cellClassName: "name-column--cell"}, 
        {field: "city", headerName: "City", headerAlign: "left", align: "left"},
        {field: "phone", headerName: "Phone Number", flex: 1},
        {field: "email", headerName: "Email", flex: 1},
        {field: "vendingType", headerName: "Supply Type"},
        ]; {/*field: value/data grabbed from  colName: column title in table */}

    return(
        <Box m="20px">
            <Box display="flex" justifyContent="space-between" alignItems="center">
                <Header title="Order Information💻" subtitle="View order information"/>
                <Box display="flex" alignItems="center">
                    <PrintButton apiUrl="http://127.0.0.1:8000/api/v1/customers/" columns={columns} />
                    <DownloadButton
                        apiUrl="http://127.0.0.1:8000/api/v1/orders/"
                        fileName="orders_report.csv"
                        columns={columns}
                    />
                    {/*Need to create a order form*/}
                    <AddButton navigateTo="orderform"/>
                </Box>
            </Box>
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
                }}>

                <DataGrid rows={sampleDataVendors} columns={columns}
                />
            </Box>


        </Box>
    );
}

export default Orders;
