import { Box, useTheme } from "@mui/material";
import { DataGrid, GridToolbar } from "@mui/x-data-grid";
import { tokens } from "../../theme";
import Header from "../../components/Header";
import PrintButton from "../../components/PrintButton";
import AddButton from "../../components/AddButton";
import DownloadButton from "../../components/DownloadButton";
import { useEffect, useState } from "react";
import axios from "axios";
import EditButton from "../../components/EditButton";
import DeleteButton from "../../components/DeleteButton";

const Shops = ({ isOpen }) => {
	const theme = useTheme();
	const colors = tokens(theme.palette.mode);
	const [ShopsData, setShopsData] = useState([]);
	const [loading, setLoading] = useState(true);
	const [selectedShops, setSelectedShops] = useState([]);
	const [editingRow, setEditingRow] = useState(null);

	useEffect(() => {
		const fetchShopsData = async () => {
			try {
				const response = await axios.get(
					"https://theme-park-backend.ambitioussea-02dd25ab.eastus.azurecontainerapps.io/api/v1/shops/"
				);
				console.log("Fetched Shops Data:", response.data);
				setShopsData(response.data);
			} catch (error) {
				console.error("Error fetching shop:", error);
			} finally {
				setLoading(false);
			}
		};
		fetchShopsData();
	}, []);

	// Handle row selection
	const handleRowSelection = (selectionModel) => {
		setSelectedShops(selectionModel);
		const selectedRowData =
			selectionModel.length === 1
				? ShopsData.find((shop) => shop.shop_id === selectionModel[0])
				: null;
		setEditingRow(selectedRowData);
		console.log("Editing Row Data:", selectedRowData); // Log for debugging
	};

	// Define columns with editable properties
	const columns = [
		{ field: "shop_id", headerName: "ShopID", flex: 1 },
		{
			field: "shop_name",
			headerName: "Shop Name",
			flex: 1,
			editable: true,
		},
		{ field: "address", headerName: "Address", flex: 1, editable: true },
		{ field: "park_section_id", headerName: "Park Section ID", flex: 1 },
		{
			field: "manager_id",
			headerName: "Manager ID",
			flex: 1,
			editable: true,
		},
		{
			field: "opening_time",
			headerName: "Opening Time",
			flex: 1,
			editable: true,
		},
		{
			field: "closing_time",
			headerName: "Closing Time",
			flex: 1,
			editable: true,
		},
	];

	return (
		<Box
			m="20px"
			ml={isOpen ? "250px" : "80px"} // Adjust left margin based on isOpen
			transition="margin 0.3s ease" // Smooth transition for margin
		>
			<Box
				display="flex"
				justifyContent="space-between"
				alignItems="center"
			>
				<Header
					title="Shops💻"
					subtitle="View a list of Theme Park Shops"
				/>
				<Box display="flex" alignItems="center">
					<PrintButton
						apiUrl="https://theme-park-backend.ambitioussea-02dd25ab.eastus.azurecontainerapps.io/api/v1/shops/"
						columns={columns}
					/>
					<DownloadButton
						apiUrl="https://theme-park-backend.ambitioussea-02dd25ab.eastus.azurecontainerapps.io/api/v1/shops/"
						fileName="shops_report.csv"
						columns={columns}
					/>
					<EditButton
						editingRow={editingRow}
						disabled={!editingRow}
						onSuccess={(updatedRow) => {
							// Update ShopsData state with the updated row details
							setShopsData((prevData) =>
								prevData.map((shop) =>
									shop.shop_id === updatedRow.shop_id
										? updatedRow
										: shop
								)
							);
							setEditingRow(null); // Clear editingRow state after save
						}}
					/>
					<DeleteButton
						selectedItems={selectedShops}
						apiUrl="https://theme-park-backend.ambitioussea-02dd25ab.eastus.azurecontainerapps.io/api/v1/shops/"
						onDeleteSuccess={() => {
							setShopsData((prevData) =>
								prevData.filter(
									(shop) =>
										!selectedShops.includes(shop.shop_id)
								)
							);
							setSelectedShops([]);
						}}
					/>
					<AddButton navigateTo={"/shopform"} />
				</Box>
			</Box>

			<Box
				m="10px 0 0 0"
				height="75vh"
				sx={{
					"& .MuiDataGrid-root": { border: "none" },
					"& .MuiDataGrid-cell": { borderBottom: "none" },
					"& .name-column--cell": { color: colors.greenAccent[300] },
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
					"& .Mui-selected": {
						backgroundColor: colors.primary[200], // Highlight edited row
					},
				}}
			>
				<DataGrid
					checkboxSelection
					rows={ShopsData}
					columns={columns}
					components={{ Toolbar: GridToolbar }}
					loading={loading}
					getRowId={(row) => row.shop_id}
					onRowSelectionModelChange={handleRowSelection}
				/>
			</Box>
		</Box>
	);
};

export default Shops;
