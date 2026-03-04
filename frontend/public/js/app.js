// Global state
let allPatients = [];
let filteredPatients = [];
let currentFilter = { gender: 'all', language: '' };
let currentView = 'dashboard';

// Initialize app
document.addEventListener('DOMContentLoaded', async () => {
    initializeNavigation();
    await loadPatients();
    updateStats();
});

// Initialize navigation
function initializeNavigation() {
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach((item, index) => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            
            // Remove active class from all items
            navItems.forEach(nav => nav.classList.remove('active'));
            
            // Add active class to clicked item
            item.classList.add('active');
            
            // Get view name from the span text
            const viewName = item.querySelector('span:not(.badge)').textContent.toLowerCase();
            switchView(viewName);
        });
    });
}

// Switch between views
function switchView(view) {
    currentView = view;
    const mainContent = document.querySelector('.main-content');
    const topbarTitle = document.querySelector('.topbar-left h1');
    const topbarSubtitle = document.querySelector('.topbar-left .subtitle');
    const statsGrid = document.querySelector('.stats-grid');
    const searchSection = document.querySelector('.search-section');
    const tableCard = document.querySelector('.table-card');
    const comingSoon = document.querySelector('.coming-soon');
    
    // Remove coming soon if it exists
    if (comingSoon) {
        comingSoon.remove();
    }
    
    switch(view) {
        case 'dashboard':
            topbarTitle.textContent = 'Patient Dashboard';
            topbarSubtitle.textContent = 'Manage and view all registered patients';
            if (statsGrid) statsGrid.style.display = 'grid';
            if (searchSection) searchSection.style.display = 'block';
            if (tableCard) tableCard.style.display = 'block';
            break;
        case 'patients':
            topbarTitle.textContent = 'All Patients';
            topbarSubtitle.textContent = 'Complete list of registered patients';
            if (statsGrid) statsGrid.style.display = 'none';
            if (searchSection) searchSection.style.display = 'block';
            if (tableCard) tableCard.style.display = 'block';
            break;
        case 'appointments':
            topbarTitle.textContent = 'Appointments';
            topbarSubtitle.textContent = 'View and manage patient appointments';
            if (statsGrid) statsGrid.style.display = 'none';
            if (searchSection) searchSection.style.display = 'none';
            if (tableCard) tableCard.style.display = 'none';
            showComingSoon('Appointments');
            break;
        case 'history':
            topbarTitle.textContent = 'Patient History';
            topbarSubtitle.textContent = 'Review past patient interactions';
            if (statsGrid) statsGrid.style.display = 'none';
            if (searchSection) searchSection.style.display = 'none';
            if (tableCard) tableCard.style.display = 'none';
            showComingSoon('History');
            break;
    }
}

// Show coming soon message
function showComingSoon(feature) {
    if (!document.querySelector('.coming-soon')) {
        const comingSoonDiv = document.createElement('div');
        comingSoonDiv.className = 'coming-soon';
        comingSoonDiv.innerHTML = `
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" style="width: 80px; height: 80px; color: var(--primary);">
                <circle cx="12" cy="12" r="10" stroke-width="2"/>
                <polyline points="12 6 12 12 16 14" stroke-width="2"/>
            </svg>
            <h2>${feature} Coming Soon</h2>
            <p>This feature is under development and will be available soon.</p>
            <button class="btn-primary" onclick="switchView('dashboard')">Back to Dashboard</button>
        `;
        const mainContent = document.querySelector('.main-content');
        // Insert at the end of main-content
        mainContent.appendChild(comingSoonDiv);
    }
}

// Load patients from API
async function loadPatients() {
    try {
        const response = await API.getPatients();
        if (response.data) {
            allPatients = response.data;
            filteredPatients = [...allPatients];
            renderPatients(filteredPatients);
            updateStats();
        }
    } catch (error) {
        console.error('Error loading patients:', error);
        showToast('Failed to load patients', 'error');
    }
}

