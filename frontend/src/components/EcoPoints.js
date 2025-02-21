import React from 'react';

const EcoPoints = ({ ecoPoints }) => {
    return (
        <div className="eco-points">
            <h2>Your EcoPoints Balance</h2>
            <p>{ecoPoints} EcoPoints</p>
        </div>
    );
};

export default EcoPoints;