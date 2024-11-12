import { Box, Card, CardContent, Typography } from "@mui/material";
import CustomizedTabs from "../../../components/tabs";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Header from "../../../components/Header";
import Employees from "../../employees";
import EmployeePayroll from "../../employees/payroll";



const ManageStaff = () => {


  const navigate = useNavigate();

  {/*Table/Tab state management */}
    const [activeTab, setActiveTab] = useState('Employee Roster');
    const tabs = ['Employee Roster', 'Timesheets'];   // Page table tabs
    // Function to render the correct table component
    const renderTable = () => {
      switch (activeTab) {
        case 'Employee Roster':
          return <Employees />
        case 'Timesheets':
          return <EmployeePayroll />
        default:
          return null;
      }
    };
  
  
  

      return <Box m="20px"> 
                  <Header title="Vendor and Order " subtitle="Track order status/history, and view list of park vendors " />
                      <Box >
                        <CustomizedTabs tabs={tabs} activeTab={activeTab} setActiveTab={setActiveTab} />
                        {renderTable()} 
                      </Box>  
      
              </Box>
      
      }
    
    export default ManageStaff; 