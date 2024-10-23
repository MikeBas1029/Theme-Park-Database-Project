import React from 'react';
import { IconButton } from "@mui/material";
import FileDownloadOutlinedIcon from "@mui/icons-material/FileDownloadOutlined";
import axios from 'axios';

const DownloadButton = ({ apiUrl, fileName, columns }) => {
    const handleDownload = async () => {
        try {
            const response = await axios.get(apiUrl);
            const data = response.data;

// Check if data is defined and is an array
if (!Array.isArray(data) || data.length === 0) {
    console.error("No data available for download.");
    return; // Exit if there's no data
}

// Generate CSV headers based on the columns prop
const csvHeaders = columns.map(col => col.field).join(","); // Extract fields from columns
const csvContent = "data:text/csv;charset=utf-8,"
    + csvHeaders + "\n" // CSV header row
    + data.map(item => 
        columns.map(col => item[col.field] !== undefined ? item[col.field] : '').join(",") // Extract values for each column
    ).join("\n");

            const encodedUri = encodeURI(csvContent);
            const link = document.createElement("a");
            link.setAttribute("href", encodedUri);
            link.setAttribute("download", fileName);
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link); // Clean up
        } catch (error) {
            console.error("Error downloading report:", error);
        }
    };

    return (
        <IconButton onClick={handleDownload}>
            <FileDownloadOutlinedIcon sx={{ fontSize: "30px" }} />
        </IconButton>
    );
};

export default DownloadButton;