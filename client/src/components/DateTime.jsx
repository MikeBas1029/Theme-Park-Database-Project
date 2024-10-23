import * as React from 'react';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import TextField from '@mui/material/TextField';
import dayjs from 'dayjs';

export default function BasicDatePicker() {
  const [selectedDate, setSelectedDate] = React.useState(null);

  const handleDateChange = (newValue) => {
    setSelectedDate(newValue);
  };

  return (
    <LocalizationProvider dateAdapter={AdapterDayjs}>
      <DatePicker
        label="Date of Birth"
        value={selectedDate}
        onChange={handleDateChange}
        // Instead of renderInput, use the textField prop
        slots={{
          textField: TextField,
        }}
        // To format the output value, you may need to format it manually if necessary
      />
    </LocalizationProvider>
  );
}
