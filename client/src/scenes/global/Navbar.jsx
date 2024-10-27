import {Box, Icon, IconButton, useTheme, Typography} from "@mui/material";
import { useContext, useState } from "react";
import { DisplayModeContext, tokens } from "../../theme";
import InputBase from "@mui/material/InputBase";

import LightModeOutlinedIcon from "@mui/icons-material/LightModeOutlined";
import DarkModeOutlinedIcon from "@mui/icons-material/DarkModeOutlined"; 
import NotificationsOutlinedIcon from "@mui/icons-material/NotificationsOutlined";
import CalendarTodayOutlinedIcon from "@mui/icons-material/CalendarTodayOutlined"; 
import PersonOutlinedIcon from "@mui/icons-material/PersonOutlined";
import SearchIcon from "@mui/icons-material/Search";
import HomeOutlinedIcon from "@mui/icons-material/HomeOutlined";
import InventoryIcon from '@mui/icons-material/Inventory';
import LocalActivityIcon from '@mui/icons-material/LocalActivity';
import ContactsOutlinedIcon from '@mui/icons-material/ContactsOutlined';
import PeopleOutlinedIcon from '@mui/icons-material/PeopleOutlined';
import AccessibilityNewIcon from '@mui/icons-material/AccessibilityNew';
import HandymanIcon from '@mui/icons-material/Handyman';
import TourIcon from '@mui/icons-material/Tour';

import { useNavigate } from "react-router-dom";
import ProfileDropdown from "../../components/ProfileDropdown";
import AccountMenu from "../../components/AccountMenu";
import { Link } from "react-router-dom";



const Item = ({ title, to, icon }) => {
    return (
        <Link to={to} style={{ textDecoration: 'none', color: 'inherit' }}>
            <Box sx={{ display: 'flex', alignItems: 'center', padding: '10px 20px' }}>
                {icon}
                <Typography sx={{ marginLeft: '8px' }}>{title}</Typography>
            </Box>
        </Link>
    );
};


const Navbar = ({userRole} ) => {

    const theme = useTheme();
    const colors = tokens(theme.palette.mode); 
    const colorMode = useContext(DisplayModeContext);

    const [open, setOpen] = useState(false); 
    const navigate = useNavigate();


    const [dropdownOpen, setDropdownOpen] = useState(false);
    const toggleDropdown = () => {
        setDropdownOpen((prev) => !prev);
    };


    return (
    <Box display="flex" justifyContent="space-between" p={2} > 
        {/*Search bar*/}
        <Box 
            display="flex" 
            backgroundColor={colors.primary[400]}
            borderRadius="3px"
        >
             
            <InputBase sx={{ml: 2, flex: 1}} placeholder="Search"/>
            <IconButton type="button" sx={{p: 1}}>
                <SearchIcon /> 
            </IconButton>
        </Box> 

        {userRole === 'customer' ? (
            <Box display="flex" ml="auto">
            {/* Customer navbar*/}
            <Item title="Home" to="/customerhome" icon={<HomeOutlinedIcon />} />
            <Item title="My Tickets" to="/customertickets" icon={<LocalActivityIcon />} />
            <Item title="Rides & Attractions" to="/parkrides" icon={<ContactsOutlinedIcon />} />
            <Item title="Events" to="/customerevents" icon={<LocalActivityIcon />} />
            <Item title="Map" to="/parkmap" icon={<PeopleOutlinedIcon />} />
            <Item title="Facilities" to="/parkfacilities" icon={<AccessibilityNewIcon />} />
            <Item title="Dining" to="/parkdining" icon={<TourIcon />} />
            <Item title="Shopping" to="/parkshops" icon={<HandymanIcon />} />
            {/* <Item title="FAQS" to="/faqs" icon={<InsightsIcon />} />*/}
           {/*  <Item title="Help Center" to="/helpcenter" icon={<ReceiptOutlinedIcon />} />*/}
            {/* <Item title="Feedback" to="/feedback" icon={<TimelineOutlinedIcon />} />*/}
             </Box>

      ) : (
        <Box display="flex" ml="auto">
        {/* Employee navbar*/}
            {/*Icons */}
            <IconButton onClick={colorMode.toggleDisplayMode} sx={{ ml: 1 }}>
                {theme.palette.mode === 'dark' ? <DarkModeOutlinedIcon /> : <LightModeOutlinedIcon />}
            </IconButton>

            <IconButton sx={{ ml: 1 }}>
                <CalendarTodayOutlinedIcon />
            </IconButton>

            <IconButton sx={{ ml: 1 }}>
                <NotificationsOutlinedIcon />
            </IconButton>
            
        </Box>
        
      )}
            <AccountMenu userRole={userRole} />


    </Box>

); };
    
    export default Navbar; 