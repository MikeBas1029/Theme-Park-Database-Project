import { Box, Button, IconButton, Typography, useTheme } from "@mui/material";
import Header from "../../components/Header";
import DownloadOutlinedIcon from "@mui/icons-material/DownloadOutlined";
import EmojiPeopleIcon from '@mui/icons-material/EmojiPeople';
import ThunderstormIcon from '@mui/icons-material/Thunderstorm';
import PointOfSaleIcon from "@mui/icons-material/PointOfSale";
import PersonAddIcon from "@mui/icons-material/PersonAdd";
import TrafficIcon from "@mui/icons-material/Traffic";
import { tokens } from "../../theme";
import StatBox from "../../components/StatBox";





const Dashboard = () => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);



    return <Box m="20px">
    {/* HEADER */}
    <Box display="flex" justifyContent="space-between" alignItems="center">
      <Header title="DASHBOARD" subtitle="Welcome to your dashboard" />

      <Box>
        <Button
          sx={{
            backgroundColor: colors.blueAccent[700],
            color: colors.grey[100],
            fontSize: "14px",
            fontWeight: "bold",
            padding: "10px 20px",
          }}
        >
          <DownloadOutlinedIcon sx={{ mr: "10px" }} />
          Download Reports
        </Button>
      </Box>
    </Box>

    {/* GRID & CHARTS */}
    <Box
      display="grid"
      gridTemplateColumns="repeat(12, 1fr)"
      gridAutoRows="140px"
      gap="20px"
    >
    {/* ROW 1 */}
    <Box
        gridColumn="span 3"
        backgroundColor={colors.primary[400]}
        display="flex"
        alignItems="center"
        justifyContent="center"
      >
        <StatBox
          title="20"
          subtitle="Avg. Monthly Customers"
          progress="0.50"
          increase="-50%"
          icon={
            <EmojiPeopleIcon
              sx={{ color: colors.greenAccent[100], fontSize: "26px" }}
            />
          }
        />
      </Box>
    <Box
        gridColumn="span 3"
        backgroundColor={colors.primary[400]}
        display="flex"
        alignItems="center"
        justifyContent="center"
      >
        <StatBox
          title="2"
          subtitle="Rainouts this Month"
          progress="0.50"
          increase="-20%"
          icon={
            <ThunderstormIcon
              sx={{ color: colors.greenAccent[100], fontSize: "26px" }}
            />
          }
        />
      </Box>
      <Box
        gridColumn="span 3"
        backgroundColor={colors.primary[400]}
        display="flex"
        alignItems="center"
        justifyContent="center"
      >
        <Typography>
            Recents incidents: 
            N/A
        </Typography>
      </Box>
      <Box
        gridColumn="span 3"
        backgroundColor={colors.primary[400]}
        display="flex"
        alignItems="center"
        justifyContent="center"
      >
        <StatBox
          title="90"
          subtitle="Total Customers"
          progress="0.50"
          increase="-50%"
          icon={
            <EmojiPeopleIcon
              sx={{ color: colors.greenAccent[100], fontSize: "26px" }}
            />
          }
        />
      </Box>

      {/* ROW 2 */}
      <Box
        gridColumn="span 8"
        gridRow="span 2"
        backgroundColor={colors.primary[400]}
      >
        <Box
          mt="25px"
          p="0 30px"
          display="flex "
          justifyContent="space-between"
          alignItems="center"
        >
          <Box>
            <Typography
              variant="h5"
              fontWeight="600"
              color={colors.grey[100]}
            >
              Revenue Generated
            </Typography>
            <Typography
              variant="h3"
              fontWeight="bold"
              color={colors.greenAccent[500]}
            >
              $39
            </Typography>
          </Box>
          <Box>
            <IconButton>
              <DownloadOutlinedIcon
                sx={{ fontSize: "26px", color: colors.greenAccent[500] }}
              />
            </IconButton>
          </Box>
        </Box>
        <Box height="250px" m="-20px 0 0 0">
        </Box>
      </Box>
      <Box
        gridColumn="span 4"
        gridRow="span 2"
        backgroundColor={colors.primary[400]}
        overflow="auto"
      >
        <Box
          display="flex"
          justifyContent="space-between"
          alignItems="center"
          borderBottom={`4px solid ${colors.primary[500]}`}
          colors={colors.grey[100]}
          p="15px"
        >
          <Typography color={colors.grey[100]} variant="h5" fontWeight="600">
            Recent Transactions
          </Typography>
        </Box>
      </Box>

      {/* ROW 3 */}
      <Box
        gridColumn="span 4"
        gridRow="span 2"
        backgroundColor={colors.primary[400]}
        p="30px"
      >
        <Typography variant="h5" fontWeight="600">
        Popular Rides
        </Typography>
        <Box
          display="flex"
          flexDirection="column"
          alignItems="center"
          mt="25px"
        >

          <Typography
            variant="h5"
            color={colors.greenAccent[500]}
            sx={{ mt: "15px" }}
          >
            Giant Wheel
          </Typography>
          <Typography>GIANT WHEEL was Ridden: 22 times this month🔥</Typography>
        </Box>
      </Box>
      <Box
        gridColumn="span 4"
        gridRow="span 2"
        backgroundColor={colors.primary[400]}
      >
        <Typography
          variant="h5"
          fontWeight="600"
          sx={{ padding: "30px 30px 0 30px" }}
        >
          Customer Statistics
          </Typography>
        <Box height="250px" mt="-20px">
        </Box>
      </Box>
      <Box
        gridColumn="span 4"
        gridRow="span 2"
        backgroundColor={colors.primary[400]}
        padding="30px"
      >
        <Typography
          variant="h5"
          fontWeight="600"
          sx={{ marginBottom: "15px" }}
        >
          Operational Summary
        </Typography>
        <Box height="200px">
        </Box>
      </Box>
    </Box>
  </Box>
};
    
    export default Dashboard; 