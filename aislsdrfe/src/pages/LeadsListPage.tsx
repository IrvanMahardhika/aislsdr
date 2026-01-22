import React, { useEffect, useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { Lead } from '../types/lead';
import { leadsApi, industryApi, headcountApi } from '../services/api';
import { LeadsTable } from '../components/LeadsTable/LeadsTable';
import './LeadsListPage.css';

export const LeadsListPage: React.FC = () => {
  const [leads, setLeads] = useState<Lead[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [industryOptions, setIndustryOptions] = useState<string[]>([]);
  const [headcountOptions, setHeadcountOptions] = useState<string[]>([]);
  const [selectedIndustry, setSelectedIndustry] = useState<string>('');
  const [selectedHeadcount, setSelectedHeadcount] = useState<string>('');
  const navigate = useNavigate();

  const fetchLeads = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const params: {
        industry?: string;
        headcount?: string;
      } = {};
      
      if (selectedIndustry) {
        params.industry = selectedIndustry;
      }
      if (selectedHeadcount) {
        params.headcount = selectedHeadcount;
      }
      
      const data = await leadsApi.getAll(params);
      setLeads(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load leads');
    } finally {
      setIsLoading(false);
    }
  }, [selectedIndustry, selectedHeadcount]);

  useEffect(() => {
    const fetchOptions = async () => {
      try {
        const [industries, headcounts] = await Promise.all([
          industryApi.getOptions(),
          headcountApi.getOptions(),
        ]);
        setIndustryOptions(industries);
        setHeadcountOptions(headcounts);
      } catch (err) {
        console.error('Failed to load filter options:', err);
      }
    };
    
    fetchOptions();
  }, []);

  useEffect(() => {
    fetchLeads();
  }, [fetchLeads]);  

  const handleIndustryChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedIndustry(e.target.value);
  };

  const handleHeadcountChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedHeadcount(e.target.value);
  };

  const clearFilters = () => {
    setSelectedIndustry('');
    setSelectedHeadcount('');
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

      <div className="filters-section">
        <div className="filter-group">
          <label htmlFor="industry-filter">Industry:</label>
          <select
            id="industry-filter"
            value={selectedIndustry}
            onChange={handleIndustryChange}
            className="filter-select"
          >
            <option value="">All Industries</option>
            {industryOptions.map((industry) => (
              <option key={industry} value={industry}>
                {industry}
              </option>
            ))}
          </select>
        </div>

        <div className="filter-group">
          <label htmlFor="headcount-filter">Headcount:</label>
          <select
            id="headcount-filter"
            value={selectedHeadcount}
            onChange={handleHeadcountChange}
            className="filter-select"
          >
            <option value="">All Headcounts</option>
            {headcountOptions.map((headcount) => (
              <option key={headcount} value={headcount}>
                {headcount}
              </option>
            ))}
          </select>
        </div>

        {(selectedIndustry || selectedHeadcount) && (
          <button
            className="btn-secondary"
            onClick={clearFilters}
          >
            Clear Filters
          </button>
        )}
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