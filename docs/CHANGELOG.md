# Changelog

All notable changes to the Voice AI Agent Patient Registration System will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.3] - 2026-03-04

### Fixed
- Fixed backend README documentation (was incorrectly showing Node.js/Express instead of Python/FastAPI)
- Updated main README with live production URLs and phone number

### Changed
- Updated frontend phone number display to +1 (276) 582-5544
- Removed fake dashboard statistics (Appointments Today, Call History, Insurance Claims)
- Simplified dashboard to show only real patient gender statistics
- Configured Railway frontend service with proper root directory

### Deployment
- Frontend successfully deployed to Railway with Python simple HTTP server
- Backend running at: https://voice-ai-patient-registration-production.up.railway.app
- Phone number active: +1 (276) 582-5544

## [1.0.2] - 2026-03-03

### Added
- Complete TESTING_WORKFLOW.md documentation
- PRE_DEPLOYMENT_TEST_CHECKLIST.md for deployment validation
- LOCAL_TEST_RESULTS.md with actual test outputs
- CRITICAL_ITEMS_AUDIT.md for production readiness

### Changed
- Improved error handling in Vapi webhook endpoint
- Enhanced patient validation logic
- Updated API response formats for consistency

## [1.0.1] - 2026-03-02

### Added
- Docker support for frontend service
- Railway deployment configurations (railway.json)
- DEPLOYMENT_PLAN.md with step-by-step guide

### Changed
- Migrated frontend from Vite to simple Python HTTP server for better deployment compatibility
- Simplified frontend build process (no build step required)

### Fixed
- CORS configuration for production deployment
- Environment variable handling in backend

## [1.0.0] - 2026-03-01

### Added
- Initial release of Voice AI Agent Patient Registration System
- FastAPI backend with REST API endpoints
- PostgreSQL database with proper schema and constraints
- Vapi.ai webhook integration for voice calls
- Simple HTML/CSS/JS frontend with dashboard
- Complete documentation (README, BUSINESS_OVERVIEW, TECHNICAL_EXPLANATION)
- Local testing capabilities with seed data
- VAPI_SETUP.md guide for voice AI configuration

### Features
- Voice-based patient demographic registration
- Real-time duplicate detection by phone number
- Confirmation flow before saving patient data
- Web dashboard for viewing patient records
- Gender-based patient statistics
- RESTful API with full CRUD operations
- Health check endpoints
- Comprehensive error handling and validation

### Technical Stack
- Backend: Python 3.9+, FastAPI, SQLAlchemy, Pydantic
- Database: PostgreSQL 14+
- Frontend: Vanilla HTML/CSS/JavaScript
- Voice AI: Vapi.ai + OpenAI GPT-4o-mini
- Deployment: Railway (backend + frontend + database)
- Server: Uvicorn (backend), Python SimpleHTTPServer (frontend)

---

## Version History Summary

- **1.0.3** - Production polish, documentation fixes, frontend cleanup
- **1.0.2** - Testing documentation, production readiness audit
- **1.0.1** - Deployment improvements, Docker support
- **1.0.0** - Initial production-ready release
