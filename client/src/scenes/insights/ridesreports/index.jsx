import React, { useEffect, useState } from "react";
import { Box, Typography, useTheme, Select, MenuItem } from "@mui/material";
import { DataGrid, GridToolbar } from "@mui/x-data-grid";
import { tokens } from "../../../theme";
import Header from "../../../components/Header";
import DownloadButton from "../../../components/DownloadButton";
import PrintButton from "../../../components/PrintButton";
import axios from "axios";

const RidesReports = () => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);

    const [ridesData, setRidesData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [selectedRange, setSelectedRange] = useState("year"); // Default range is 'year'
    const [rangeOptions, setRangeOptions] = useState([]);
    const [selectedValue, setSelectedValue] = useState(null);

    // Columns for DataGrid
    const columns = [
        { field: "rowNumber", headerName: "#", width: 60, sortable: false },
        { field: "ride_name", headerName: "Ride", flex: 1 },
        { field: "ride_type", headerName: "Category", flex: 1 },
        { field: "year", headerName: "Year", flex: 1 },
        { field: "yearly_count", headerName: "Yearly Count", flex: 1 },
        { field: "month", headerName: "Month", flex: 1 },
        { field: "monthly_count", headerName: "Monthly Count", flex: 1 },
        { field: "week", headerName: "Week", flex: 1 },
        { field: "weekly_count", headerName: "Weekly Count", flex: 1 },
        { field: "day", headerName: "Day", flex: 1 },
        { field: "daily_count", headerName: "Daily Count", flex: 1 },
    ];

    useEffect(() => {
        const fetchRidesData = async () => {
            try {
                const response = await axios.get("https://theme-park-backend.ambitioussea-02dd25ab.eastus.azurecontainerapps.io/api/v1/reports/ride-counts");
                setRidesData(response.data);
            } catch (error) {
                console.error("Error fetching ride data:", error);
            } finally {
                setLoading(false);
            }
        };
        fetchRidesData();
    }, []);

    // Generate options for the range selection (year, month, week, or day)
    useEffect(() => {
        if (selectedRange && ridesData.length) {
            const uniqueOptions = [...new Set(ridesData.map((item) => item[selectedRange]))];
            setRangeOptions(uniqueOptions);
        }
    }, [selectedRange, ridesData]);

    // Filter data based on the selected range and value
    const filteredData = ridesData.filter((item) => {
        if (selectedValue === null) return true;
        return item[selectedRange] === selectedValue;
    });

    // Add row numbers to each row for display
    const rowsWithNumbers = filteredData.map((row, index) => ({ ...row, rowNumber: index + 1 }));

    return (
        <Box m="20px">
            {/* Header with Print, Download, and Add Buttons */}
            <Box display="flex" justifyContent="space-between" alignItems="center">
                <Header title="Rides Reports" subtitle="View ride statistics by selected range" />
                <Box display="flex" alignItems="center">
                    <PrintButton apiUrl="https://theme-park-backend.ambitioussea-02dd25ab.eastus.azurecontainerapps.io/api/v1/reports/ride-counts" columns={columns} />
                    <DownloadButton
                        apiUrl="https://theme-park-backend.ambitioussea-02dd25ab.eastus.azurecontainerapps.io/api/v1/reports/ride-counts"
                        fileName="ride_counts_report.csv"
                        columns={columns}
                    />
                </Box>
            </Box>

            {/* Dropdown Filters */}
            <Box display="flex" gap="10px" mb="20px">
                <Select
                    value={selectedRange}
                    onChange={(e) => {
                        setSelectedRange(e.target.value);
                        setSelectedValue(null); // Reset selected value when range changes
                    }}
                    displayEmpty
                    variant="outlined"
                    style={{ minWidth: 120 }}
                >
                    <MenuItem value="year">Year</MenuItem>
                    <MenuItem value="month">Month</MenuItem>
                    <MenuItem value="week">Week</MenuItem>
                    <MenuItem value="day">Day</MenuItem>
                </Select>

                {rangeOptions.length > 0 && (
                    <Select
                        value={selectedValue}
                        onChange={(e) => setSelectedValue(e.target.value)}
                        displayEmpty
                        variant="outlined"
                        style={{ minWidth: 120 }}
                    >
                        <MenuItem value={null}>All</MenuItem>
                        {rangeOptions.map((option) => (
                            <MenuItem key={option} value={option}>
                                {selectedRange === "month" ? `Month ${option}` : option}
                            </MenuItem>
                        ))}
                    </Select>
                )}
            </Box>

            {/* Data Grid */}
            <Box
                height="75vh"
                sx={{
                    "& .MuiDataGrid-root": { border: "none" },
                    "& .MuiDataGrid-cell": { borderBottom: "none" },
                    "& .name-column--cell": { color: colors.greenAccent[300] },
                    "& .MuiDataGrid-columnHeader": { backgroundColor: colors.blueAccent[700], borderBottom: "none" },
                    "& .MuiDataGrid-virtualScroller": { backgroundColor: colors.primary[400] },
                    "& .MuiDataGrid-footerContainer": { borderTop: "none", backgroundColor: colors.blueAccent[700] },
                    "& .MuiDataGrid-toolbarContainer .MuiButton-text": { color: `${colors.greenAccent[100]} !important`, backgroundColor: colors.blueAccent[700] },
                }}
            >
                {loading ? (
                    <div>Loading...</div>
                ) : (
                    <DataGrid
                        rows={rowsWithNumbers}
                        columns={columns}
                        components={{ Toolbar: GridToolbar }}
                        getRowId={(row) => row.rowNumber}
                        checkboxSelection
                    />
                )}
            </Box>
        </Box>
    );
};

export default RidesReports;
