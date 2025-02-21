import React, { useEffect, useState } from 'react';
import { getEcoPoints, getUserStatistics } from '../services/api';
import EcoPoints from './EcoPoints';
import Statistics from './Statistics';

const Dashboard = () => {
    const [ecoPoints, setEcoPoints] = useState(0);
    const [statistics, setStatistics] = useState({});

    useEffect(() => {
        const fetchData = async () => {
            const points = await getEcoPoints();
            const stats = await getUserStatistics();
            setEcoPoints(points);
            setStatistics(stats);
        };

        fetchData();
    }, []);

    return (
        <div className="dashboard">
            <h1>Your Dashboard</h1>
            <EcoPoints points={ecoPoints} />
            <Statistics data={statistics} />
        </div>
    );
};

export default Dashboard;