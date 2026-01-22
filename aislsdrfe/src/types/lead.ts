export interface Lead {
  id: number;
  name: string;
  job_title?: string;
  phone_number?: string;
  company?: string;
  email: string;
  headcount?: number;
  industry?: string;
}

export interface LeadCreate {
  name: string;
  job_title?: string;
  phone_number?: string;
  company?: string;
  email: string;
  headcount?: number;
  industry?: string;
}