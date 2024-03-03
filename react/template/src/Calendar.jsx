import { useEffect, useState } from 'react';
import PropTypes from 'prop-types';
import './CalendarStyles.css';

const WeekLoadBar = ({ dailyHours }) => {
    const maxHoursInDay = 24; // Maximum hours in a day for scaling
    return (
        <div style={{
            display: 'flex',
            flexDirection: 'row', // Adjust to row for horizontal layout
            justifyContent: 'center', // Center items horizontally
            flexWrap: 'wrap', // Wrap items to next line if not enough space
            gap: '10px',
            padding: '20px',
            backgroundColor: 'transparent',
            borderRadius: '10px',
            maxWidth: '600px', // Set a max width for the container
            margin: 'auto', // Center the container
            height: '60dvh',
          }}>
            {Object.entries(dailyHours).map(([day, hours]) => (
                <div key={day} style={{
                    display: 'flex',
                    alignItems: 'center',
                    flexDirection: 'row',
                    width: "95%",
                    justifyContent: 'space-between'
                }} className="dayContainer">
                    <span className='displayHeaderTitle' style={{
                    fontSize: '14px',
                    whiteSpace: 'nowrap'
                    }}>{day}</span>
                    <div style={{
                    width: '60%',
                    height: '50%',
                    backgroundColor: '#fff',
                    borderRadius: '10px',
                    position: 'relative',
                    display: 'flex',
                    flexDirection: 'row',
                    justifyContent: 'space-between'
                    }} title={`${hours.toFixed(2)} hours`}>
                    <div className="barAnimation" style={{
                        position: 'absolute',
                        left: 0,
                        top: 0,
                        width: `${(hours / maxHoursInDay) * 100}%`,
                        height: '100%',
                        backgroundImage: 'linear-gradient(90deg, #d19fff 0%, #67b3ff 100%)',
                        borderRadius: '5px',
                        boxShadow: '0 2px 4px rgba(0,0,0,0.2)',
                        backdropFilter: 'blur(10px)',
                        opacity: 0.8,
                        justifyContent: 'center',
                        display: 'flex',
                        alignItems: 'center',
                    }} />
                    <div style={{
                    fontSize: '14px',
                    position: 'absolute',
                    top: '2px',
                    right: '-32px',
                    color: '#333',
                    whiteSpace: 'nowrap',
                    fontStyle: 'italic',
                    }}>{Math.round(hours / maxHoursInDay * 100)}%</div>
                    </div>
                </div>
                ))}
            </div>
    );
  };
  
WeekLoadBar.propTypes = {
    dailyHours: PropTypes.object.isRequired,
};

