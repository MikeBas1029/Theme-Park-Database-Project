import { createSlice } from '@reduxjs/toolkit';

const initialState = {
    rides: [
        { id: 1, name: 'Roller Coaster', description: 'Fast and thrilling!', image: '/images/roller-coaster.jpg' },
        { id: 2, name: 'Ferris Wheel', description: 'A relaxing ride!', image: '/images/ferris-wheel.jpg' },
        { id: 3, name: 'Haunted House', description: 'Scary fun!', image: '/images/haunted-house.jpg' },
    ],
};

const ridesSlice = createSlice({
    name: 'rides',
    initialState,
    reducers: {},
});

export const selectRides = (state) => state.rides.rides;
export default ridesSlice.reducer;