import React from 'react';
import { IconButton } from '@mui/material';
import AddCircleOutlineIcon from '@mui/icons-material/AddCircleOutline';
import { useNavigate } from 'react-router-dom'; // Ensure you have react-router-dom installed

const AddButton = () => {
    const navigate = useNavigate();

    const handleClick = () => {
        navigate("/form");
    };

    return (
        <IconButton onClick={handleClick}>
            <AddCircleOutlineIcon sx={{ fontSize: "30px" }} /> {/* You can adjust the color as needed */}
        </IconButton>
    );
};

export default AddButton;