const MyCalendar = () => {
    const [events, setEvents] = useState({
        "items": [
            {
              "id": "event1abc",
              "summary": "Team Meeting",
              "description": "Monthly team meeting to discuss project progress and milestones.",
              "location": "Conference Room 1",
              "start": {
                "dateTime": "2024-03-01T09:00:00-07:00",
                "timeZone": "America/Los_Angeles"
              },
              "end": {
                "dateTime": "2024-03-01T10:00:00-07:00",
                "timeZone": "America/Los_Angeles"
              },
              "attendees": [
                {"email": "member1@example.com", "responseStatus": "accepted"},
                {"email": "member2@example.com", "responseStatus": "declined"},
                {"email": "member3@example.com", "responseStatus": "needsAction"}
              ],
              "created": "2024-02-20T12:00:00.000Z",
              "updated": "2024-02-25T14:00:00.000Z"
            },
            {
              "id": "event2xyz",
              "summary": "Client Presentation",
              "description": "Presenting the new product features to the client.",
              "location": "Client's Office",
              "start": {
                "dateTime": "2024-03-05T14:00:00-07:00",
                "timeZone": "America/Los_Angeles"
              },
              "end": {
                "dateTime": "2024-03-05T15:30:00-07:00",
                "timeZone": "America/Los_Angeles"
              },
              "attendees": [
                {"email": "client@example.com", "responseStatus": "accepted"},
                {"email": "sales@example.com", "responseStatus": "accepted"}
              ],
              "created": "2024-02-22T08:30:00.000Z",
              "updated": "2024-02-26T09:45:00.000Z"
            },
            {
              "id": "xyz",
              "summary": "Client Presentation",
              "description": "Presenting the new product features to the client.",
              "location": "Client's Office",
              "start": {
                "dateTime": "2024-03-05T14:00:00-07:00",
                "timeZone": "America/Los_Angeles"
              },
              "end": {
                "dateTime": "2024-03-05T15:30:00-07:00",
                "timeZone": "America/Los_Angeles"
              },
              "attendees": [
                {"email": "client@example.com", "responseStatus": "accepted"},
                {"email": "sales@example.com", "responseStatus": "accepted"}
              ],
              "created": "2024-02-22T08:30:00.000Z",
              "updated": "2024-02-26T09:45:00.000Z"
            },
            {
                "id": "xyzz",
                "summary": "Client Presentation",
                "description": "Presenting the new product features to the client.",
                "location": "Client's Office",
                "start": {
                  "dateTime": "2024-03-05T14:00:00-07:00",
                  "timeZone": "America/Los_Angeles"
                },
                "end": {
                  "dateTime": "2024-03-05T15:30:00-07:00",
                  "timeZone": "America/Los_Angeles"
                },
                "attendees": [
                  {"email": "client@example.com", "responseStatus": "accepted"},
                  {"email": "sales@example.com", "responseStatus": "accepted"}
                ],
                "created": "2024-02-22T08:30:00.000Z",
                "updated": "2024-02-26T09:45:00.000Z"
            },
            {
                "id": "xyz",
                "summary": "Client Presentation",
                "description": "Presenting the new product features to the client.",
                "location": "Client's Office",
                "start": {
                  "dateTime": "2024-03-02T14:00:00-07:00",
                  "timeZone": "America/Los_Angeles"
                },
                "end": {
                  "dateTime": "2024-03-02T15:30:00-07:00",
                  "timeZone": "America/Los_Angeles"
                },
                "attendees": [
                  {"email": "client@example.com", "responseStatus": "accepted"},
                  {"email": "sales@example.com", "responseStatus": "accepted"}
                ],
                "created": "2024-02-22T08:30:00.000Z",
                "updated": "2024-02-26T09:45:00.000Z"
              },
              {
                "id": "xyz",
                "summary": "Client Presentation",
                "description": "Presenting the new product features to the client.",
                "location": "Client's Office",
                "start": {
                  "dateTime": "2024-03-06T14:00:00-07:00",
                  "timeZone": "America/Los_Angeles"
                },
                "end": {
                  "dateTime": "2024-03-06T20:30:00-07:00",
                  "timeZone": "America/Los_Angeles"
                },
                "attendees": [
                  {"email": "client@example.com", "responseStatus": "accepted"},
                  {"email": "sales@example.com", "responseStatus": "accepted"}
                ],
                "created": "2024-02-22T08:30:00.000Z",
                "updated": "2024-02-26T09:45:00.000Z"
              }
          ]
      });
      const [dailyHours, setDaily] = useState({ Monday: 0, Tuesday: 0, Wednesday: 0, Thursday: 0, Friday: 0, Saturday: 0, Sunday: 0 });
    /**useEffect(() => {
        const fetchEvents = async () => {
            try {
              const response = await fetch('http://127.0.0.1:5000/get_calendar_events');
              if (!response.ok) {
                throw new Error('Network response was not ok');
              }
              const eventData = await response.json();
              const formattedEvents = eventData.items.map(event => ({
                ...event,
                start: new Date(event.start.dateTime),
                end: new Date(event.end.dateTime)
              }));
              setEvents(formattedEvents);
              console.log(formattedEvents);
        
                
                
            } catch (error) {
              console.error("Failed to fetch events:", error);
            }
          };
        fetchEvents();
        console.log(dailyHours)
    }, []);
      **/
     useEffect(() => {
        setDaily({ Monday: 0, Tuesday: 0, Wednesday: 0, Thursday: 0, Friday: 0, Saturday: 0, Sunday: 0 });
        events.items.forEach(event => {
            const start = new Date(event.start.dateTime);
            const end = new Date(event.end.dateTime);
            const durationHours = (end - start) / (1000 * 60 * 60); // Convert duration from milliseconds to hours
        
            const dayOfWeek = start.toLocaleString('en-US', { weekday: 'long' });
            setDaily(prev => ({
              ...prev,
              [dayOfWeek]: prev[dayOfWeek] + durationHours
            }));
            });
        }
    , []);
    return (
        <div>
        {/* Render your WeekLoadBar component */}
        <WeekLoadBar dailyHours={dailyHours} />
        </div>
    );
};

export default MyCalendar;