import { Box, useTheme } from "@mui/material";
import { DataGrid, GridToolbar } from "@mui/x-data-grid";
import { tokens } from "../../theme";
import Header from "../../components/Header";
import PrintButton from "../../components/PrintButton";
import AddButton from "../../components/AddButton";
import DownloadButton from "../../components/DownloadButton";
import { useEffect, useState } from "react";
import axios from "axios"; //install if have !! needed for API requests

//facility_id, facility_name, facility_type, location_id, status
const Facilities = ({ isOpen }) => {
	const theme = useTheme();
	const colors = tokens(theme.palette.mode);
	const [FacilitiesData, setFacilitiesData] = useState([]);
	{
		/*State for storing facilities data*/
	}
	const [loading, setLoading] = useState(true); // Loading state

	{
		/*Fetch facilities data from endpoints when table is pulled*/
	}
	useEffect(() => {
		const fetchFacilitiesData = async () => {
			try {
				const response = await axios.get(
					"https://theme-park-backend.ambitioussea-02dd25ab.eastus.azurecontainerapps.io/api/v1/park-factilities/"
				);
				console.log("Fetched facilites:", response.data);
				setFacilitiesData(response.data);
			} catch (error) {
				console.error("Error fetching facilities:", error);
			} finally {
				setLoading(false);
			}
		};

		fetchFacilitiesData();
	}, []);
	const columns = [
		{ field: "facility_id", headerName: "Facility ID", flex: 1 },
		{
			field: "facility_name",
			headerName: "Facility Name",
			flex: 1,
			cellClassName: "name-column--cell",
		},
		{ field: "facility_type", headerName: "Facility Type", flex: 1 },
		{ field: "location_id", headerName: "Location ID", flex: 1 },
		{ field: "status", headerName: "Status", flex: 1 },
	];
	{
		/*field: value/data grabbed from  colName: column title in table */
	}

	return (
		<Box
			m="20px"
			ml={isOpen ? "250px" : "80px"} // Adjust left margin based on isOpen
			transition="margin 0.3s ease" // Smooth transition for margin
		>
			<Header
				title="Park Facilities💻"
				subtitle="View park facilities (restrooms, etc)"
			/>
			<PrintButton
				apiUrl="https://theme-park-backend.ambitioussea-02dd25ab.eastus.azurecontainerapps.io/api/v1/park-factilities/"
				columns={columns}
			/>
			<DownloadButton
				apiUrl="https://theme-park-backend.ambitioussea-02dd25ab.eastus.azurecontainerapps.io/api/v1/park-factilities/"
				fileName="customers_report.csv"
				columns={columns}
			/>
			<AddButton navigateTo={"/facilitiesform"} />
			<Box
				m="40px 0 0 0"
				height="75vh"
				sx={{
					"& .MuiDataGrid-root": {
						border: "none",
					},
					"& .MuiDataGrid-cell": {
						borderBottom: "none",
					},
					"& .name-column--cell": {
						color: colors.greenAccent[300],
					},
					"& .MuiDataGrid-columnHeader": {
						backgroundColor: colors.blueAccent[700],
						borderBottom: "none",
					},
					"& .MuiDataGrid-virtualScroller": {
						backgroundColor: colors.primary[400],
					},
					"& .MuiDataGrid-footerContainer": {
						borderTop: "none",
						backgroundColor: colors.blueAccent[700],
					},
				}}
			>
				<DataGrid
					checkboxSelection
					rows={FacilitiesData}
					columns={columns} // Use the columns based on the toggle
					components={{ Toolbar: GridToolbar }}
					loading={loading}
					getRowId={(row) => row.facility_id}
				/>
			</Box>
		</Box>
	);
};

export default Facilities;
