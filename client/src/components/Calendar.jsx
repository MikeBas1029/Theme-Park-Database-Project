// CalendarComponent.js
import React from "react";
import FullCalendar from "@fullcalendar/react";
import dayGridPlugin from "@fullcalendar/daygrid";
import interactionPlugin from "@fullcalendar/interaction"; // Import the interaction plugin

const CalendarComponent = ({ onDateSelect }) => {
	return (
		<FullCalendar
			plugins={[dayGridPlugin, interactionPlugin]}
			initialView="dayGridMonth"
			selectable={true} // Enable selection
			select={(info) => onDateSelect(new Date(info.start))} // Pass the selected date
			headerToolbar={{
				left: "prev,next today",
				center: "title",
				right: "dayGridMonth",
			}}
			height="auto"
		/>
	);
};

export default CalendarComponent;
