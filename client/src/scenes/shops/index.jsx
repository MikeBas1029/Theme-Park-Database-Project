import { Box, useTheme } from "@mui/material";
import { DataGrid, GridToolbar } from "@mui/x-data-grid";
import { tokens } from "../../theme";
import  Header from "../../components/Header"
import PrintButton from "../../components/PrintButton";
import AddButton from "../../components/AddButton";
import DownloadButton from "../../components/DownloadButton";
import { useEffect, useState } from "react";
import axios  from "axios"; //install if have !! needed for API requests
import EditButton from "../../components/EditButton";
import DeleteButton from "../../components/DeleteButton";



const Shops = () => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);
    
    const [ShopsData, setShopsData] = useState([]); {/*State for storing employee data*/}
    const [loading, setLoading] = useState(true); // Loading state
    const [selectedShop, setSelectedShop] = useState(null); // State for currently selected shop

    

    {/*Fetch shop data from endpoints when table is pulled*/}
useEffect(() => {
    const fetchShopsData = async () => {
        try {
            const response = await axios.get("https://theme-park-backend.ambitioussea-02dd25ab.eastus.azurecontainerapps.io/api/v1/shops/");
            console.log("Fetched shop:", response.data);
            setShopsData(response.data);
        } catch (error) {
            console.error("Error fetching shop:", error);
        } finally {
            setLoading(false);
        }
    };

    fetchShopsData();
    }, []);

    const handleRowSelection = (selectionModel) => {
        console.log("Selection Model Changed:", selectionModel); // Debugging line
        if (selectionModel.length > 0) {
            setSelectedShop(selectionModel[0]);
        } else {
            setSelectedShop(null);
        }
    };




    const columns = [
        {field: "shop_id", headerName: "ShopID", flex: 1}, 
        {field: "shop_name", headerName: "Shop Name", flex: 1, cellClassName: "name-column--cell"}, 
        {field: "address", headerName: "Address",flex: 1},
        {field: "park_section_id", headerName: "Park Section ID", flex: 1},
        {field: "manager_id", headerName: "Manager ID", flex: 1},
        {field: "opening_time", headerName: "Opening Time", flex: 1},
        {field: "closing_time", headerName: "Closing Time", flex: 1},
        
        ]; {/*field: value/data grabbed from  colName: column title in table */}

    return(
        <Box m="20px">
            <Box display="flex" justifyContent="space-between" alignItems="center">
                <Header title="Shops💻" subtitle="View a list of Theme Park Shops"/>
                <Box display="flex" alignItems="center">
                    <PrintButton
                        apiUrl="https://theme-park-backend.ambitioussea-02dd25ab.eastus.azurecontainerapps.io/api/v1/shops/"
                        columns={columns} />
                    <DownloadButton
                         apiUrl="https://theme-park-backend.ambitioussea-02dd25ab.eastus.azurecontainerapps.io/api/v1/shops/"
                        fileName="shops_report.csv"
                        columns={columns}
                        />
                        <EditButton
                        navigateTo={`/`} // Pass selectedShop ID to the EditButton
                        disabled={!selectedShop} // Disable if no shop is selected
                        sx={{
                            color: selectedShop ? colors.primary.main : colors.grey[500], // Change icon color based on selection
                        }}
                    />
                    <DeleteButton />
                    <AddButton navigateTo={'/shopform'} />
                </Box>
            </Box>

            <Box
            m="10px 0 0 0"
            height="75vh"
            sx={{"& .MuiDataGrid-root": {
                border: "none"
                }, 
                "& .MuiDataGrid-cell": {
                borderBottom: "none"
                },
                "& .name-column--cell": {
                color: colors.greenAccent[300]
                },
                "& .MuiDataGrid-columnHeader": {
                backgroundColor: colors.blueAccent[700],
                borderBottom: "none"
                },
                "& .MuiDataGrid-virtualScroller": {
                backgroundColor: colors.primary[400]
                },
                "& .MuiDataGrid-footerContainer": {
                borderTop: "none",
                backgroundColor: colors.blueAccent[700]
                },
                "& .MuicCheckbox-root": {
                color: `${colors.greenAccent[200]} !important`,
                },
                }}>

            <DataGrid 
                    checkboxSelection={true}
                    rows={ShopsData}
                    columns={columns} // Use the columns based on the toggle
                    components={{ Toolbar: GridToolbar }}
                    loading={loading}
                    getRowId={(row) => row.shop_id}
                    onSelectionModelChange={handleRowSelection} // Ensure this is set
                    />

            </Box>
        </Box>
    );
}

export default Shops;



