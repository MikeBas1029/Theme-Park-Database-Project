import React from "react";
import { useState, useEffect, useRef } from "react";
import { Menu, MenuItem } from "react-pro-sidebar";

const ProfileDropdown = ({ visible}) => {
    return (
        <Menu
            open={visible}
            style={{ display: visible ? 'block' : 'none' }} // Control visibility
        >
            <MenuItem>Profile</MenuItem>
            <MenuItem>Settings</MenuItem>
            <MenuItem>Logout</MenuItem>
        </Menu>
    );
};


export default ProfileDropdown;