import { Box, Card, CardContent, Typography } from "@mui/material";
import { useNavigate } from "react-router-dom";
import Header from "../../components/Header";
import CustomizedTabs from "../../components/tabs";
import { useState } from "react";
import Shops from "../shops";
import Inventory from "../inventory";



const Supplies = () => {


const navigate = useNavigate();


{/*Table/Tab state management */}
  const [activeTab, setActiveTab] = useState('Shops');
  const tabs = ['Shops', 'Inventory'];   // Page table tabs
  // Function to render the correct table component
  const renderTable = () => {
    switch (activeTab) {
      case 'Shops':
        return <Shops />;
      case 'Inventory':
        return <Inventory />;
      default:
        return null;
    }
  };




    return <Box m="20px"> 
                <Header title="Shops and Inventory" subtitle="Select the Category you'd Like to see Transactions for. " />
                    <Box >
                      <CustomizedTabs tabs={tabs} activeTab={activeTab} setActiveTab={setActiveTab} />
                      {renderTable()} 
                    </Box>  
    
            </Box>
    
    }
    
    export default Supplies; 