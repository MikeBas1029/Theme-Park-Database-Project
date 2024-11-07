import { Box, useTheme, Button} from "@mui/material";
import { DataGrid, GridToolbar } from "@mui/x-data-grid";
import { tokens } from "../../theme";
import {sampleDataRoster} from "../../data/sampleData"
import  AdminPanelSettingsOutlinedIcon from "@mui/icons-material/AdminPanelSettingsOutlined";
import  LockOpenOutlinedIcon  from "@mui/icons-material/LockOpenOutlined";
import  SecurityOutlinedIcon  from "@mui/icons-material/SecurityOutlined";
import  Header from "../../components/Header"
import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import axios  from "axios"; //install if have !! needed for API requests
import DownloadButton from "../../components/DownloadButton";
import AddButton from "../../components/AddButton";
import PrintButton from "../../components/PrintButton";


const EmployeePayroll = ({ userRole }) => {
const theme = useTheme();
const colors = tokens(theme.palette.mode);
const navigate = useNavigate();

const [employeePayrollData, setEmployeePayrollData] = useState([]); {/*State for storing employee data*/}
const [loading, setLoading] = useState(true); // Loading state


{/*Fetch employee data from endpoints when table is pulled*/}
useEffect(() => {
    const fetchEmployeePayrollData = async () => {
        try {
            const response = await axios.get("https://theme-park-backend.ambitioussea-02dd25ab.eastus.azurecontainerapps.io/api/v1/employees/");
            console.log("Fetched employees:", response.data);
            setEmployeePayrollData(response.data);
        } catch (error) {
            console.error("Error fetching employees:", error);
        } finally {
            setLoading(false);
        }
    };

    fetchEmployeePayrollData();
    }, []);



{/*Colums for employee table */ }
const columns = [
    { field: "shift_id", headerName: "Shift ID", flex: 0.5 },
    { field: "employee_id", headerName: "Employee ID", flex: 0.5 },
    { field: "section_id", headerName: "Section ID", cellClassName: "name-column--cell" },
    { field: "shift_date", headerName: "Shift Date", cellClassName: "name-column--cell" },
    { field: "punch_in_time", headerName: "Clock In", cellClassName: "name-column--cell" },
    { field: "punch_out_time", headerName: "Clock out" },
    { field: "meal_break_start", headerName: "Break Start" },
    { field: "meal_break_end", headerName: "Break End" },
    { field: "status", headerName: "Status" },
    { field: "created_on", headerName: "Date Created" },
    { field: "updated_on", headerName: "Date Updated" },
    { field: "created_by", headerName: "Logged By" },
    { field: "updated_by", headerName: "Confirmed by" },
];



if (userRole === 'admin') {
    return (
        <Box m="20px">
            <Header title="Access Denied" subtitle="You do not have permission to view this page." />
        </Box>
    );
}

    return (
        <Box m="20px">
        {/* Print | Export | Add  */}
        <Box display="flex" justifyContent="space-between" alignItems="center">
            <Header title="All Employees✅" subtitle="...."/>
            <Box display="flex" alignItems="center">
                <PrintButton apiUrl="https://theme-park-backend.ambitioussea-02dd25ab.eastus.azurecontainerapps.io/api/v1/employees/"  />
                <DownloadButton apiUrl="https://theme-park-backend.ambitioussea-02dd25ab.eastus.azurecontainerapps.io/api/v1/employees/" fileName="employee_payroll_report.csv"  />
                <AddButton navigateTo={'/employeeform'}/>
            </Box>
        </Box>


        {/*Form fields, missing validation method linkings + user auth */}
            <Box
                m="40px 0 0 0"
                height="75vh"
                sx={{
                    "& .MuiDataGrid-root": { border: "none" },
                    "& .MuiDataGrid-cell": { borderBottom: "none" },
                    "& .MuiDataGrid-columnHeader": { backgroundColor: colors.blueAccent[700] },
                    "& .MuiDataGrid-virtualScroller": { backgroundColor: colors.primary[400] },
                    "& .MuiDataGrid-footerContainer": { borderTop: "none", backgroundColor: colors.blueAccent[700] }
                }}
            >
                <DataGrid
                    checkboxSelection
                    rows={employeePayrollData}
                    components={{ Toolbar: GridToolbar }}
                    loading={loading}
                    getRowId={(row) => row.shift_id}
                />
            </Box>
        </Box>
    );
};

export default EmployeePayroll;

