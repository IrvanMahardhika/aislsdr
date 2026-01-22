import { Lead, LeadCreate } from '../types/lead';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const leadsApi = {
  getAll: async (params?: {
    skip?: number;
    limit?: number;
    name?: string;
    email?: string;
    company?: string;
    industry?: string;
    headcount?: string;
  }): Promise<Lead[]> => {
    const queryParams = new URLSearchParams();
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          queryParams.append(key, String(value));
        }
      });
    }
    
    const response = await fetch(`${API_BASE_URL}/leads?${queryParams.toString()}`);
    if (!response.ok) {
      throw new Error('Failed to fetch leads');
    }
    return response.json();
  },

  create: async (lead: LeadCreate): Promise<Lead> => {
    const response = await fetch(`${API_BASE_URL}/leads`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(lead),
    });
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to create lead');
    }
    return response.json();
  },

  createMultiple: async (leads: LeadCreate[]): Promise<Lead[]> => {
    const promises = leads.map(lead => leadsApi.create(lead));
    return Promise.all(promises);
  },
};

export const industryApi = {
  getOptions: async (): Promise<string[]> => {
    const response = await fetch(`${API_BASE_URL}/industry/options`);
    if (!response.ok) {
      throw new Error('Failed to fetch industry options');
    }
    return response.json();
  },
};

export const headcountApi = {
  getOptions: async (): Promise<string[]> => {
    const response = await fetch(`${API_BASE_URL}/headcount/options`);
    if (!response.ok) {
      throw new Error('Failed to fetch headcount options');
    }
    return response.json();
  },
};