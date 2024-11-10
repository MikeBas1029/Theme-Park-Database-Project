import { Box, Button, IconButton, Typography, useTheme } from "@mui/material";
import { tokens } from "../../../theme";
import GroupsIcon from '@mui/icons-material/Groups';
import AssignmentTurnedInIcon from '@mui/icons-material/AssignmentTurnedIn';
import CampaignIcon from '@mui/icons-material/Campaign';
import Header from "../../../components/Header";
import StatBox from "../../../components/StatBox";
import DownloadButton from "../../../components/DownloadButton";
import LineChart from "../../../components/LineChart";
import { useUser } from "../../../components/context/UserContext";

const ManagerDashboard = () => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);
  const {user} = useUser();

  return (
    <Box m="20px">
      {/* HEADER */}
      <Box display="flex" justifyContent="space-between" alignItems="center">
      <Header title={`Hello, ${user.first_name}`} subtitle="Welcome Back !" />
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
          gridColumn="span 4"
          backgroundColor={colors.primary[400]}
          display="flex"
          alignItems="center"
          justifyContent="center"
        >
          <StatBox
            title="11/17/2024 - 24:59:59"
            subtitle="Next Deadline"
            progress="0.75"
            increase="+14%"
            icon={
              <AssignmentTurnedInIcon
                sx={{ color: colors.greenAccent[600], fontSize: "26px" }}
              />
            }
          />
        </Box>
        <Box
          gridColumn="span 4"
          backgroundColor={colors.primary[400]}
          display="flex"
          alignItems="center"
          justifyContent="center"
        >
          <StatBox
            title="11/10/2024 - 11:59:59"
            subtitle="Next Meeting"
            progress="0.50"
            increase="+21%"
            icon={
              <GroupsIcon
                sx={{ color: colors.greenAccent[600], fontSize: "26px" }}
              />
            }
          />
        </Box>
        <Box
          gridColumn="span 4"
          backgroundColor={colors.primary[400]}
          display="flex"
          alignItems="center"
          justifyContent="center"
        >
          <StatBox
            title="51"
            subtitle="Recent Announcements"
            progress="0.30"
            increase="+5%"
            icon={
              <CampaignIcon
                sx={{ color: colors.greenAccent[600], fontSize: "26px" }}
              />
            }
          />
        </Box>


        {/* ROW 2 */}
        <Box
          gridColumn="span 8"
          gridRow="span 5"
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
                Progress
              </Typography>
              <Typography
                variant="h3"
                fontWeight="bold"
                color={colors.greenAccent[500]}
              >
                1234 Tasks Remaining
              </Typography>
              <Typography
                variant="h5"
                fontWeight="bold"
                color={colors.grey[100]}
              >
                234423 Total this week
              </Typography>
            </Box>
            <Box>
                <DownloadButton
                  sx={{ fontSize: "26px", color: colors.greenAccent[500] }}
                />
        </Box>
          </Box>
          <Box height="250px" m="-20px 0 0 0">
            <LineChart isDashboard={true} />
          </Box>
        </Box>
        <Box
          gridColumn="span 4"
          gridRow="span 3"
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
              Approve Hours
            </Typography>
          </Box>
          Timelogs here
        </Box>

        {/* ROW 3 */}
        <Box
          gridColumn="span 4"
          gridRow="span 2"
          backgroundColor={colors.primary[400]}
          p="30px"
        >
          <Typography variant="h5" fontWeight="600">
            View Requests 
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
              0 Time-Off Requests
            </Typography>
            <Typography>The workers yearn for more time</Typography>
          </Box>
        </Box>
    </Box>
    </Box>
  );
};

export default ManagerDashboard;