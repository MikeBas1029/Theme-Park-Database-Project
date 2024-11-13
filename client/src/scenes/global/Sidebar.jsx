import {useState} from "react";
import { ProSidebar, Menu, MenuItem} from "react-pro-sidebar";

import {Box, IconButton, Typography, useTheme } from '@mui/material';
import { Link } from 'react-router-dom';
import "react-pro-sidebar/dist/css/styles.css"; /*CSS file not included potentiall breaks sidebar ??*/
import {tokens} from "../../theme";
import HomeOutlinedIcon from "@mui/icons-material/HomeOutlined";
import PeopleOutlinedIcon from "@mui/icons-material/PeopleOutlined";
import ReceiptOutlinedIcon from "@mui/icons-material/ReceiptOutlined";
import ContactsOutlinedIcon from "@mui/icons-material/ContactsOutlined";
import HandymanIcon from '@mui/icons-material/Handyman';
import LocalActivityIcon from '@mui/icons-material/LocalActivity';
import TourIcon from '@mui/icons-material/Tour';
import InventoryIcon from '@mui/icons-material/Inventory';
import InsightsIcon from '@mui/icons-material/Insights';
import AccessibilityNewIcon from '@mui/icons-material/AccessibilityNew';
import SecurityIcon from '@mui/icons-material/Security';
import MenuOutlinedIcon from "@mui/icons-material/MenuOutlined";
import MapOutlinedIcon from "@mui/icons-material/MapOutlined";
import { useUser } from "../../components/context/UserContext";
import AnalyticsOutlinedIcon from '@mui/icons-material/AnalyticsOutlined';


const Item = ({ title, to, icon, selected, setSelected }) => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);
    return (
      <MenuItem
        active={selected === title}
        style={{
          color: colors.grey[100],
        }}
        onClick={() => setSelected(title)}
        icon={icon}
      >
        <Typography>{title}</Typography>
        <Link to={to} />
      </MenuItem>
    );
  };


const Sidebar = () => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);
    const [isClosed, setIsClosed] = useState(false); 
    const [selected, setSelected] =useState("Dashboard");  
    const { user } = useUser(); //Get the user context




