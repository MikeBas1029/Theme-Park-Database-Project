import React, {useState} from 'react';
import { IconButton } from '@mui/material';
import DeleteForeverOutlinedIcon from '@mui/icons-material/DeleteForeverOutlined';
import { useNavigate } from 'react-router-dom'; // Ensure you have react-router-dom installed

const DeleteButton = ({ disabled, onDelete}) => {
    const [open, setOpen] = useState(false);
    const [password, setPassword] = useState('');
    const handleClick = () => {
        if (!disabled) {
            setOpen(true);
        }
    };

    const handleClose = () => {
        setOpen(false);
        setPassword('');
    };

    const handleDelete = () => {
        if (password === 'yourHardcodedPassword') {
            onDelete(); // Call the delete function passed from parent
            handleClose();
        } else {
            alert('Incorrect password.'); // Handle incorrect password
        }
    };

    return (
        <IconButton onClick={handleClick} 
        disabled={disabled}  >
            <DeleteForeverOutlinedIcon sx={{ fontSize: "30px" }} />
        </IconButton>
    );
};

export default DeleteButton;
