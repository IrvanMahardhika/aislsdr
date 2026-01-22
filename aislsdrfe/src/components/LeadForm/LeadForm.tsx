import React, { useState } from 'react';
import { LeadCreate } from '../../types/lead';
import './LeadForm.css';

interface LeadFormProps {
  onSubmit: (lead: LeadCreate) => Promise<void>;
  onCancel?: () => void;
  initialValues?: Partial<LeadCreate>;
}

export const LeadForm: React.FC<LeadFormProps> = ({
  onSubmit,
  onCancel,
  initialValues,
}) => {
  const [formData, setFormData] = useState<LeadCreate>({
    name: initialValues?.name || '',
    email: initialValues?.email || '',
    job_title: initialValues?.job_title || '',
    phone_number: initialValues?.phone_number || '',
    company: initialValues?.company || '',
    industry: initialValues?.industry || '',
    headcount: initialValues?.headcount,
  });

  const [errors, setErrors] = useState<Partial<Record<keyof LeadCreate, string>>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: name === 'headcount' ? (value ? parseInt(value, 10) : undefined) : value,
    }));
    // Clear error when user starts typing
    if (errors[name as keyof LeadCreate]) {
      setErrors((prev) => ({ ...prev, [name]: undefined }));
    }
  };

  const validate = (): boolean => {
    const newErrors: Partial<Record<keyof LeadCreate, string>> = {};

    if (!formData.name.trim()) {
      newErrors.name = 'Name is required';
    }

    if (!formData.email.trim()) {
      newErrors.email = 'Email is required';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newErrors.email = 'Invalid email format';
    }

    if (formData.headcount !== undefined && formData.headcount < 0) {
      newErrors.headcount = 'Headcount must be a positive number';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validate()) {
      return;
    }

    setIsSubmitting(true);
    try {
      await onSubmit(formData);
      // Reset form after successful submission
      setFormData({
        name: '',
        email: '',
        job_title: '',
        phone_number: '',
        company: '',
        industry: '',
        headcount: undefined,
      });
    } catch (error) {
      console.error('Error submitting form:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form className="lead-form" onSubmit={handleSubmit}>
      <div className="form-group">
        <label htmlFor="name">
          Name <span className="required">*</span>
        </label>
        <input
          type="text"
          id="name"
          name="name"
          value={formData.name}
          onChange={handleChange}
          className={errors.name ? 'error' : ''}
        />
        {errors.name && <span className="error-message">{errors.name}</span>}
      </div>

      <div className="form-group">
        <label htmlFor="email">
          Email <span className="required">*</span>
        </label>
        <input
          type="email"
          id="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
          className={errors.email ? 'error' : ''}
        />
        {errors.email && <span className="error-message">{errors.email}</span>}
      </div>

      <div className="form-group">
        <label htmlFor="job_title">Job Title</label>
        <input
          type="text"
          id="job_title"
          name="job_title"
          value={formData.job_title}
          onChange={handleChange}
        />
      </div>

      <div className="form-group">
        <label htmlFor="company">Company</label>
        <input
          type="text"
          id="company"
          name="company"
          value={formData.company}
          onChange={handleChange}
        />
      </div>

      <div className="form-group">
        <label htmlFor="phone_number">Phone Number</label>
        <input
          type="tel"
          id="phone_number"
          name="phone_number"
          value={formData.phone_number}
          onChange={handleChange}
        />
      </div>

      <div className="form-group">
        <label htmlFor="industry">Industry</label>
        <input
          type="text"
          id="industry"
          name="industry"
          value={formData.industry}
          onChange={handleChange}
        />
      </div>

      <div className="form-group">
        <label htmlFor="headcount">Headcount</label>
        <input
          type="number"
          id="headcount"
          name="headcount"
          value={formData.headcount || ''}
          onChange={handleChange}
          min="0"
          className={errors.headcount ? 'error' : ''}
        />
        {errors.headcount && (
          <span className="error-message">{errors.headcount}</span>
        )}
      </div>

      <div className="form-actions">
        <button type="submit" disabled={isSubmitting} className="btn-primary">
          {isSubmitting ? 'Submitting...' : 'Submit'}
        </button>
        {onCancel && (
          <button type="button" onClick={onCancel} className="btn-secondary">
            Cancel
          </button>
        )}
      </div>
    </form>
  );
};