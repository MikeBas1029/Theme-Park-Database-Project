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
import Sidebar from "./Sidebar";


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


const SidebarCust = ({ userRole }) => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);
    const [isClosed, setIsClosed] = useState(false);
    const [selected, setSelected] = useState("Dashboard");

    // Define sidebar items based on user role
    const sidebarItems = {
        employee: [
            { title: "Dashboard Home", to: "/", icon: <HomeOutlinedIcon /> },
            { title: "Shops & Inventory", to: "/supplies", icon: <InventoryIcon /> },
            { title: "Orders & Vendors", to: "/vendorsandorders", icon: <ContactsOutlinedIcon /> },
            { title: "Rides & Attractions", to: "/rides", icon: <LocalActivityIcon /> },
            { title: "Park Safety", to: "/safety", icon: <SecurityIcon /> },
            { title: "Manage Staff", to: "/employees", icon: <PeopleOutlinedIcon /> },
            { title: "Maintenance", to: "/maintenance", icon: <HandymanIcon /> },
            { title: "Customer/Visit info", to: "/customervisits", icon: <TourIcon /> },
            { title: "Facilities", to: "/facilities", icon: <AccessibilityNewIcon /> },
            { title: "Insights", to: "/insights", icon: <InsightsIcon /> },
            { title: "Transactions", to: "/transactions", icon: <ReceiptOutlinedIcon /> },
            { title: "Tickets", to: "/tickets", icon: <TimelineOutlinedIcon /> },
        ],
        customer: [
            { title: "Dashboard Home", to: "/", icon: <HomeOutlinedIcon /> },
            { title: "My Profile", to: "/profile", icon: <PersonOutlinedIcon /> },
            { title: "Book Tickets", to: "/book-tickets", icon: <LocalActivityIcon /> },
            { title: "View Orders", to: "/my-orders", icon: <ReceiptOutlinedIcon /> },
        ],
    };

    // Get items based on user role
    const itemsToRender = sidebarItems[userRole] || sidebarItems['employee']; // Default to employee items

    return (
        <Box sx={{ /* your styles here */ }}>
            <ProSidebar collapsed={isClosed}>
                <Menu iconShape="square">
                    <MenuItem /* Logo and Menu Icon */ />
                    {!isClosed && /* Profile Picture and Name */(
                        <Box mb="25px">
                            <Box display="flex" justifyContent="center" alignItems="center">
                                <img
                                    alt="profile-photo"
                                    width="100px"
                                    height="100px"
                                    src={`../../assets/user2.jpeg`} // You may want to dynamically set this based on the logged-in user
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
                                    Sasha 'Gar {/* Replace with dynamic user name */}
                                </Typography>
                                <Typography variant="h5" color={colors.greenAccent[500]}>
                                    Manager | Ride Department {/* Replace with dynamic user role */}
                                </Typography>
                            </Box>
                        </Box>
                    )}

                    <Box paddingLeft={isClosed ? undefined : "10%"}>
                        {itemsToRender.map((item) => (
                            <Item
                                key={item.title}
                                title={item.title}
                                to={item.to}
                                icon={item.icon}
                                selected={selected}
                                setSelected={setSelected}
                            />
                        ))}
                    </Box>
                </Menu>
            </ProSidebar>
        </Box>
    );
};

export default SidebarCust;
