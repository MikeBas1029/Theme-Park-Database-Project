import { configureStore } from '@reduxjs/toolkit';
import ridesReducer from '../features/rides/ridesSlice';

const store = configureStore({
    reducer: {
        rides: ridesReducer,
    },
});

export default store;
