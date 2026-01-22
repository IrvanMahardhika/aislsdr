import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { LeadsListPage } from './pages/LeadsListPage';
import { AddLeadPage } from './pages/AddLeadPage';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Navigate to="/leads" replace />} />
          <Route path="/leads" element={<LeadsListPage />} />
          <Route path="/add-lead" element={<AddLeadPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;