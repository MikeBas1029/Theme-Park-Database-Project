import React, { useEffect, useState } from 'react';
import { Box, Card, CardContent, Typography, Modal } from '@mui/material';
import { useUser } from '../../../components/context/UserContext'; // Ensure you have the user context to access user data


const CustomerTickets = () => {
  const { user } = useUser(); // Get the logged-in user's info
  const [tickets, setTickets] = useState([]);
  const [selectedTicket, setSelectedTicket] = useState(null);

  useEffect(() => {
    const fetchTickets = async () => {
      if (!user) return; // If no user, don't fetch

      try {
        const response = await fetch(`/api/v1/tickets?email=${user.email}`);
        const data = await response.json();
        setTickets(data);
      } catch (error) {
        console.error("Error fetching tickets:", error);
      }
    };

    fetchTickets();
  }, [user]);

  const handleOpen = (ticket) => {
    setSelectedTicket(ticket);
  };

  const handleClose = () => {
    setSelectedTicket(null);
  };

  return (
    <Box display="grid" gridTemplateColumns="repeat(auto-fill, minmax(200px, 1fr))" gap={2}>
      {tickets.map((ticket) => (
        <Card key={ticket.id} onClick={() => handleOpen(ticket)} style={{ cursor: 'pointer' }}>
          <CardContent>
            <Typography variant="h6">{ticket.eventName}</Typography>
            <Typography variant="subtitle1">{ticket.date} - {ticket.time}</Typography>
            <Typography variant="body2">{ticket.price}</Typography>
          </CardContent>
        </Card>
      ))}

      {/* Modal for Ticket Details */}
      <Modal open={!!selectedTicket} onClose={handleClose}>
        <Box
          sx={{
            width: 400,
            bgcolor: 'background.paper',
            borderRadius: 2,
            boxShadow: 24,
            p: 4,
            m: 'auto',
            mt: '20%',
          }}
        >
          {selectedTicket && (
            <>
              <Typography variant="h5">{selectedTicket.eventName}</Typography>
              <Typography variant="subtitle1">{selectedTicket.date} - {selectedTicket.time}</Typography>
              <Typography variant="body1">{selectedTicket.details}</Typography>
              <Typography variant="h6">{selectedTicket.price}</Typography>
              <img src={selectedTicket.image} alt={selectedTicket.eventName} style={{ width: '100%' }} />
            </>
          )}
        </Box>
      </Modal>
    </Box>
  );
};

export default CustomerTickets;
