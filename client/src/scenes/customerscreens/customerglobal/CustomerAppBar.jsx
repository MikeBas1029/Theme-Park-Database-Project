import { useState } from "react";
import { Box, IconButton, Typography, useTheme } from '@mui/material';
import { Link } from 'react-router-dom';
import { tokens } from "../../../theme";
import HomeOutlinedIcon from "@mui/icons-material/HomeOutlined";
import InventoryIcon from '@mui/icons-material/Inventory';
import LocalActivityIcon from '@mui/icons-material/LocalActivity';
import ContactsOutlinedIcon from '@mui/icons-material/ContactsOutlined';
import PeopleOutlinedIcon from '@mui/icons-material/PeopleOutlined';
import AccessibilityNewIcon from '@mui/icons-material/AccessibilityNew';
import HandymanIcon from '@mui/icons-material/Handyman';
import TourIcon from '@mui/icons-material/Tour';
import InsightsIcon from '@mui/icons-material/Insights';
import ReceiptOutlinedIcon from '@mui/icons-material/ReceiptOutlined';
import TimelineOutlinedIcon from '@mui/icons-material/TimelineOutlined';

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

const CustomerNavbar = () => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);

    return (
        <Box
            sx={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                background: colors.primary[400],
                padding: '10px 20px',
                position: 'sticky',
                top: 0,
                zIndex: 1000,
            }}
        >

            <Box display="flex">
                <Item title="Home" to="/customerhome" icon={<HomeOutlinedIcon />} />
                <Item title="My Tickets" to="/customertickets" icon={<InventoryIcon />} />
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
            <Box display="flex" alignItems="center">
                <img
                    alt="profile-photo"
                    width="50px"
                    height="50px"
                    src={`../../assets/user2.jpeg`}
                    style={{ borderRadius: "50%", marginRight: '10px' }}
                />
                <Typography variant="h6" color={colors.grey[100]}>
                    Sasha 'Gar
                </Typography>
            </Box>
            
        </Box>
    );
};

export default CustomerNavbar;