return(
    <Box
    sx ={{
      position: 'fixed',
      top: 0,
      left: 0,
      height: '100vh',
      width: isClosed ? '80px' : '250px',
      background: `${colors.grey[700]} !important`,
      zIndex: 1000,
        "& .pro-sidebar-inner": {
            background: `${colors.grey[700]} !important`
        },
        "& .pro-icon-wrapper": {
            backgroundColor: "transparent !important"
        },
        "& .pro-inner-item": {
            padding: "5px 35px 5px 20px !important"
        },
        "& .pro-inner-item:hover": {
            color: "#868dfb !important"
        },
        "& .pro-menu-item.active": {
            color : "#6870fa !important"
        }
    }}


>
<ProSidebar collapsed={isClosed}>
       <Menu iconShape="square">
         {/* LOGO AND MENU ICON */}
         <MenuItem
           onClick={() => setIsClosed(!isClosed)}
           icon={isClosed ? <MenuOutlinedIcon /> : undefined}
           style={{
             margin: "0px 0 20px 0",
             color: colors.grey[100],
           }}
         >
           {!isClosed && (
             <Box
               display="flex"
               justifyContent="space-between"
               alignItems="center"
               ml="15px"
             >
               <Typography variant="h3" color={colors.grey[100]}>
                   SHASTA PORTAL
               </Typography>
               <IconButton onClick={() => setIsClosed(!isClosed)}>
                 <MenuOutlinedIcon />
               </IconButton>
             </Box>
           )}
         </MenuItem>


         {!isClosed && (
           <Box mb="25px">
             <Box display="flex" justifyContent="center" alignItems="center">
               <img
                 alt="profile-photo"
                 width="100px"
                 height="100px"
                 src={user.userType === 'employee' ? '../../assets/user.png' : '../../assets/user2.jpeg'}
                 style={{ cursor: "pointer", borderRadius: "50%" }}
               />
             </Box>
             <Box textAlign="center">
               <Typography
                 variant="h2"
                 color={colors.grey[100]}
                 fontWeight="bold"
                 sx={{ m: "10px 0 0 0" }}
               >
                 {user.first_name} {user.last_name}
               </Typography>
               <Typography variant="h5" color={colors.greenAccent[500]}>
                 {user.role} |{`${user.email}`}
               </Typography>
             </Box>
           </Box>
         )}


         <Box paddingLeft={isClosed ? undefined : "10%"}>

            <Item
              title="Dashboard Home"
              to={user?.role === 'employee' ? '/employeedashboard' : user?.role === 'manager' ? '/managerdashboard' : '/dashboard'}
              icon={<HomeOutlinedIcon />}
              selected={selected}
              setSelected={setSelected}
            />

              {/* Employee elements */}
              {user.role === 'employee' && (
            <>
              <Typography variant="h4" color={colors.grey[300]} sx={{ m: "15px 0 5px 20px" }}>
                  My Employment
              </Typography>
              <Item
                  title="Timesheet"
                  to="/clockin"
                  icon={<AccessibilityNewIcon />}
                  selected={selected}
                  setSelected={setSelected}
              />
              <Item
                  title="Payroll"
                  to="/mypayroll"
                  icon={<InventoryIcon />}
                  selected={selected}
                  setSelected={setSelected}
              />
            </>)}


           {!isClosed &&(
           <Typography
             variant="h4"
             color={colors.grey[300]}
             sx={{ m: "15px 0 5px 20px" }}
           >
               Park Overview
           </Typography>
             )}



           {/* Park(admin) overview */}
           {user.role === 'admin' && (
            <>
            <Item
             title="Shops & Inventory"
             to="/supplies"
             icon={<InventoryIcon />}
             selected={selected}
             setSelected={setSelected}
           /> 
             <Item
              title="Orders & Vendors"
              to="/vendorsorders"
              icon={<ContactsOutlinedIcon />}
              selected={selected}
              setSelected={setSelected}
              />
            </>)}

            {/* Everyone but varying elements */}
            {user.role === 'employee' && (
            <>
              <Item
                  title="Shops & Dining"
                  to="/shops"
                  icon={<InventoryIcon />}
                  selected={selected}
                  setSelected={setSelected}
              />
            </>)}
            <Item
             title="Rides & Attractions"
             to="/rides"
             icon={<LocalActivityIcon />}
             selected={selected}
             setSelected={setSelected}
           />
            <Item
             title="Park Safety"
             to="/safety"
             icon={<SecurityIcon />}
             selected={selected}
             setSelected={setSelected}
           />




                
           {/* Manager elements */}
           {user.role === 'manager' && (
                            <>
             {!isClosed &&(
           <Typography
             variant="h4"
             color={colors.grey[300]}
             sx={{ m: "15px 0 5px 20px" }}
           >
             My Department
           </Typography>
                 )}

           <Item
             title="Manage Team"
             to="/my-team"
             icon={<PeopleOutlinedIcon />}
             selected={selected}
             setSelected={setSelected}
           />

           <Item
             title="Budget"
             to=""
             icon={<HandymanIcon />}
             selected={selected}
             setSelected={setSelected}
           />

            <Item
             title="Meetings"
             to=""
             icon={<TourIcon />}
             selected={selected}
             setSelected={setSelected}
           />

             {!isClosed &&(
           <Typography
             variant="h4"
             color={colors.grey[300]}
             sx={{ m: "15px 0 5px 20px" }}
           >
               Communication and Planning
           </Typography>
                 )}
             <Item
             title="Tasks"
             to=""
             icon={<InsightsIcon />}
             selected={selected}
             setSelected={setSelected}
             />

            <Item
             title="Workflow"
             to=""
             icon={<ReceiptOutlinedIcon />}
             selected={selected}
             setSelected={setSelected}
           />
            <Item
             title="Announcements"
             to=""
             icon={<AnalyticsOutlinedIcon />}
             selected={selected}
             setSelected={setSelected}
           />
          </>)}



           {/* Admin elements */}
           {user.role === 'admin' && (
                            <>
             {!isClosed &&(
           <Typography
             variant="h4"
             color={colors.grey[300]}
             sx={{ m: "15px 0 5px 20px" }}
           >
             Team and Operations
           </Typography>
                 )}

           <Item
             title="Manage Staff"
             to="/managestaff"
             icon={<PeopleOutlinedIcon />}
             selected={selected}
             setSelected={setSelected}
           />

           <Item
             title="Maintenance"
             to="/maintenance"
             icon={<HandymanIcon />}
             selected={selected}
             setSelected={setSelected}
           />

            <Item
             title="Customer/Visit info"
             to="/customervisits"
             icon={<TourIcon />}
             selected={selected}
             setSelected={setSelected}
           />

            <Item
             title="Facilities"
             to="/facilities"
             icon={<AccessibilityNewIcon />}
             selected={selected}
             setSelected={setSelected}
           />

             {!isClosed &&(
           <Typography
             variant="h4"
             color={colors.grey[300]}
             sx={{ m: "15px 0 5px 20px" }}
           >
               Reports and Analytics
           </Typography>
                 )}
           <Item
             title="Charts"
             to="/charts"
             icon={<AnalyticsOutlinedIcon />}
             selected={selected}
             setSelected={setSelected}
           />
             <Item
             title="Insights"
             to="/insights"
             icon={<InsightsIcon />}
             selected={selected}
             setSelected={setSelected}
             />

            <Item
             title="Finances"
             to="/finances"
             icon={<ReceiptOutlinedIcon />}
             selected={selected}
             setSelected={setSelected}
           />
          </>)}



         </Box>
       </Menu>
     </ProSidebar>
   </Box>
    );
}

export default Sidebar;
