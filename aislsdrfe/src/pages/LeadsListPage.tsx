import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Lead } from '../types/lead';
import { leadsApi } from '../services/api';
import { LeadsTable } from '../components/LeadsTable/LeadsTable';
import './LeadsListPage.css';

export const LeadsListPage: React.FC = () => {
  const [leads, setLeads] = useState<Lead[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    fetchLeads();
  }, []);

  const fetchLeads = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await leadsApi.getAll();
      setLeads(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load leads');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="leads-list-page">
      <div className="page-header">
        <h1>Leads</h1>
        <button
          className="btn-primary"
          onClick={() => navigate('/add-lead')}
        >
          Add New Lead
        </button>
      </div>

      {error && (
        <div className="error-banner">
          {error}
          <button onClick={fetchLeads}>Retry</button>
        </div>
      )}

      <LeadsTable leads={leads} isLoading={isLoading} />
    </div>
  );
};