// Render patients table
function renderPatients(patients) {
    const tbody = document.getElementById('patientTableBody');
    
    if (!patients || patients.length === 0) {
        tbody.innerHTML = `
            <tr class="empty-state">
                <td colspan="9">
                    <div class="loading-content">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" style="width: 64px; height: 64px; color: var(--gray-300);">
                            <circle cx="12" cy="12" r="10" stroke-width="2"/>
                            <path d="M12 6v6l4 2" stroke-width="2"/>
                        </svg>
                        <span style="font-size: 18px; font-weight: 600; color: var(--gray-400);">No patients found</span>
                        <span style="font-size: 14px; color: var(--gray-400);">Add your first patient to get started</span>
                    </div>
                </td>
            </tr>
        `;
        return;
    }

    tbody.innerHTML = patients.map((patient, index) => `
        <tr>
            <td>
                <label class="checkbox">
                    <input type="checkbox" data-patient-id="${patient.patient_id}">
                    <span class="checkmark"></span>
                </label>
            </td>
            <td>
                <div>
                    <div class="patient-name">${escapeHtml(patient.first_name)} ${escapeHtml(patient.last_name)}</div>
                    <div class="patient-id">#${patient.patient_id.substring(0, 8)}</div>
                </div>
            </td>
            <td>${formatDate(patient.date_of_birth)}</td>
            <td>${escapeHtml(patient.sex)}</td>
            <td>
                <div>
                    <div>${formatPhone(patient.phone_number)}</div>
                    ${patient.email ? `<div style="font-size: 12px; color: var(--gray-500);">${escapeHtml(patient.email)}</div>` : ''}
                </div>
            </td>
            <td>
                <div>
                    <div>${escapeHtml(patient.city)}, ${escapeHtml(patient.state)}</div>
                    <div style="font-size: 12px; color: var(--gray-500);">${escapeHtml(patient.zip_code)}</div>
                </div>
            </td>
            <td>
                ${patient.insurance_provider 
                    ? `<div>
                        <div>${escapeHtml(patient.insurance_provider)}</div>
                        <div style="font-size: 12px; color: var(--gray-500);">${escapeHtml(patient.insurance_member_id || 'N/A')}</div>
                       </div>`
                    : '<span style="color: var(--gray-400);">No Insurance</span>'}
            </td>
            <td>
                <span class="status-badge status-active">Active</span>
            </td>
            <td>
                <div class="action-buttons">
                    <button class="action-btn" onclick="viewPatient('${patient.patient_id}')" title="View Details">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                            <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" stroke-width="2"/>
                            <circle cx="12" cy="12" r="3" stroke-width="2"/>
                        </svg>
                    </button>
                    <button class="action-btn" onclick="editPatient('${patient.patient_id}')" title="Edit">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" stroke-width="2"/>
                            <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" stroke-width="2"/>
                        </svg>
                    </button>
                    <button class="action-btn" onclick="deletePatient('${patient.patient_id}')" title="Delete" style="color: var(--danger);">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                            <path d="M3 6h18M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" stroke-width="2"/>
                        </svg>
                    </button>
                </div>
            </td>
        </tr>
    `).join('');

    // Update counts
    document.getElementById('showing-count').textContent = patients.length;
    document.getElementById('total-count').textContent = allPatients.length;
}

// Update statistics
function updateStats() {
    const total = allPatients.length;
    const today = new Date().toISOString().split('T')[0];
    const todayCount = allPatients.filter(p => 
        p.created_at && p.created_at.startsWith(today)
    ).length;
    const maleCount = allPatients.filter(p => p.sex === 'Male').length;
    const femaleCount = allPatients.filter(p => p.sex === 'Female').length;

    document.getElementById('stat-total').textContent = total;
    document.getElementById('stat-today').textContent = todayCount;
    document.getElementById('stat-male').textContent = maleCount;
    document.getElementById('stat-female').textContent = femaleCount;
    document.getElementById('patient-count').textContent = total;
}

