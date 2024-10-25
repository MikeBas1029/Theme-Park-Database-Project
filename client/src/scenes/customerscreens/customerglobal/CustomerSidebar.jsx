import {useState} from "react";
import { ProSidebar, Menu, MenuItem} from "react-pro-sidebar";
import {Box, IconButton, Typography, useTheme } from '@mui/material';
import { Link } from 'react-router-dom';
import "react-pro-sidebar/dist/css/styles.css"; /*CSS file not included potentiall breaks sidebar ??*/
import { tokens } from "../../../theme";
import HomeOutlinedIcon from "@mui/icons-material/HomeOutlined";
import PeopleOutlinedIcon from "@mui/icons-material/PeopleOutlined";
import ReceiptOutlinedIcon from "@mui/icons-material/ReceiptOutlined";
import ContactsOutlinedIcon from "@mui/icons-material/ContactsOutlined";
import PersonOutlinedIcon from "@mui/icons-material/PersonOutlined";
import CalendarTodayOutlinedIcon from "@mui/icons-material/CalendarTodayOutlined";
import ConstructionIcon from '@mui/icons-material/Construction';
import HandymanIcon from '@mui/icons-material/Handyman';
import LocalActivityIcon from '@mui/icons-material/LocalActivity';
import TourIcon from '@mui/icons-material/Tour';
import InventoryIcon from '@mui/icons-material/Inventory';
import InsightsIcon from '@mui/icons-material/Insights';
import AccessibilityNewIcon from '@mui/icons-material/AccessibilityNew';
import SecurityIcon from '@mui/icons-material/Security';
import HelpOutlineOutlinedIcon from "@mui/icons-material/HelpOutlined";
import BarChartOutlinedIcon from "@mui/icons-material/BarChartOutlined";
import PieChartOutlineOutlinedIcon from "@mui/icons-material/PieChartOutlineOutlined";
import TimelineOutlinedIcon from "@mui/icons-material/TimelineOutlined";
import MenuOutlinedIcon from "@mui/icons-material/MenuOutlined";
import MapOutlinedIcon from "@mui/icons-material/MapOutlined";


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


const CustomerSidebar = () => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);
    const [isClosed, setIsClosed] = useState(false); {/*sidebar status */}
    const [selected, setSelected] =useState("Dashboard");  {/*Which page/tab user is on */}


return(
    <Box
    sx ={{
        "& .pro-sidebar-inner": {
            background: `${colors.primary[400]} !important`
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
                 src={`../../assets/user2.jpeg`}
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
                 Sasha 'Gar
               </Typography>
               <Typography variant="h5" color={colors.greenAccent[500]}>
                 GOLD Member
               </Typography>
             </Box>
           </Box>
         )}


         <Box paddingLeft={isClosed ? undefined : "10%"}>
           <Item
             title="Home"
             to="/customerhome"
             icon={<HomeOutlinedIcon />}
             selected={selected}
             setSelected={setSelected}
           />

           {!isClosed &&(
           <Typography
             to="/"
             variant="h4"
             color={colors.grey[300]}
             sx={{ m: "15px 0 5px 20px" }}
           >
               Park Overview
           </Typography>
             )}

            <Item
             title=" My Tickets"
             to="/customertickets"
             icon={<InventoryIcon />}
             selected={selected}
             setSelected={setSelected}
           />

            <Item
             title="Rides & Attractions"
             to="/parkrides"
             icon={<ContactsOutlinedIcon />}
             selected={selected}
             setSelected={setSelected}
           />

            <Item
             title="Events"
             to="/customerevents"
             icon={<LocalActivityIcon />}
             selected={selected}
             setSelected={setSelected}
           />
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
             title="Map"
             to="/parkmap"
             icon={<PeopleOutlinedIcon />}
             selected={selected}
             setSelected={setSelected}
           />

            <Item
             title="Facilities"
             to="/parkfacilities"
             icon={<AccessibilityNewIcon />}
             selected={selected}
             setSelected={setSelected}
           /> 

           <Item
             title="Dining"
             to="/parkdining"
             icon={<TourIcon />}
             selected={selected}
             setSelected={setSelected}
           />

           <Item
             title="Shopping"
             to="/parkshops"
             icon={<HandymanIcon />}
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
             title="FAQS"
             to="/faqs"
             icon={<InsightsIcon />}
             selected={selected}
             setSelected={setSelected}
             />

            <Item
             title="Help Center"
             to="/helpcenter"
             icon={<ReceiptOutlinedIcon />}
             selected={selected}
             setSelected={setSelected}
           />

           <Item
             title="Feedback"
             to="/feedback"
             icon={<TimelineOutlinedIcon />}
             selected={selected}
             setSelected={setSelected}
           />
         </Box>
       </Menu>
     </ProSidebar>
   </Box>
    );
}

export default CustomerSidebar; 