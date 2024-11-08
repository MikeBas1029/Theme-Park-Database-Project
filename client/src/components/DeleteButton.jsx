import React, { useState } from 'react';
import { IconButton, CircularProgress, Alert, Box, AlertTitle } from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import axios from 'axios';

const DeleteButton = ({ selectedItems, apiUrl, onDeleteSuccess }) => {
    const [loading, setLoading] = useState(false);
    const [statusMessage, setStatusMessage] = useState(null);
    const [statusType, setStatusType] = useState(''); // 'success' or 'error'

    const handleDelete = async () => {
        if (!selectedItems || selectedItems.length === 0) {
            setStatusMessage('No items selected for deletion');
            setStatusType('info');
            return;
        }

        // Confirm deletion
        const confirmDelete = window.confirm(
            `Are you sure you want to delete ${selectedItems.length} items?`
        );
        if (!confirmDelete) return;

        setLoading(true);
        setStatusMessage(null);

        try {
            // Iterate over each selected ID and delete
            for (const id of selectedItems) {
                await axios.delete(`${apiUrl}/${id}`);
                console.log(`Deleted item with ID: ${id}`);
            }

            // Success message and callback
            setStatusMessage('Items deleted successfully');
            setStatusType('success');
            if (onDeleteSuccess) onDeleteSuccess();
        } catch (error) {
            console.error('Error deleting items:', error);
            setStatusMessage('An error occurred while deleting items.');
            setStatusType('error');
        } finally {
            setLoading(false);
        }
    };

    return (
        <Box display="flex" flexDirection="column" alignItems="center">
            <IconButton onClick={handleDelete} disabled={loading || selectedItems.length === 0}>
                {loading ? (
                    <CircularProgress size={24} />
                ) : (
                    <DeleteIcon />
                )}
            </IconButton>

            {/* Display Alert for status messages */}
            {statusMessage && (
                <Alert variant="filled"severity={statusType} sx={{ mt: 2 }}>
                    <AlertTitle>{statusType} </AlertTitle>
                    {statusMessage}
                </Alert>
            )}
        </Box>
    );
};

export default DeleteButton;
