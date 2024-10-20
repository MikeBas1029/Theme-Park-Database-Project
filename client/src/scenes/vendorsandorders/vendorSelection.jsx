import { Box, Card, CardContent, Typography } from "@mui/material";
import CustomizedTabs from "../../components/tabs";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Header from "../../components/Header";
import Orders from "../orders";
import Vendors from "../vendors";



const VendorSelection = () => {


  const navigate = useNavigate();


  {/*Table/Tab state management */}
    const [activeTab, setActiveTab] = useState('Orders');
    const tabs = ['Orders', 'Vendors'];   // Page table tabs
    // Function to render the correct table component
    const renderTable = () => {
      switch (activeTab) {
        case 'Orders':
          return <Orders />
        case 'Vendors':
          return <Vendors />
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
    
    export default VendorSelection; 