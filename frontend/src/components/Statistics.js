import React from 'react';

const Statistics = ({ co2Savings, wasteReduction, ecoPoints }) => {
    return (
        <div className="statistics">
            <h2>Your Environmental Impact</h2>
            <div className="statistic-item">
                <h3>CO₂ Savings</h3>
                <p>{co2Savings} kg</p>
            </div>
            <div className="statistic-item">
                <h3>Waste Reduction</h3>
                <p>{wasteReduction} kg</p>
            </div>
            <div className="statistic-item">
                <h3>EcoPoints Earned</h3>
                <p>{ecoPoints}</p>
            </div>
        </div>
    );
};

export default Statistics;