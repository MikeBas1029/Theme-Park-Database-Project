import { useEffect, useState } from 'react';
import axios from 'axios';
import { Box, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Typography } from '@mui/material';

const Leaderboard = ({ selectedMonth }) => {
  const [rideData, setRideData] = useState([]);
  const [loading, setLoading] = useState(true);

  // Function to fetch and sort data
  useEffect(() => {
    const fetchRideData = async () => {
      try {
        const response = await axios.get('https://theme-park-backend.ambitioussea-02dd25ab.eastus.azurecontainerapps.io/api/v1/reports/frequent-rides');
        setRideData(response.data);
      } catch (error) {
        console.error('Error fetching ride data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchRideData();
  }, []);

  // Filter the rideData based on the selected month
  const filteredData = rideData.filter(ride => ride.month === selectedMonth).sort((a, b) => b.num_rides - a.num_rides);

  return (
    <Box m="20px">
      {loading ? (
        <div>Loading...</div>
      ) : (
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Rank</TableCell>
                <TableCell>Ride Name</TableCell>
                <TableCell align="right">Number of Rides</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {filteredData.map((ride, index) => (
                <TableRow key={`${ride.name}-${index}`}>
                  <TableCell>{index + 1}</TableCell>
                  <TableCell>{ride.name}</TableCell>
                  <TableCell align="right">{ride.num_rides}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}
    </Box>
  );
};

export default Leaderboard;
