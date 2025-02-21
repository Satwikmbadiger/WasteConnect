import React, { useState } from 'react';

const PickupScheduler = () => {
    const [pickupDate, setPickupDate] = useState('');
    const [pickupTime, setPickupTime] = useState('');
    const [message, setMessage] = useState('');

    const handleSchedulePickup = async () => {
        // Logic to schedule the pickup using API call
        try {
            const response = await fetch('/api/schedule-pickup', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ date: pickupDate, time: pickupTime }),
            });

            if (response.ok) {
                setMessage('Pickup scheduled successfully!');
            } else {
                setMessage('Failed to schedule pickup. Please try again.');
            }
        } catch (error) {
            setMessage('An error occurred. Please try again later.');
        }
    };

    return (
        <div>
            <h2>Schedule Waste Pickup</h2>
            <input
                type="date"
                value={pickupDate}
                onChange={(e) => setPickupDate(e.target.value)}
            />
            <input
                type="time"
                value={pickupTime}
                onChange={(e) => setPickupTime(e.target.value)}
            />
            <button onClick={handleSchedulePickup}>Schedule Pickup</button>
            {message && <p>{message}</p>}
        </div>
    );
};

export default PickupScheduler;