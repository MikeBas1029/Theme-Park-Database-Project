import * as React from 'react';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import { Box, Typography } from '@mui/material';
import { useNavigate } from 'react-router-dom';

export default function DropdownMenu({ title, menuItems, icon }) {
  const [anchorEl, setAnchorEl] = React.useState(null);
  const open = Boolean(anchorEl);
  const navigate = useNavigate();

  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleMenuItemClick = (path) => {
    navigate(path);
    handleClose(); // Close the menu after navigation
  };

  return (
    <div>
      <Box
        onClick={handleClick}
        sx={{
          display: 'flex',
          alignItems: 'center',
          padding: '10px 20px',
          cursor: 'pointer',
        }}
      >
        {icon && <Box sx={{ marginRight: '8px' }}>{icon}</Box>}
        <Typography>{title}</Typography>
      </Box>
      <Menu
        id="basic-menu"
        anchorEl={anchorEl}
        open={open}
        onClose={handleClose}
        MenuListProps={{
          'aria-labelledby': 'basic-button',
        }}
      >
        {menuItems.map((item) => (
          <MenuItem key={item.label} onClick={() => handleMenuItemClick(item.path)}>
            {item.icon && <Box sx={{ marginRight: '8px' }}>{item.icon}</Box>}
            {item.label}
          </MenuItem>
        ))}
      </Menu>
    </div>
  );
}
