import { Box, Card, CardContent, Typography } from "@mui/material";
import { useNavigate } from "react-router-dom";
import Header from "../../components/Header";



const TransactionSelection = () => {


    const navigate = useNavigate();




    return <Box m="20px"> 
                <Header title="Transactions" subtitle="Select the Category you'd Like to see Transactions for. " />
                    <Box 
                        display="flex" 
                        justifyContent="center" 
                        alignItems="center" 
                        flexDirection="column"
                        gap={2}
                    >


        <Card sx={{ minWidth: 275, cursor: 'pointer'}} onClick={() => navigate('./transactions')}>
      <CardContent>
        <Typography variant="h5" component="div">
          Customer
        </Typography>
        <Typography variant="body2">
          View customer transaction history.
        </Typography>
      </CardContent>
      </Card>



        <Card sx={{ minWidth: 275, cursor: 'pointer'}} onClick={() => navigate('/transactions')}>
      <CardContent>
        <Typography variant="h5" component="div">
          Payroll
        </Typography>
        <Typography variant="body2">
          View employees salaries/paychecks
        </Typography>
      </CardContent>
      </Card>



        <Card sx={{ minWidth: 275, cursor: 'pointer'}} onClick={() => navigate('/invoices')}>
      <CardContent>
        <Typography variant="h5" component="div">
          Invoices
        </Typography>
        <Typography variant="body2">
          View invoice history for past orders.
        </Typography>
      </CardContent>
      </Card>
                    </Box>  
    
            </Box>
    
    }
    
    export default TransactionSelection; 