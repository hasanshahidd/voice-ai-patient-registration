/**
 * API Client
 * Handles all HTTP requests to the backend API
 */

const API = {
  /**
   * Generic fetch wrapper with error handling
   */
  async request(endpoint, options = {}) {
    const url = `${CONFIG.API_BASE_URL}${endpoint}`;
    
    try {
      const response = await fetch(url, {
        headers: {
          'Content-Type': 'application/json',
          ...options.headers
        },
        ...options
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || data.error || 'Request failed');
      }

      return data;
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  },

  /**
   * Check system health
   */
  async checkHealth() {
    return await this.request(CONFIG.ENDPOINTS.health);
  },

  /**
   * Get all patients with optional filters
   */
  async getPatients(filters = {}) {
    const queryParams = new URLSearchParams();
    
    if (filters.last_name) {
      queryParams.append('last_name', filters.last_name);
    }
    if (filters.phone_number) {
      queryParams.append('phone_number', filters.phone_number);
    }
    if (filters.date_of_birth) {
      queryParams.append('date_of_birth', filters.date_of_birth);
    }

    const endpoint = queryParams.toString() 
      ? `${CONFIG.ENDPOINTS.patients}?${queryParams}`
      : CONFIG.ENDPOINTS.patients;

    return await this.request(endpoint);
  },

  /**
   * Get single patient by ID
   */
  async getPatient(patientId) {
    return await this.request(`${CONFIG.ENDPOINTS.patients}/${patientId}`);
  },

  /**
   * Create new patient
   */
  async createPatient(patientData) {
    return await this.request(CONFIG.ENDPOINTS.patients, {
      method: 'POST',
      body: JSON.stringify(patientData)
    });
  },

  /**
   * Update patient
   */
  async updatePatient(patientId, updates) {
    return await this.request(`${CONFIG.ENDPOINTS.patients}/${patientId}`, {
      method: 'PUT',
      body: JSON.stringify(updates)
    });
  },

  /**
   * Delete patient
   */
  async deletePatient(patientId) {
    return await this.request(`${CONFIG.ENDPOINTS.patients}/${patientId}`, {
      method: 'DELETE'
    });
  },

  /**
   * Get Vapi status
   */
  async getVapiStatus() {
    return await this.request(CONFIG.ENDPOINTS.vapiStatus);
  }
};
