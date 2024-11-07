import { Box, Card, CardContent, Typography } from "@mui/material";
import CustomizedTabs from "../../components/tabs";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Header from "../../components/Header";
import Invoices from "../invoices";
import EmployeePayroll from "../payroll";
import Transactions from "../customertransactions";



const TransactionSelection = () => {


  const navigate = useNavigate();


  {/*Table/Tab state management */}
    const [activeTab, setActiveTab] = useState('Employee Payroll');
    const tabs = ['Employee Payroll', 'Vendor Invoices', 'Customer Transactions'];   // Page table tabs
    // Function to render the correct table component
    const renderTable = () => {
      switch (activeTab) {
        case 'Employee Payroll':
          return <EmployeePayroll />
        case 'Vendor Invoices':
          return <Invoices />
        case 'Customer Transactions':
          return <Transactions />
        default:
          return null;
      }
    };
  
  
  
  
      return <Box m="20px"> 
                  <Header title="Transactions" subtitle="Select the Category you'd Like to see Transactions for. " />
                      <Box >
                        <CustomizedTabs tabs={tabs} activeTab={activeTab} setActiveTab={setActiveTab} />
                        {renderTable()} 
                      </Box>  
      
              </Box>
      
      }
    
    export default TransactionSelection; 