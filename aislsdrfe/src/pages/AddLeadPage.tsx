import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { LeadCreate } from '../types/lead';
import { leadsApi } from '../services/api';
import { LeadForm } from '../components/LeadForm/LeadForm';
import './AddLeadPage.css';

export const AddLeadPage: React.FC = () => {
  const navigate = useNavigate();
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  const handleSubmit = async (lead: LeadCreate) => {
    try {
      await leadsApi.create(lead);
      setSuccessMessage('Lead created successfully!');
      setTimeout(() => {
        navigate('/leads');
      }, 1500);
    } catch (error) {
      throw error; // Let the form handle the error
    }
  };

  return (
    <div className="add-lead-page">
      <div className="page-header">
        <h1>Add New Lead</h1>
        <button
          className="btn-secondary"
          onClick={() => navigate('/leads')}
        >
          Back to Leads
        </button>
      </div>

      {successMessage && (
        <div className="success-banner">{successMessage}</div>
      )}

      <LeadForm onSubmit={handleSubmit} onCancel={() => navigate('/leads')} />
    </div>
  );
};