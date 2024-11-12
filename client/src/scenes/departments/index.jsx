import { Box, useTheme, Button} from "@mui/material";
import { DataGrid, GridToolbar } from "@mui/x-data-grid";
import { tokens } from "../../theme";
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
import { useUser } from "../../components/context/UserContext";


const Departments = () => {
const theme = useTheme();
const colors = tokens(theme.palette.mode);
const navigate = useNavigate();
const {user} = useUser();


const [employeeData, setEmployeeData] = useState([]); {/*State for storing employee data*/}
const [loading, setLoading] = useState(true); // Loading state
const [showFullColumns, setShowFullColumns] = useState(true);


{/*Fetch employee data from endpoints when table is pulled*/}
useEffect(() => {
    const fetchEmployeeData = async () => {
        try {
            const response = await axios.get(`https://theme-park-backend.ambitioussea-02dd25ab.eastus.azurecontainerapps.io/api/v1/departments/
`);
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
    { field: "department_id", headerName: "Dept ID"},
    { field: "name", headerName: "Dept Name" },
    { field: "num_employees", headerName: "# of Employees" },
    { field: "budget", headerName: "Department Budget" },
    { field: "department_role", headerName: "Department Role", flex: 1 },
];



    return (
        <Box m="20px">
        {/* Print | Export | Add  */}
        <Box display="flex" justifyContent="space-between" alignItems="center">
            <Header title="All Departments" subtitle="List of all the departments in business"/>
            <Box display="flex" alignItems="center">
                <PrintButton apiUrl={`https://theme-park-backend.ambitioussea-02dd25ab.eastus.azurecontainerapps.io/api/v1/departments/
`} columns={columns} />
                <DownloadButton apiUrl={`https://theme-park-backend.ambitioussea-02dd25ab.eastus.azurecontainerapps.io/api/v1/departments/
`} fileName="employees_report.csv" columns={columns} />
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
                    rows={employeeData}
                    columns={columns} 
                    components={{ Toolbar: GridToolbar }}
                    loading={loading}
                    getRowId={(row) => row.department_id}
                />
            </Box>
        </Box>
    );
};

export default Departments;

