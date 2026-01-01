# Schema Drift Detection

## Context

Source systems change their schemas without notice. A field that was optional yesterday becomes required today. A string field becomes an integer. New fields appear. Old fields disappear. These changes break downstream pipelines, causing data quality issues, failed transformations, and silent data corruption.

The challenge isn't just detecting changes—it's understanding their impact. A new optional field might be harmless, but a required field becoming optional could break validation logic. A type change from string to integer might cause silent failures or data loss. Your drift detection system must not only identify changes but also assess their severity and impact on downstream systems.

## Core Functionality

Build a production-ready schema drift detection system with the following capabilities:

### Schema Snapshot & Comparison
- **Schema Capture**: Capture complete schema snapshots (field names, types, constraints, nullability)
- **Schema Storage**: Store schemas in versioned registry with timestamps
- **Schema Comparison**: Compare current schema against previous versions
- **Diff Generation**: Generate detailed diff reports showing all changes
- **Schema Versioning**: Track schema versions with semantic versioning

### Change Detection
- **Field Addition**: Detect new fields added to schema
- **Field Removal**: Detect fields removed from schema
- **Type Changes**: Detect changes in data types (string → integer, etc.)
- **Constraint Changes**: Detect changes in nullability, uniqueness, defaults
- **Enum Value Changes**: Detect changes in allowed enum values
- **Nested Structure Changes**: Detect changes in nested objects/arrays

### Impact Analysis
- **Pipeline Impact**: Identify which pipelines use affected fields
- **Transformation Impact**: Identify which transformations depend on changed fields
- **Downstream Impact**: Identify downstream systems consuming affected data
- **Breaking Change Detection**: Classify changes as breaking vs non-breaking
- **Dependency Graph**: Build dependency graph of fields and transformations

### Alerting & Notification
- **Severity Classification**: Classify changes by severity (critical, warning, info)
- **Multi-Channel Alerts**: Send alerts via email, Slack, PagerDuty, webhooks
- **Alert Aggregation**: Group related changes into single alert
- **Alert Suppression**: Suppress alerts for expected changes
- **Alert History**: Maintain history of all alerts sent

### Migration Suggestions
- **Automatic Migrations**: Suggest automatic migration scripts for safe changes
- **Manual Review Flags**: Flag changes requiring manual review
- **Backward Compatibility**: Check if changes maintain backward compatibility
- **Data Validation**: Suggest validation rules for new/changed fields
- **Rollback Plans**: Generate rollback plans for schema changes

## Edge Cases

### Backward-Incompatible Changes
- **Required Field Added**: New required field breaks existing records
- **Type Narrowing**: String field becomes enum with limited values
- **Constraint Tightening**: Nullable field becomes non-nullable
- **Field Removal**: Required field removed breaks downstream queries
- **Enum Value Removal**: Removed enum value breaks existing data

### Gradual Schema Evolution
- **Optional to Required**: Field gradually becomes required over time
- **Type Coercion**: Field type changes but old values still present
- **Field Deprecation**: Field marked deprecated but still in use
- **Schema Drift**: Schema changes without version bump
- **Partial Rollout**: Schema changes rolled out gradually across instances

### Nested Structure Changes
- **Object Field Changes**: Changes to nested object structures
- **Array Element Changes**: Changes to array element schemas
- **Deep Nesting**: Changes deep in nested structures
- **Optional Nesting**: Nested objects becoming optional or required
- **Type Changes in Nested Fields**: Type changes within nested structures

### Data Quality Impact
- **Silent Failures**: Type changes causing silent data loss
- **Validation Failures**: Constraint changes causing validation failures
- **Query Failures**: Field removal breaking existing queries
- **Aggregation Errors**: Type changes breaking aggregations
- **Join Failures**: Key field changes breaking joins

### Multi-Source Schema Drift
- **Multiple Sources**: Same logical schema from multiple sources drifting differently
- **Schema Merging**: Merging schemas from multiple sources
- **Conflict Resolution**: Resolving conflicts between source schemas
- **Consistency Checks**: Ensuring consistency across sources

