import {Box, Icon, IconButton, useTheme } from "@mui/material";
import { useContext, useState } from "react";
import { DisplayModeContext, tokens } from "../../theme";
import InputBase from "@mui/material/InputBase";

import LightModeOutlinedIcon from "@mui/icons-material/LightModeOutlined";
import DarkModeOutlinedIcon from "@mui/icons-material/DarkModeOutlined"; 
import NotificationsOutlinedIcon from "@mui/icons-material/NotificationsOutlined";
import SettingsOutlinedIcon from "@mui/icons-material/SettingsOutlined"; 
import PersonOutlinedIcon from "@mui/icons-material/PersonOutlined";
import SearchIcon from "@mui/icons-material/Search";

import { useNavigate } from "react-router-dom";



const Navbar = () => {

    const theme = useTheme();
    const colors = tokens(theme.palette.mode); 
    const colorMode = useContext(DisplayModeContext);

    const [open, setOpen] = useState(false); 
    const navigate = useNavigate();



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

        {/*Icons */}
        <Box display="flex">
            <IconButton onClick={colorMode.toggleDisplayMode}>
                {theme.palette.mode === 'dark' ? (
                    <DarkModeOutlinedIcon />) : (
                <LightModeOutlinedIcon /> )}
            </IconButton>

            <IconButton>
                <NotificationsOutlinedIcon />
            </IconButton>

            <IconButton>
                <SettingsOutlinedIcon />
            </IconButton>

            <IconButton onClick={() => navigate("/login")}>
                <PersonOutlinedIcon />
            </IconButton>
        </Box>


    </Box>

)};
    
    export default Navbar; 