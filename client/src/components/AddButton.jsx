import React from 'react';
import { IconButton } from '@mui/material';
import AddCircleOutlineIcon from '@mui/icons-material/AddCircleOutline';
import { useNavigate } from 'react-router-dom'; // Ensure you have react-router-dom installed

const AddButton = ({ navigateTo}) => {
    const navigate = useNavigate();

    const handleClick = () => {
        navigate(navigateTo);
    };

    return (
        <IconButton onClick={handleClick}>
            <AddCircleOutlineIcon sx={{ fontSize: "30px" }} />
        </IconButton>
    );
};

export default AddButton;
