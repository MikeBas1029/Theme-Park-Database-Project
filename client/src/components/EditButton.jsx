import React from 'react';
import { IconButton } from '@mui/material';
import EditOutlinedIcon from '@mui/icons-material/EditOutlined';
import axios from 'axios';

const EditButton = ({ editingRow, disabled, sx, onSuccess }) => {
    const apiUrl = `https://theme-park-backend.ambitioussea-02dd25ab.eastus.azurecontainerapps.io/api/v1/shops/${editingRow?.shop_id}`;

    const handleClick = async () => {
        if (disabled || !editingRow) return;

        try {
            const { shop_id, ...dataToUpdate } = editingRow; // Exclude `shop_id` from data to be sent
            const response = await axios.put(apiUrl, dataToUpdate);

            console.log("Row updated successfully:", response.data);
            if (onSuccess) {
                onSuccess(response.data); // Callback to handle successful update
            }
        } catch (error) {
            console.error("Error updating data:", error);
        }
    };

    return (
        <IconButton 
            onClick={handleClick}
            disabled={disabled || !editingRow} 
            sx={{
                color: disabled || !editingRow ? 'grey.100' : 'primary.main',
                ...sx // Additional styles
            }}
        >
            <EditOutlinedIcon sx={{ fontSize: "30px" }} />
        </IconButton>
    );
};

export default EditButton;