## Resilience Patterns

### Schema Versioning
- **Semantic Versioning**: Use semantic versioning (major.minor.patch)
- **Version History**: Maintain complete version history
- **Version Comparison**: Compare any two schema versions
- **Version Tagging**: Tag important schema versions
- **Rollback Support**: Support rolling back to previous schema versions

### Backward Compatibility Checks
- **Compatibility Rules**: Define rules for backward compatibility
- **Automatic Checks**: Automatically check compatibility on schema changes
- **Compatibility Reports**: Generate compatibility reports
- **Migration Paths**: Identify migration paths for incompatible changes
- **Deprecation Warnings**: Warn about deprecated fields before removal

### Impact Analysis Engine
- **Dependency Tracking**: Track dependencies between fields and transformations
- **Impact Scoring**: Score impact of changes (high/medium/low)
- **Affected Components**: List all affected components
- **Test Coverage**: Check if affected components have tests
- **Risk Assessment**: Assess risk of changes

### Change Validation
- **Schema Validation**: Validate new schema against rules
- **Data Validation**: Validate existing data against new schema
- **Compatibility Validation**: Validate backward compatibility
- **Impact Validation**: Validate impact on downstream systems
- **Rollback Validation**: Validate rollback plans

### Monitoring & Observability
- **Change Logging**: Log all schema changes with context
- **Metrics Tracking**: Track schema change frequency and types
- **Alert Metrics**: Track alert delivery and acknowledgment
- **Impact Metrics**: Track impact of schema changes on pipelines
- **Dashboard**: Visualize schema evolution over time

## Configuration Options

### Schema Registry Configuration
```yaml
schema_registry:
  storage:
    type: "database" | "file" | "api"
    connection: "${SCHEMA_REGISTRY_DB_URL}"
  
  versioning:
    strategy: "semantic" | "timestamp" | "hash"
    auto_version: true
  
  comparison:
    ignore_fields: ["_metadata", "_timestamp"]
    compare_types: true
    compare_constraints: true
    compare_nested: true
```

### Detection Configuration
```yaml
detection:
  sources:
    - name: "customers_api"
      type: "api"
      endpoint: "https://api.example.com/schema"
      frequency: "daily"
    
    - name: "transactions_db"
      type: "database"
      connection: "${DB_URL}"
      table: "transactions"
      frequency: "hourly"
  
  change_types:
    - "field_addition"
    - "field_removal"
    - "type_change"
    - "constraint_change"
    - "enum_change"
```

### Impact Analysis Configuration
```yaml
impact_analysis:
  pipelines:
    - name: "customer_etl"
      dependencies: ["customers_api.name", "customers_api.email"]
    
    - name: "transaction_etl"
      dependencies: ["transactions_db.*"]
  
  severity_rules:
    critical:
      - "required_field_removed"
      - "type_change_incompatible"
    warning:
      - "optional_field_removed"
      - "type_change_compatible"
    info:
      - "field_added"
      - "constraint_relaxed"
```

### Alerting Configuration
```yaml
alerting:
  channels:
    - type: "email"
      recipients: ["data-team@example.com"]
      severity: ["critical", "warning"]
    
    - type: "slack"
      webhook: "${SLACK_WEBHOOK}"
      channel: "#data-alerts"
      severity: ["critical"]
    
    - type: "pagerduty"
      service_key: "${PAGERDUTY_KEY}"
      severity: ["critical"]
  
  aggregation:
    enabled: true
    window: "5 minutes"
  
  suppression:
    - pattern: ".*_metadata"
      reason: "Metadata fields change frequently"
```

## Output Specifications

