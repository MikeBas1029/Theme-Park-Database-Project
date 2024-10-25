import { Box, Typography, useTheme } from "@mui/material";
import { DataGrid, GridToolbar } from "@mui/x-data-grid";
import { tokens } from "../../theme";
import { sampleInvoices } from "../../data/sampleInvoices";
import  Header from "../../components/Header"
import DownloadButton from "../../components/DownloadButton";
import AddButton from "../../components/AddButton";
import PrintButton from "../../components/PrintButton";


const Payroll = () => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);

    const columns = [
        {field: "id", headerName: "ID", flex: 0.5}, 
        {field: "vendorName", headerName: "Name", flex: 1, cellClassName: "name-column--cell"}, 
        {field: "invoiceNumber", headerName: "Invoice Number"},
        {field: "amount", headerName: "Price", flex: 1, renderCell: (params) => (
            <Typography color={colors.greenAccent[500]}>
            {new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(params.value)}
          </Typography>
            

        )},
        {field: "date", headerName: "Data", flex: 1},
        {field: "status", headerName: "Payment Status", flex: 1},
        
        ]; {/*field: value/data grabbed from  colName: column title in table */}

    return(
        <Box m="20px">
            <Header title="Employee Payroll💻" subtitle="Record of invoices from vendor orders"/>
            <PrintButton
                apiUrl="http://127.0.0.1:8000/api/v1/customers/" 
                columns={columns} />
            <DownloadButton 
                 apiUrl="http://127.0.0.1:8000/api/v1/customers/" 
                fileName="customers_report.csv" 
                columns={columns} 
                />
            <AddButton /> 
            <Box
            m="40px 0 0 0"
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

            <DataGrid checkboxSelection rows={sampleInvoices} columns={columns} components={{Toolbar: GridToolbar}}/>
            </Box>


        </Box>
    );
}

export default Payroll;



