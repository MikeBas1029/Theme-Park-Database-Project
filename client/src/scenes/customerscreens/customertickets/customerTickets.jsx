import React, { useEffect, useState } from 'react';
import { Box, Card, CardContent, Typography, Modal } from '@mui/material';
import { useUser } from '../../../components/context/UserContext'; // Ensure you have the user context to access user data


const CustomerTickets = ({customer_id}) => {
  const { user } = useUser(); // Get the logged-in user's info
  const [tickets, setTickets] = useState([]);
  const [selectedTicket, setSelectedTicket] = useState(null);
  const [loading, setLoading] = useState(true);


  useEffect(() => {
    const fetchTickets = async () => {
      if (!user) return; // If no user, don't fetch

      try {
        const response = await fetch(`https://theme-park-backend.ambitioussea-02dd25ab.eastus.azurecontainerapps.io/api/v1/tickets/`);
        const data = await response.json();
        console.log(data); // Log the fetched data
        setTickets(Array.isArray(data) ? data : []);
      } catch (error) {
        console.error("Error fetching tickets:", error);
      } finally {
        setLoading(false);
    }
    };

    fetchTickets();
  }, [customer_id, user]);

  const handleOpen = (ticket) => {
    setSelectedTicket(ticket);
  };

  const handleClose = () => {
    setSelectedTicket(null);
  };

  
  return (
    <Box display="grid" gridTemplateColumns="repeat(auto-fill, minmax(200px, 1fr))" gap={2}>
      {tickets.length === 0 ? (
        <Typography variant="body1">No tickets available.</Typography>
      ) : (
        tickets.map((ticket) => (
          <Card key={ticket.id} onClick={() => handleOpen(ticket)} style={{ cursor: 'pointer' }}>
            <CardContent>
              <Typography variant="h6">{ticket.ticket_type}</Typography>
              <Typography variant="subtitle1">{ticket.start_date} </Typography>
              <Typography variant="body2">{ticket.status}</Typography>
            </CardContent>
          </Card>
        ))
      )}

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
              <Typography variant="h5"> Ticket: {selectedTicket.ticket_type}</Typography>
              <Typography variant="body1"> Purchased on: {selectedTicket.purchase_date}</Typography>
              <Typography variant="h6">Status: {selectedTicket.status}</Typography>
              <Typography variant="subtitle1">Activated: {selectedTicket.start_date}</Typography>
              {/* {<img src={selectedTicket.image} alt={selectedTicket.eventName} style={{ width: '100%' }} />} */}
            </>
          )}
        </Box>
      </Modal>
    </Box>
  );
};

export default CustomerTickets;
