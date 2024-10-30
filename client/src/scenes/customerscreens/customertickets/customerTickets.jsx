import React, { useEffect, useState } from 'react';
import { Box, Card, CardContent, Typography, Modal } from '@mui/material';
import Header from '../../../components/Header';
import { useUser } from '../../../components/context/UserContext'; 


const CustomerTickets = () => {
  const { user } = useUser(); // Get the logged-in user's info
  
  const customer_id = user.customer_id; // grab customer_id from user context
  const [tickets, setTickets] = useState([]);
  const [selectedTicket, setSelectedTicket] = useState(null);
  const [loading, setLoading] = useState(true);


  useEffect(() => {
    const fetchTickets = async () => {
      if (!user) return; // If no user, don't fetch

      try {
        const response = await fetch(`http://127.0.0.1:8000/api/v1/tickets/user/${customer_id}`);   //     https://theme-park-backend.ambitioussea-02dd25ab.eastus.azurecontainerapps.io/api/v1/employees//api/v1/tickets/user/${customer_id}  //for live backend api 
        const data = await response.json();
        console.log("Cust ID",customer_id)
        console.log("Fetched Data:", data); // Log the fetched data
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
    <Box m="20px">
      <Header title="My Tickets" subtitle="View your purchased tickets" />
      <Box display="grid" gridTemplateColumns="repeat(auto-fill, minmax(200px, 1fr))" gap={2} >
      {tickets.length === 0 ? (
        <Typography variant="body1">No tickets available. for ID: {customer_id ? customer_id : "..."} </Typography>
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
      </Box>

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
