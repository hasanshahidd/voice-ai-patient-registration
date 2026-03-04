/**
 * Configuration
 * Update API_BASE_URL with your deployed backend URL
 */

const CONFIG = {
  // For LOCAL testing (NOW): Use localhost
  API_BASE_URL: 'http://localhost:8001',
  
  // For PRODUCTION testing (AFTER deployment): Replace with your Railway URL
  // API_BASE_URL: 'https://your-app-production.up.railway.app',
  
  // Or use environment-based config
  // API_BASE_URL: window.location.hostname === 'localhost' 
  //   ? 'http://localhost:3000' 
  //   : 'https://your-backend.railway.app',
  
  // Vapi phone number (update after provisioning)
  PHONE_NUMBER: '+1-XXX-XXX-XXXX',
  
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
