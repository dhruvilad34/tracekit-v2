-- ============================================
-- TraceKit v2 — Database Schema
-- Pharma MES Recipe Designer
-- ============================================

-- Master Batch Records (MBR)
-- The template/recipe — never executed directly
CREATE TABLE batch_records (
    id              SERIAL PRIMARY KEY,
    title           VARCHAR(255) NOT NULL,
    product_code    VARCHAR(100) NOT NULL,
    version         VARCHAR(20) NOT NULL DEFAULT '1.0',
    status          VARCHAR(50) NOT NULL DEFAULT 'draft',
    -- status options: draft, under_review, approved, obsolete
    created_by      VARCHAR(100) NOT NULL DEFAULT 'system',
    created_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Process Steps within a Batch Record
CREATE TABLE steps (
    id                    SERIAL PRIMARY KEY,
    batch_record_id       INTEGER NOT NULL REFERENCES batch_records(id) ON DELETE CASCADE,
    step_number           INTEGER NOT NULL,
    operation_type        VARCHAR(100) NOT NULL,
    -- e.g. Dispense, Mix, Process, Transfer, Sample, Clean, Inspect
    description           TEXT,
    parameters            JSONB,
    -- flexible key-value pairs: {"speed": "250 rpm", "duration": "12 min"}
    is_critical           BOOLEAN NOT NULL DEFAULT FALSE,
    requires_double_check BOOLEAN NOT NULL DEFAULT FALSE,
    source_reference      VARCHAR(255),
    -- paper master formula reference e.g. PMF-2024-001 §3.2
    status                VARCHAR(50) NOT NULL DEFAULT 'draft',
    created_at            TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Parameter Value Lists (PVL)
-- Min/target/max ranges for each parameter
CREATE TABLE pvl (
    id               SERIAL PRIMARY KEY,
    batch_record_id  INTEGER NOT NULL REFERENCES batch_records(id) ON DELETE CASCADE,
    parameter_name   VARCHAR(255) NOT NULL,
    min_value        NUMERIC,
    target_value     NUMERIC,
    max_value        NUMERIC,
    unit             VARCHAR(50),
    -- e.g. rpm, kg, °C, min, bar
    notes            TEXT,
    created_at       TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Executed Batch Records (EBR)
-- An actual production run — instantiated FROM an MBR
CREATE TABLE executions (
    id               SERIAL PRIMARY KEY,
    batch_record_id  INTEGER NOT NULL REFERENCES batch_records(id),
    lot_number       VARCHAR(100) NOT NULL UNIQUE,
    batch_size       NUMERIC,
    batch_size_unit  VARCHAR(50),
    operator         VARCHAR(100) NOT NULL,
    reviewed_by      VARCHAR(100),
    approved_by      VARCHAR(100),
    reviewed_at      TIMESTAMP,
    approved_at      TIMESTAMP,
    status           VARCHAR(50) NOT NULL DEFAULT 'in_progress',
    -- status options: in_progress, completed, rejected
    started_at       TIMESTAMP NOT NULL DEFAULT NOW(),
    completed_at     TIMESTAMP
);

-- Deviations & CAPA
-- Logged against a specific step in an execution
CREATE TABLE deviations (
    id               SERIAL PRIMARY KEY,
    execution_id     INTEGER NOT NULL REFERENCES executions(id) ON DELETE CASCADE,
    step_id          INTEGER REFERENCES steps(id),
    deviation_type   VARCHAR(100) NOT NULL,
    -- e.g. Out of Specification, Equipment Failure, Process Deviation
    description      TEXT NOT NULL,
    root_cause       TEXT,
    capa_reference   VARCHAR(100),
    -- Corrective and Preventive Action ID
    severity         VARCHAR(50) NOT NULL DEFAULT 'minor',
    -- minor, major, critical
    status           VARCHAR(50) NOT NULL DEFAULT 'open',
    -- open, under_review, closed
    raised_by        VARCHAR(100) NOT NULL,
    raised_at        TIMESTAMP NOT NULL DEFAULT NOW(),
    closed_at        TIMESTAMP
);

-- Change Controls
-- Tracks changes made to batch records
CREATE TABLE change_controls (
    id               SERIAL PRIMARY KEY,
    batch_record_id  INTEGER NOT NULL REFERENCES batch_records(id) ON DELETE CASCADE,
    description      TEXT NOT NULL,
    reason           TEXT NOT NULL,
    initiator        VARCHAR(100) NOT NULL,
    status           VARCHAR(50) NOT NULL DEFAULT 'open',
    -- open, under_review, approved, rejected, closed
    effective_date   DATE,
    created_at       TIMESTAMP NOT NULL DEFAULT NOW(),
    closed_at        TIMESTAMP
);

-- Audit Trail (21 CFR Part 11 simulation)
-- Auto-logs every create/update/delete across all tables
CREATE TABLE audit_log (
    id           SERIAL PRIMARY KEY,
    table_name   VARCHAR(100) NOT NULL,
    record_id    INTEGER NOT NULL,
    action       VARCHAR(20) NOT NULL,
    -- INSERT, UPDATE, DELETE
    changed_by   VARCHAR(100) NOT NULL DEFAULT 'system',
    changed_at   TIMESTAMP NOT NULL DEFAULT NOW(),
    old_value    JSONB,
    new_value    JSONB
);

-- ============================================
-- Indexes for performance
-- ============================================
CREATE INDEX idx_steps_batch_record ON steps(batch_record_id);
CREATE INDEX idx_pvl_batch_record ON pvl(batch_record_id);
CREATE INDEX idx_executions_batch_record ON executions(batch_record_id);
CREATE INDEX idx_deviations_execution ON deviations(execution_id);
CREATE INDEX idx_change_controls_batch ON change_controls(batch_record_id);
CREATE INDEX idx_audit_log_table ON audit_log(table_name, record_id);