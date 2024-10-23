import React from 'react';
import { IconButton } from "@mui/material";
import FileDownloadOutlinedIcon from "@mui/icons-material/FileDownloadOutlined";
import axios from 'axios';

const DownloadButton = ({ apiUrl, fileName }) => {
    const handleDownload = async () => {
        try {
            const response = await axios.get(apiUrl);
            const data = response.data;

            // Convert data to CSV format
            const csvContent = "data:text/csv;charset=utf-8,"
                + "Company Name,Vendor Contact,Phone Number,Email,Address Line 1,Address Line 2,City,Zip Code,Country,Vendor Type,Contract Start Date,Contract End Date,State\n" // Exported table header
                + data.map(vendor => 
                    `${vendor.company_name},${vendor.vendor_contact},${vendor.phone_number},${vendor.email},${vendor.address_line1},${vendor.address_line2},${vendor.city},${vendor.zip_code},${vendor.country},${vendor.vendor_type},${vendor.contract_start_date},${vendor.contract_end_date},${vendor.state}`
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