### Schema Diff Report
```json
{
  "metadata": {
    "source": "customers_api",
    "previous_version": "1.2.3",
    "current_version": "1.3.0",
    "detected_at": "2024-01-15T10:30:00Z",
    "comparison_timestamp": "2024-01-15T09:00:00Z"
  },
  "changes": [
    {
      "type": "field_addition",
      "field": "phone_number",
      "severity": "info",
      "details": {
        "type": "string",
        "nullable": true,
        "description": "Customer phone number"
      }
    },
    {
      "type": "type_change",
      "field": "age",
      "severity": "warning",
      "details": {
        "previous_type": "string",
        "current_type": "integer",
        "breaking": false,
        "migration_required": true
      }
    },
    {
      "type": "constraint_change",
      "field": "email",
      "severity": "critical",
      "details": {
        "previous": {"nullable": true},
        "current": {"nullable": false},
        "breaking": true,
        "affected_records": 150
      }
    }
  ],
  "impact_analysis": {
    "affected_pipelines": [
      {
        "pipeline": "customer_etl",
        "impact": "high",
        "affected_fields": ["email"],
        "status": "will_fail"
      }
    ],
    "affected_transformations": [
      {
        "transformation": "validate_email",
        "impact": "high",
        "status": "will_fail"
      }
    ],
    "risk_score": 0.85
  },
  "migration_suggestions": [
    {
      "change": "email.nullable: true → false",
      "suggestion": "Backfill null emails or make field optional in pipeline",
      "automatic": false,
      "estimated_effort": "2 hours"
    }
  ],
  "rollback_plan": {
    "previous_schema_version": "1.2.3",
    "rollback_steps": [
      "1. Revert API schema to version 1.2.3",
      "2. Update pipeline to handle nullable email",
      "3. Validate data consistency"
    ]
  }
}
```

### Alert Format
```json
{
  "alert_id": "alert_123456",
  "severity": "critical",
  "title": "Breaking schema change detected in customers_api",
  "message": "Field 'email' changed from nullable to non-nullable",
  "source": "customers_api",
  "detected_at": "2024-01-15T10:30:00Z",
  "changes": [
    {
      "type": "constraint_change",
      "field": "email",
      "breaking": true
    }
  ],
  "impact": {
    "affected_pipelines": 3,
    "risk_score": 0.85
  },
  "actions": [
    {
      "action": "review_migration",
      "url": "https://schema-registry.example.com/changes/123456"
    }
  ]
}
```

### Success Criteria
- ✅ Detects all schema changes (additions, removals, type changes, constraints)
- ✅ Accurately classifies changes by severity and breaking status
- ✅ Identifies all affected pipelines and transformations
- ✅ Provides actionable migration suggestions
- ✅ Sends timely alerts via configured channels
- ✅ Maintains complete schema version history
- ✅ Supports rollback to previous schema versions
- ✅ Handles nested schema structures correctly

## Usage Example

### Customizing Schema Sources
Replace `[SOURCE_NAME]` with your data source names and configure how to fetch schemas (API endpoints, database connections, file paths).

### Customizing Impact Analysis
Define your pipelines and their field dependencies. Configure severity rules based on your organization's tolerance for breaking changes.

### Customizing Alerting
Configure alert channels (email, Slack, PagerDuty) and severity thresholds. Set up alert suppression for expected changes.

### Testing Requirements
1. **Unit Tests**: Test schema comparison, change detection, impact analysis
2. **Integration Tests**: Test with real schema changes, verify alerts
3. **Edge Case Tests**: Test nested changes, gradual evolution, multi-source drift
4. **Performance Tests**: Test with large schemas, many dependencies
5. **Alert Tests**: Verify alerts are sent correctly, test alert suppression

## Implementation Notes

- Use schema validation libraries: `jsonschema`, `pydantic`, `marshmallow` for schema definition
- Implement efficient schema comparison using hash-based change detection
- Use graph algorithms for dependency tracking and impact analysis
- Store schemas in versioned storage (Git, database with versioning)
- Implement webhook endpoints for real-time schema change notifications
- Consider using schema registries (Confluent Schema Registry, AWS Glue Schema Registry)
- Implement caching for schema fetches and comparisons
- Use structured logging for all schema changes and alerts
- Consider machine learning for predicting impact of schema changes

