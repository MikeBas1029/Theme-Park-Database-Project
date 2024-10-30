import Header from "../../../components/Header";
import { Box, useTheme, Button} from "@mui/material";
import { tokens } from "../../../theme";
import { useNavigate } from "react-router-dom";


const PurchaseTickets = () => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);
    const navigate = useNavigate();

    return (
        <Box m="20px">
        {/* Print | Export | Add  */}
        <Box display="flex" justifyContent="space-between" alignItems="center">
        <Header title="My Tickets" subtitle="View ticket purchase and activation history" />

        </Box>

        {/*Form fields, missing validation method linkings + user auth */}
            <Box
                m="40px 0 0 0"
                height="75vh"
            >
                Hi there
            </Box>
        </Box>
    );
};
    
    export default PurchaseTickets; 