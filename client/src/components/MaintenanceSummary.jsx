import { useEffect, useState } from 'react';
import axios from 'axios';
import { Box, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Typography } from '@mui/material';

const MaintenanceSummary = () => {
  const [maintenanceData, setMaintenanceData] = useState([]);
  const [loading, setLoading] = useState(true);

  // Fetch maintenance data when the component mounts
  useEffect(() => {
    const fetchMaintenanceData = async () => {
      try {
        const response = await axios.get('https://theme-park-backend.ambitioussea-02dd25ab.eastus.azurecontainerapps.io/api/v1/reports/broken-rides');
        setMaintenanceData(response.data);
        console.log(response.data);
      } catch (error) {
        console.error('Error fetching maintenance data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchMaintenanceData();
  }, []);

  return (
    <Box m="20px">
      {loading ? (
        <div>Loading...</div>
      ) : (
        <TableContainer component={Paper} style={{ maxHeight: '300px', overflow: 'auto' }}>
          <Table stickyHeader>
            <TableHead>
              <TableRow>
                <TableCell align="center">Month</TableCell>
                <TableCell align="center">Rides Maintained</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {maintenanceData.length > 0 ? (
                maintenanceData.map((item, index) => (
                  <TableRow key={`maintenance-${index}`}>
                    <TableCell align="center">{item.Maintenance_Month}</TableCell>
                    <TableCell align="center">{item.Num_Rides_Maintained}</TableCell>
                  </TableRow>
                ))
              ) : (
                <TableRow>
                  <TableCell colSpan={2} align="center">
                    No maintenance data available.
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </TableContainer>
      )}
    </Box>
  );
};

export default MaintenanceSummary;
