import {useState} from "react";
import { ProSidebar, Menu, MenuItem} from "react-pro-sidebar";

import {Box, IconButton, Typography, useTheme } from '@mui/material';
import { Link, useNavigate } from 'react-router-dom';
import {tokens} from "../../theme";
import HomeOutlinedIcon from "@mui/icons-material/HomeOutlined";
import PeopleOutlinedIcon from "@mui/icons-material/PeopleOutlined";
import ReceiptOutlinedIcon from "@mui/icons-material/ReceiptOutlined";
import ContactsOutlinedIcon from "@mui/icons-material/ContactsOutlined";
import PersonOutlinedIcon from "@mui/icons-material/PersonOutlined";
import CalendarTodayOutlinedIcon from "@mui/icons-material/CalendarTodayOutlined";
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


const Sidebar = () => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);
    const [isClosed, setIsClosed] = useState(false); {/*sidebar status */}
    const [selected, setSelected] =useState("Dashboard");  {/*Which page/tab user is on */}


const navigate = useNavigate();


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
               <Typography variant="h3" color={colors.grey[100]}>
                  ADMIN
                 PORTAL
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
                 src={`../../assets/user.png`}
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
                 Mmokut Umoh
               </Typography>
               <Typography variant="h5" color={colors.greenAccent[500]}>
                 Manager | Ride Department
               </Typography>
             </Box>
           </Box>
         )}


         <Box paddingLeft={isClosed ? undefined : "10%"}>
           <Item
             title="Portal Home"
             to="/"
             icon={<HomeOutlinedIcon />}
             selected={selected}
             setSelected={setSelected}
             onClick={() => navigate("/")}
           />
           <Typography
               to="/"
             variant="h4"
             color={colors.grey[300]}
             sx={{ m: "15px 0 5px 20px" }}
           >
               Park Overview
           </Typography>
           <Item
             title="Manage Staff"
             to="/team"
             icon={<PeopleOutlinedIcon />}
             selected={selected}
             setSelected={setSelected}
           />
            <Item
             title="Rides/Attractions/Facilites"
             to="/contacts"
             icon={<ContactsOutlinedIcon />}
             selected={selected}
             setSelected={setSelected}
           />
            <Item
             title="Vendor Information"
             to="/contacts"
             icon={<ContactsOutlinedIcon />}
             selected={selected}
             setSelected={setSelected}
           />
           <Typography
             variant="h4"
             color={colors.grey[300]}
             sx={{ m: "15px 0 5px 20px" }}
           >
             Documents (?)
           </Typography>
           <Item
             title="Calendar"
             to="/calendar"
             icon={<CalendarTodayOutlinedIcon />}
             selected={selected}
             setSelected={setSelected}
           />
            <Item
             title="Transactions"
             to="/invoices"
             icon={<ReceiptOutlinedIcon />}
             selected={selected}
             setSelected={setSelected}
           />
           <Typography
             variant="h4"
             color={colors.grey[300]}
             sx={{ m: "15px 0 5px 20px" }}
           >
             Reports and Analytics
           </Typography>
           <Item
             title="Bar Chart"
             to="/bar"
             icon={<BarChartOutlinedIcon />}
             selected={selected}
             setSelected={setSelected}
           />
           <Item
             title="Line Chart"
             to="/line"
             icon={<TimelineOutlinedIcon />}
             selected={selected}
             setSelected={setSelected}
           />
           <Item
             title="Pie Chart"
             to="/pie"
             icon={<PieChartOutlineOutlinedIcon />}
             selected={selected}
             setSelected={setSelected}
           />
         </Box>
       </Menu>
     </ProSidebar>
   </Box>
    );
}

export default Sidebar; 