// Search functionality
function handleSearch() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase().trim();
    
    if (!searchTerm) {
        filteredPatients = allPatients.filter(p => 
            matchesFilters(p, currentFilter)
        );
    } else {
        filteredPatients = allPatients.filter(patient => {
            const matchesSearch = 
                patient.first_name?.toLowerCase().includes(searchTerm) ||
                patient.last_name?.toLowerCase().includes(searchTerm) ||
                patient.phone_number?.includes(searchTerm) ||
                patient.patient_id?.toLowerCase().includes(searchTerm) ||
                patient.email?.toLowerCase().includes(searchTerm);
            
            return matchesSearch && matchesFilters(patient, currentFilter);
        });
    }
    
    renderPatients(filteredPatients);
}

// Clear search
function clearSearch() {
    document.getElementById('searchInput').value = '';
    handleSearch();
}

// Filter by gender
function filterByGender(gender) {
    currentFilter.gender = gender;
    
    // Update active button
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
    
    applyFilters();
}

// Apply all filters
function applyFilters() {
    const languageFilter = document.getElementById('languageFilter').value;
    currentFilter.language = languageFilter;
    
    filteredPatients = allPatients.filter(patient => 
        matchesFilters(patient, currentFilter)
    );
    
    renderPatients(filteredPatients);
}

// Check if patient matches filters
function matchesFilters(patient, filters) {
    const matchesGender = filters.gender === 'all' || patient.sex === filters.gender;
    const matchesLanguage = !filters.language || patient.preferred_language === filters.language;
    return matchesGender && matchesLanguage;
}

// View patient details
async function viewPatient(patientId) {
    try {
        const response = await API.getPatient(patientId);
        if (response.data) {
            showPatientModal(response.data);
        }
    } catch (error) {
        console.error('Error loading patient:', error);
        showToast('Failed to load patient details', 'error');
    }
}

// Show patient modal
function showPatientModal(patient) {
    const modal = document.getElementById('patientModal');
    const modalTitle = document.getElementById('modalTitle');
    const modalBody = document.getElementById('modalBody');

    modalTitle.textContent = `${patient.first_name} ${patient.last_name}`;
    
    modalBody.innerHTML = `
        <div class="detail-grid">
            <div class="detail-section">
                <h4 class="detail-section-title">Personal Information</h4>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px;">
                    <div class="detail-item">
                        <span class="detail-label">Patient ID</span>
                        <span class="detail-value">${patient.patient_id}</span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Full Name</span>
                        <span class="detail-value">${patient.first_name} ${patient.last_name}</span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Date of Birth</span>
                        <span class="detail-value">${formatDate(patient.date_of_birth)}</span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Gender</span>
                        <span class="detail-value">${patient.sex}</span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Preferred Language</span>
                        <span class="detail-value">${patient.preferred_language || 'Not specified'}</span>
                    </div>
                </div>
            </div>

            <div class="detail-section">
                <h4 class="detail-section-title">Contact Information</h4>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px;">
                    <div class="detail-item">
                        <span class="detail-label">Phone Number</span>
                        <span class="detail-value">${formatPhone(patient.phone_number)}</span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Email</span>
                        <span class="detail-value">${patient.email || 'Not provided'}</span>
                    </div>
                </div>
            </div>

            <div class="detail-section">
                <h4 class="detail-section-title">Address</h4>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px;">
                    <div class="detail-item" style="grid-column: 1 / -1;">
                        <span class="detail-label">Street Address</span>
                        <span class="detail-value">${patient.address_line_1}</span>
                        ${patient.address_line_2 ? `<span class="detail-value">${patient.address_line_2}</span>` : ''}
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">City</span>
                        <span class="detail-value">${patient.city}</span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">State</span>
                        <span class="detail-value">${patient.state}</span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">ZIP Code</span>
                        <span class="detail-value">${patient.zip_code}</span>
                    </div>
                </div>
            </div>

            ${patient.insurance_provider ? `
                <div class="detail-section">
                    <h4 class="detail-section-title">Insurance Information</h4>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px;">
                        <div class="detail-item">
                            <span class="detail-label">Provider</span>
                            <span class="detail-value">${patient.insurance_provider}</span>
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">Member ID</span>
                            <span class="detail-value">${patient.insurance_member_id || 'Not provided'}</span>
                        </div>
                    </div>
                </div>
            ` : ''}

            ${patient.emergency_contact_name ? `
                <div class="detail-section">
                    <h4 class="detail-section-title">Emergency Contact</h4>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px;">
                        <div class="detail-item">
                            <span class="detail-label">Contact Name</span>
                            <span class="detail-value">${patient.emergency_contact_name}</span>
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">Contact Phone</span>
                            <span class="detail-value">${formatPhone(patient.emergency_contact_phone)}</span>
                        </div>
                    </div>
                </div>
            ` : ''}

            <div class="detail-section">
                <h4 class="detail-section-title">Registration Details</h4>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px;">
                    <div class="detail-item">
                        <span class="detail-label">Created At</span>
                        <span class="detail-value">${formatDateTime(patient.created_at)}</span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Last Updated</span>
                        <span class="detail-value">${formatDateTime(patient.updated_at)}</span>
                    </div>
                </div>
            </div>
        </div>
    `;

    modal.classList.add('active');
}

