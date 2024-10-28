import { Box, Typography, useTheme } from "@mui/material";
import { DataGrid } from "@mui/x-data-grid";
import { tokens } from "../../theme";
import  AdminPanelSettingsOutlinedIcon from "@mui/icons-material/AdminPanelSettingsOutlined";
import  LockOpenOutlinedIcon  from "@mui/icons-material/LockOpenOutlined";
import  SecurityOutlinedIcon  from "@mui/icons-material/SecurityOutlined";
import  Header from "../../components/Header"
import { sampleDataVendors } from "../../data/sampleVendorData";
import AddButton from "../../components/AddButton";
import DownloadButton from "../../components/DownloadButton";
import PrintButton from "../../components/PrintButton";


const Safety = () => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);

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
            <Header title="Park Safety💻" subtitle="View and log park incident reports"/>
            <PrintButton
                apiUrl="https://theme-park-backend.ambitioussea-02dd25ab.eastus.azurecontainerapps.io/api/v1/employees/" 
                columns={columns} />
            <DownloadButton 
                 apiUrl="https://theme-park-backend.ambitioussea-02dd25ab.eastus.azurecontainerapps.io/api/v1/employees/" 
                fileName="customers_report.csv" 
                columns={columns} 
                />
            <AddButton navigateTo={'/safetyform'}/> 
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
                }}>

                <DataGrid rows={sampleDataVendors} columns={columns}
                />
            </Box>


        </Box>
    );
}

export default Safety;
