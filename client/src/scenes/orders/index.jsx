import { Box, useTheme } from "@mui/material";
import { DataGrid, GridToolbar } from "@mui/x-data-grid";
import { tokens } from "../../theme";
import  Header from "../../components/Header"
import PrintButton from "../../components/PrintButton";
import AddButton from "../../components/AddButton";
import DownloadButton from "../../components/DownloadButton";
import { useEffect, useState } from "react";
import axios  from "axios"; //install if have !! needed for API requests


const Orders = () => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);
    
    const [ordersData, setOrdersData] = useState([]); {/*State for storing employee data*/}
    const [loading, setLoading] = useState(true); // Loading state

    {/*Fetch order data from endpoints when table is pulled*/}
useEffect(() => {
    const fetchOrdersData = async () => {
        try {
            const response = await axios.get("https://theme-park-backend.ambitioussea-02dd25ab.eastus.azurecontainerapps.io/api/v1/purchase-order-details/");
            console.log("Fetched shop:", response.data);
            setOrdersData(response.data);
        } catch (error) {
            console.error("Error fetching orders:", error);
        } finally {
            setLoading(false);
        }
    };

    fetchOrdersData();
    }, []);


    const columns = [
        {field: "order_details_id", headerName: "ID", flex: 1}, 
        {field: "order_id", headerName: "Order ID", flex: 1}, 
        {field: "supply_id", headerName: "Supply ID", flex: 1},
        {field: "quantity", headerName: "Quantity", flex: 1},
        {field: "unit_price", headerName: "Unit Price", flex: 1}
        ]; {/*field: value/data grabbed from  colName: column title in table */}

    return(
        <Box m="20px">
            <Box display="flex" justifyContent="space-between" alignItems="center">
                <Header title="Order Information💻" subtitle="View order information"/>
                <Box display="flex" alignItems="center">
                    <PrintButton apiUrl="http://127.0.0.1:8000/api/v1/customers/" columns={columns} />
                    <DownloadButton
                        apiUrl="http://127.0.0.1:8000/api/v1/orders/"
                        fileName="orders_report.csv"
                        columns={columns}
                    />
                    {/*Need to create a order form*/}
                    <AddButton navigateTo="orderform"/>
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
                }}>

                <DataGrid 
                checkboxSelection
                rows={ordersData}
                columns={columns} // Use the columns based on the toggle
                components={{ Toolbar: GridToolbar }}
                loading={loading}
                getRowId={(row) => row.order_details_id}/>
            </Box>


        </Box>
    );
}

export default Orders;
