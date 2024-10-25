import { Box, useTheme, IconButton} from "@mui/material";
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


const Employees = () => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);
    const navigate = useNavigate();

    const [employeeData, setEmployeeData] = useState([]); {/*State for storing employee data*/}
    const [loading, setLoading] = useState(true); // Loading state


    {/*Fetch employee data from endpoints when table is pulled*/}
    useEffect(() => {
        const fetchEmployeeData = async () => {
            try {
                const response = await axios.get("http://127.0.0.1:8000/api/v1/employees/");
                console.log("Fetched employees:", response.data);
                setEmployeeData(response.data);
            } catch (error) {
                console.error("Error fetching employees:", error);
            } finally {
                setLoading(false);
            }
        };
    
        fetchEmployeeData();
        }, []);

        

    {/*Colums for employee table */ } {/*field: value/data grabbed from  headerName: column title in table*/}
    const columns = [
        { field: "employee_id", headerName: "EmployeeID", flex: 0.5 },
        { field: "ssn", headerName: "SSN", flex: 0.5 },
        { field: "first_name", headerName: "First Name", cellClassName: "name-column--cell" },
        { field: "last_name", headerName: "Last Name", cellClassName: "name-column--cell" },
        { field: "middle_initial", headerName: "MI", cellClassName: "name-column--cell" },
        { field: "phone_number", headerName: "Phone Number" },
        { field: "email", headerName: "Email" },
        { field: "address_line1", headerName: "Address Line 1" },
        { field: "address_line2", headerName: "Address Line 2" },
        { field: "city", headerName: "City" },
        { field: "state", headerName: "State" },
        { field: "zip_code", headerName: "Zip Code" },
        { field: "country", headerName: "Country" },
        { field: "dob", headerName: "Date of Birth" },
        { field: "start_date", headerName: "Start Date" },
        { field: "employee_type", headerName: "Employee Type" },
        { field: "hourly_wage", headerName: "Hourly Wage" },
        { field: "salary", headerName: "Salary" },
        { field: "job_function", headerName: "Job Function" },
        {field: "access", headerName: "Access Level", flex: 1, renderCell: ({row: {access}}) => {
            return (
                <Box
                width="60%"
                m="0 auto"
                p="5px"
                display="flex"
                justifyContent="center"
                backgroundColor={
                    access === "admin"
                    ? colors.greenAccent[600]
                    : colors.greenAccent[700]
                }
                borderRadius="4px"
                >
                    {access === "admin" && <AdminPanelSettingsOutlinedIcon /> }
                    {access === "manager" && <SecurityOutlinedIcon />}
                    {access === "user" && <LockOpenOutlinedIcon />}
                    <p color={colors.grey[100]} sx={{ml: "5px"}}>
                        {access}
                    </p>
                </Box>
            )
         }
        },
        ]; 
        

        


    return(

        
        <Box m="20px">
            {/* Print | Export | Add  */}    
            <Header title="Employeess✅" subtitle="Marhaban, kayfa halak"/>
            <PrintButton
                apiUrl="http://127.0.0.1:8000/api/v1/employees/" 
                columns={columns} />
            <DownloadButton 
                 apiUrl="http://127.0.0.1:8000/api/v1/employees/" 
                fileName="employees_report.csv" 
                columns={columns} 
                />
            <AddButton /> 
            <Box display="flex" justifyContent="space-between" alignItems="center">

            </Box>

            {/*Form fields, missing validation method linkings + user auth */}
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

            <DataGrid 
            checkboxSelection
            rows={employeeData} 
            columns={columns} 
            components={{Toolbar: GridToolbar}}
            loading={loading} 
            getRowId={(row) => row.employee_id}/>
            </Box>


        </Box>
    );
}

export default Employees;


