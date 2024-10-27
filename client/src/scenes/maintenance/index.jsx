import { Box, Typography, useTheme } from "@mui/material";
import { DataGrid, GridToolbar } from "@mui/x-data-grid";
import { tokens } from "../../theme";
import { sampleInvoices } from "../../data/sampleInvoices";
import  AdminPanelSettingsOutlinedIcon from "@mui/icons-material/AdminPanelSettingsOutlined";
import  LockOpenOutlinedIcon  from "@mui/icons-material/LockOpenOutlined";
import  SecurityOutlinedIcon  from "@mui/icons-material/SecurityOutlined";
import  Header from "../../components/Header"
import { useState, useEffect } from "react";
import axios from "axios";
import DownloadButton from "../../components/DownloadButton";
import AddButton from "../../components/AddButton";
import PrintButton from "../../components/PrintButton";


const Maintenance = () => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);



    const [workOrderInfo, setworkOrderInfo] = useState([]); {/*State for storing employee data*/}
    const [loading, setLoading] = useState(true); // Loading state


    useEffect(() => {
        const fetchworkOrderInfo = async () => {
            try {
                const response = await axios.get("http://127.0.0.1:8000/api/v1/work-orders/"); //missing table but link should be working
                console.log("Fetched employees:", response.data);
                setworkOrderInfo(response.data);
            } catch (error) {
                console.error("Error fetching employees:", error);
            } finally {
                setLoading(false);
            }
        };
    
        fetchworkOrderInfo();
        }, []);

    const columns = [
        {field: "woid", headerName: "WorkOrderID", flex: 0.5}, 
        {field: "section_id", headerName: "Section", flex: 1, cellClassName: "name-column--cell"}, 
        {field: "ride_id", headerName: "Ride ID"},
        {field: "invoice_id", headerName: "Invoice ID", flex: 0.5}, 
        {field: "date", headerName: "Date", flex: 1},
        {field: "maintenance_date", headerName: "Date of Service", flex: 1},
        {field: "maintenance_type", headerName: "Maintenance Type", flex: 0.5}, 
        {field: "assigned_worker_id", headerName: "Assigned Worker(ID)", flex: 0.5}, 
        {field: "date_created", headerName: "Date Created", flex: 0.5}, 
        {field: "updated_at", headerName: "Date Updated", flex: 0.5}, 
        {field: "created_by", headerName: "Created By", flex: 0.5}, 
        {field: "updated_by", headerName: "Updated By", flex: 0.5}, 
        {field: "status", headerName: "Status", flex: 0.5}, 


        
        ]; {/*field: value/data grabbed from  colName: column title in table */}

    return(
        <Box m="20px">
            <Box display="flex" justifyContent="space-between" alignItems="center">
                <Header title="Maintenance💻" subtitle="Keep track of park work orders and maintenance schedules."/>
                <Box display="flex" alignItems="center">
                    <PrintButton
                        apiUrl="http://127.0.0.1:8000/api/v1/work-orders/"
                        columns={columns} />
                    <DownloadButton
                         apiUrl="http://127.0.0.1:8000/api/v1/work-orders/"
                        fileName="customers_report.csv"
                        columns={columns}
                        />
                    <AddButton navigateTo="/maintenanceform"/>
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
                "& .MuicCheckbox-root": {
                color: `${colors.greenAccent[200]} !important`,
                },
                }}>

            <DataGrid 
            checkboxSelection
            rows={workOrderInfo} 
            columns={columns} 
            components={{Toolbar: GridToolbar}}
            loading={loading} 
            getRowId={(row) => row.woid}/>    
            </Box>
        </Box>
    );
}

export default Maintenance;



