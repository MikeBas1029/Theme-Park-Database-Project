import React from 'react';
import { IconButton } from '@mui/material';
import EditOutlinedIcon from '@mui/icons-material/EditOutlined';
import { useNavigate } from 'react-router-dom'; // Ensure you have react-router-dom installed

const EditButton = ({ navigateTo, disabled, sx}) => {
    const navigate = useNavigate();

    const handleClick = () => {
        if (!disabled) {
            navigate(navigateTo);
        }else {
            console.log("Edit button is disabled."); // Debugging line
        }
    };

    return (
        <IconButton onClick={handleClick} 
        disabled={disabled} 
        sx={{
            color: disabled ? 'grey.100' : 'primary.main', // Change icon color based on disabled state
            ...sx // Allow for additional styles to be passed
        }} >
            <EditOutlinedIcon sx={{ fontSize: "30px" }} />
        </IconButton>
    );
};

export default EditButton;