// Close modal
function closeModal() {
    const modal = document.getElementById('patientModal');
    modal.classList.remove('active');
}

// Edit patient
function editPatient(patientId) {
    showToast('Edit functionality coming soon!', 'warning');
}

// Delete patient
async function deletePatient(patientId) {
    if (!confirm('Are you sure you want to delete this patient?')) {
        return;
    }

    try {
        await API.deletePatient(patientId);
        showToast('Patient deleted successfully', 'success');
        await loadPatients();
    } catch (error) {
        console.error('Error deleting patient:', error);
        showToast('Failed to delete patient', 'error');
    }
}

// Refresh data
async function refreshData() {
    showToast('Refreshing data...', 'info');
    await loadPatients();
    showToast('Data refreshed successfully', 'success');
}

// Toggle all rows
function toggleAllRows() {
    const checkbox = event.target;
    const checkboxes = document.querySelectorAll('.patient-table tbody input[type="checkbox"]');
    checkboxes.forEach(cb => cb.checked = checkbox.checked);
}

// Open add patient modal
function openAddModal() {
    showToast('Add patient form coming soon!', 'info');
}

// Export data
function exportData() {
    const csv = convertToCSV(allPatients);
    downloadCSV(csv, 'patients.csv');
    showToast('Data exported successfully', 'success');
}

// Convert to CSV
function convertToCSV(data) {
    const headers = ['ID', 'First Name', 'Last Name', 'DOB', 'Gender', 'Phone', 'Email', 'City', 'State'];
    const rows = data.map(p => [
        p.patient_id,
        p.first_name,
        p.last_name,
        p.date_of_birth,
        p.sex,
        p.phone_number,
        p.email || '',
        p.city,
        p.state
    ]);
    
    return [headers, ...rows].map(row => row.join(',')).join('\n');
}

// Download CSV
function downloadCSV(csv, filename) {
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    window.URL.revokeObjectURL(url);
}

// Show toast notification
function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast ${type} active`;
    
    setTimeout(() => {
        toast.classList.remove('active');
    }, 3000);
}

// Utility functions
function formatDate(dateString) {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
}

function formatDateTime(dateString) {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleString('en-US', { 
        month: 'short', 
        day: 'numeric', 
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function formatPhone(phoneNumber) {
    if (!phoneNumber) return 'N/A';
    const cleaned = phoneNumber.replace(/\D/g, '');
    const match = cleaned.match(/^(\d{3})(\d{3})(\d{4})$/);
    if (match) {
        return `(${match[1]}) ${match[2]}-${match[3]}`;
    }
    return phoneNumber;
}

function escapeHtml(unsafe) {
    if (!unsafe) return '';
    return unsafe
        .toString()
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

// Close modal on escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        closeModal();
    }
});
