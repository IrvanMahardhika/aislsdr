import React from 'react';
import { Lead } from '../../types/lead';
import './LeadsTable.css';

interface LeadsTableProps {
  leads: Lead[];
  isLoading?: boolean;
}

export const LeadsTable: React.FC<LeadsTableProps> = ({ leads, isLoading }) => {
  if (isLoading) {
    return <div className="loading">Loading leads...</div>;
  }

  if (leads.length === 0) {
    return <div className="empty-state">No leads found</div>;
  }

  return (
    <div className="leads-table-container">
      <table className="leads-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Email</th>
            <th>Job Title</th>
            <th>Company</th>
            <th>Phone</th>
            <th>Industry</th>
            <th>Headcount</th>
          </tr>
        </thead>
        <tbody>
          {leads.map((lead) => (
            <tr key={lead.id}>
              <td>{lead.id}</td>
              <td>{lead.name}</td>
              <td>{lead.email}</td>
              <td>{lead.job_title || '-'}</td>
              <td>{lead.company || '-'}</td>
              <td>{lead.phone_number || '-'}</td>
              <td>{lead.industry || '-'}</td>
              <td>{lead.headcount || '-'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};