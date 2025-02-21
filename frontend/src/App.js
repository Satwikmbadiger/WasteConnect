import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import PickupScheduler from './components/PickupScheduler';
import EcoPoints from './components/EcoPoints';
import Marketplace from './components/Marketplace';
import Statistics from './components/Statistics';

function App() {
  return (
    <Router>
      <div className="App">
        <Switch>
          <Route path="/" exact component={Dashboard} />
          <Route path="/schedule" component={PickupScheduler} />
          <Route path="/ecopoints" component={EcoPoints} />
          <Route path="/marketplace" component={Marketplace} />
          <Route path="/statistics" component={Statistics} />
        </Switch>
      </div>
    </Router>
  );
}

export default App;