import React from 'react';
import { IconButton } from "@mui/material";
import PrintOutlinedIcon from "@mui/icons-material/PrintOutlined";
import axios from 'axios';

const PrintButton = ({ apiUrl, columns }) => {
    const handlePrint = async () => {
        try {
            const response = await axios.get(apiUrl);
            const data = response.data;

        // Check if data is defined and is an array
        if (!Array.isArray(data) || data.length === 0) {
            console.error("No data available for printing.");
            return; // Exit if there's no data
        }

        // Create a printable HTML table
        const printWindow = window.open('', '', 'height=600,width=800');
        printWindow.document.write('<html><head><title>Print</title>');
        printWindow.document.write('<style>table { width: 100%; border-collapse: collapse; }');
        printWindow.document.write('th, td { border: 1px solid black; padding: 8px; text-align: left; }</style>');
        printWindow.document.write('</head><body>');
        printWindow.document.write('<h1>Report</h1>');

        // Create the table header
        printWindow.document.write('<table><thead><tr>');
        columns.forEach(col => {
            printWindow.document.write(`<th>${col.headerName}</th>`); // Use headerName for display
        });
        printWindow.document.write('</tr></thead><tbody>');

        // Create table rows
        data.forEach(item => {
            printWindow.document.write('<tr>');
            columns.forEach(col => {
                printWindow.document.write(`<td>${item[col.field] !== undefined ? item[col.field] : ''}</td>`);
            });
            printWindow.document.write('</tr>');
        });

        printWindow.document.write('</tbody></table>');
        printWindow.document.write('</body></html>');
        printWindow.document.close();
        printWindow.print();
        } catch (error) {
        console.error("Error printing report:", error);
        }
        };

    return (
        <IconButton onClick={handlePrint}>
            <PrintOutlinedIcon sx={{ fontSize: "30px" }} />
        </IconButton>
    );
};

export default PrintButton;