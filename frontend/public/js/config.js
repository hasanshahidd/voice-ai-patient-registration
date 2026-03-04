/**
 * Configuration
 * Update API_BASE_URL with your deployed backend URL
 */

const CONFIG = {
  // Connected to Railway Backend
  API_BASE_URL: 'https://voice-ai-patient-registration-production.up.railway.app',
  
  // Vapi phone number
  PHONE_NUMBER: '+1 (276) 582-5544',
  
  // API endpoints
  ENDPOINTS: {
    health: '/health',
    patients: '/api/patients',
    vapiStatus: '/api/vapi/status'
  }
};

// Export for other modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = CONFIG;
}
