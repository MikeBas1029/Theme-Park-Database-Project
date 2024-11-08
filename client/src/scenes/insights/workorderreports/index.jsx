import { Box, Typography, useTheme } from "@mui/material";
import { DataGrid, GridToolbar } from "@mui/x-data-grid";
import { tokens } from "../../../theme";
import Header from "../../../components/Header";
import { useState, useEffect } from "react";
import axios from "axios";
import DownloadButton from "../../../components/DownloadButton";
import AddButton from "../../../components/AddButton";
import PrintButton from "../../../components/PrintButton";

const MaintenanceReports = () => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);

    const [workOrderInfo, setWorkOrderInfo] = useState([]);
    const [loading, setLoading] = useState(true);

    // Fetch data from the API
    useEffect(() => {
        const fetchWorkOrderInfo = async () => {
            try {
                const response = await axios.get("https://theme-park-backend.ambitioussea-02dd25ab.eastus.azurecontainerapps.io/api/v1/reports/broken-rides");
                console.log("Fetched work-orders:", response.data);
                setWorkOrderInfo(response.data);
            } catch (error) {
                console.error("Error fetching work-orders:", error);
            } finally {
                setLoading(false);
            }
        };
        fetchWorkOrderInfo();
    }, []);

    // Table columns
    const columns = [
        { field: "ride_name", headerName: "Ride Name", flex: 1 },
        { field: "last_inspected", headerName: "Last Inspected", flex: 1 },
        { field: "ride_status", headerName: "Ride Status", flex: 1 },
        { field: "assigned_employee", headerName: "Assigned Employee", flex: 1 },
        { field: "maintenance_type", headerName: "Maintenance Type", flex: 1 },
        { field: "date_created", headerName: "Date Created", flex: 1 },
        { field: "wo_status", headerName: "Work Order Status", flex: 1 }
    ];

    return (
        <Box m="20px">
            <Box display="flex" justifyContent="space-between" alignItems="center">
                <Header title="Maintenance Reports" subtitle="Review ride maintenance records for the year" />
                <Box display="flex" alignItems="center">
                    <PrintButton
                        apiUrl="https://theme-park-backend.ambitioussea-02dd25ab.eastus.azurecontainerapps.io/api/v1/work-orders/"
                        columns={columns}
                    />
                    <DownloadButton
                        apiUrl="https://theme-park-backend.ambitioussea-02dd25ab.eastus.azurecontainerapps.io/api/v1/work-orders/"
                        fileName="maintenance_report.csv"
                        columns={columns}
                    />
                    <AddButton navigateTo="/maintenanceform" />
                </Box>
            </Box>
            <Box
                m="40px 0 0 0"
                height="75vh"
                sx={{
                    "& .MuiDataGrid-root": { border: "none" },
                    "& .MuiDataGrid-cell": { borderBottom: "none" },
                    "& .name-column--cell": { color: colors.greenAccent[300] },
                    "& .MuiDataGrid-columnHeader": {
                        backgroundColor: colors.blueAccent[700],
                        borderBottom: "none"
                    },
                    "& .MuiDataGrid-virtualScroller": { backgroundColor: colors.primary[400] },
                    "& .MuiDataGrid-footerContainer": {
                        borderTop: "none",
                        backgroundColor: colors.blueAccent[700]
                    },
                    "& .MuiCheckbox-root": { color: `${colors.greenAccent[200]} !important` }
                }}
            >
                <DataGrid
                    checkboxSelection
                    rows={workOrderInfo}
                    columns={columns}
                    components={{ Toolbar: GridToolbar }}
                    loading={loading}
                    getRowId={(row) => row.ride_name} 
                />
            </Box>
        </Box>
    );
};

export default MaintenanceReports;
