# FinTwin Project Overview

## 1. Non-Technical Overview

FinTwin is a finance operations platform that helps teams automate reconciliation and improve control visibility across invoices, payments, GST records, and bank transactions.

### Business Purpose

- Reduce manual effort in finance operations.
- Detect discrepancies early and route them for action.
- Improve audit readiness through traceable system actions.
- Provide faster financial reporting for decision-making.

### Target Users

- Accountants
- Finance managers
- Auditors
- Admin and operations teams

### Typical User Journey

1. Upload financial documents.
2. Review extracted data and confirm records.
3. Run reconciliation matching.
4. Review and resolve generated exceptions.
5. Apply or tune business rules.
6. Use learning suggestions to improve accuracy over time.
7. Generate and export reports.

## 2. Technical Architecture

### Backend

- Framework: FastAPI
- ORM: SQLAlchemy
- Default database: SQLite
- Core style: Router + service-layer architecture
- Startup behavior: auto-creates tables from models

### Frontend

- Framework: Next.js (App Router)
- Language: TypeScript
- UI: module-based operations dashboard
- API integration: frontend proxy rewrite from `/api/*` to backend (`127.0.0.1:8000`)

### Data and Processing

- Document ingestion supports PDF, Excel, and CSV.
- Extraction pipeline includes classification, field mapping, and validation.
- OCR fallback is used for scanned PDFs.

## 3. Core Feature Modules

### 3.1 Document Processing

- Upload and classify documents.
- Extract structured data.
- Validate extracted fields.
- Confirm and persist records into finance tables.

### 3.2 Ledger Data Modules

- Vendors
- Invoices
- Payments
- GST records
- Bank transactions

### 3.3 Matching Engine

- Invoice vs payment matching
- Invoice vs GST 2A matching
- Invoice vs bank transaction matching
- Weighted confidence scoring with decision bands:
	- auto approved
	- manual review
	- rejected

### 3.4 Exception Management

- Auto-generates exceptions from weak or failed matches.
- Detects missing payments, overdue invoices, and duplicate invoices.
- Supports lifecycle actions (assign, review, resolve, archive, override, etc.).

### 3.5 Rule Engine

- Configurable IF-THEN business rules.
- Rule categories include commissions, deductions, approval workflows, and payment conditions.
- Includes activation/deactivation, priority, and execution history.

### 3.6 Learning System

- Learns normalization patterns (for example, vendor aliases).
- Captures correction feedback from user decisions.
- Suggests likely matches from historical approved patterns.
- Provides recommended scoring-weight adjustments.

### 3.7 Reporting Engine

- GST reconciliation report
- Vendor ledger report
- Outstanding payments report
- Commission summary report
- Cash flow report
- Export support for JSON, Excel, and PDF-style outputs

### 3.8 Dashboard and Monitoring

- Central KPI dashboard with module summaries.
- Audit logs for append-only action tracking.
- Activity logs for auth and user-level monitoring.

## 4. Security and Governance

- User registration and login.
- Role-based access control model (admin, finance_manager, accountant, auditor).
- Token-based auth flow implemented.
- Comprehensive action logging for traceability.

## 5. Current Project State

### Strengths

- End-to-end workflow is implemented from ingestion to reporting.
- Business modules are broad and well-separated.
- Strong operational visibility via dashboard and logs.

### Current Limitations and Considerations

- SQLite is the default storage target (good for local/prototype setups).
- Token and password approach is lightweight and should be hardened for production.
- Export-to-PDF implementation is basic and can be upgraded.
- No automated test suite is currently present in the repository tree.

## 6. Summary

FinTwin is a practical finance operations platform that combines document intelligence, reconciliation automation, exception workflows, configurable business rules, learning-assisted improvements, and reporting in a single full-stack application.
