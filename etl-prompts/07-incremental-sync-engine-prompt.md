# Incremental Sync Engine

## Context

Full data synchronization is expensive and slow. Incremental sync—only syncing changed data—is essential for production data pipelines. But incremental sync introduces complexity: tracking what's changed, handling late-arriving data, resolving conflicts when the same record is modified in multiple places, and maintaining state across failures.

The reality is that source systems don't always provide reliable change tracking. Some use timestamps (but clocks drift). Some use version numbers (but they reset). Some use change logs (but they get truncated). Your sync engine must handle all these methods while gracefully dealing with the edge cases: records that arrive out of order, deletions that are actually soft deletes, and concurrent modifications that create conflicts.

## Core Functionality

Build a production-ready incremental sync engine with the following capabilities:

### State Management
- **Checkpoint Storage**: Store sync state (last sync timestamp, processed record IDs, etc.)
- **State Recovery**: Recover from failures and resume from last checkpoint
- **Multi-Table State**: Track state for multiple tables/endpoints independently
- **State Versioning**: Version sync state for rollback capability
- **State Validation**: Validate state consistency before resuming sync

### Change Data Capture (CDC)
- **Timestamp-Based CDC**: Track changes using updated_at/modified_at timestamps
- **Version-Based CDC**: Track changes using version numbers or sequence IDs
- **Change Log CDC**: Read from database change logs (binlog, WAL, etc.)
- **Trigger-Based CDC**: Use database triggers to capture changes
- **Polling-Based CDC**: Poll for changes when CDC not available
- **Hybrid CDC**: Combine multiple methods for reliability

### Incremental Processing
- **Batch Processing**: Process changes in configurable batch sizes
- **Streaming Processing**: Process changes in real-time streams
- **Parallel Processing**: Process multiple tables/endpoints in parallel
- **Priority Queuing**: Prioritize critical tables over batch syncs
- **Backpressure Handling**: Handle downstream system backpressure

### Conflict Detection & Resolution
- **Conflict Detection**: Detect when same record modified in multiple places
- **Conflict Types**: Detect update conflicts, delete conflicts, insert conflicts
- **Resolution Strategies**: Last-write-wins, source-wins, custom rules, manual review
- **Conflict Logging**: Log all conflicts with full context
- **Conflict Notification**: Alert on conflicts requiring attention

### Late-Arriving Data Handling
- **Out-of-Order Detection**: Detect records arriving out of chronological order
- **Windowed Processing**: Use time windows to handle late-arriving data
- **Re-processing**: Re-process affected records when late data arrives
- **Watermark Management**: Track high-water mark for processed data
- **Tolerance Windows**: Configure tolerance for late-arriving data

## Edge Cases

### Late-Arriving Data
- **Out-of-Order Updates**: Update for record arrives before insert
- **Delayed Deletes**: Delete arrives days after record was updated
- **Clock Skew**: Source system clock behind, causing "future" timestamps
- **Batch Delays**: Records processed in batches arrive out of order
- **Network Delays**: Network issues causing delayed record delivery

### Deletion Handling
- **Soft Deletes**: Records marked deleted but still in database
- **Hard Deletes**: Records actually removed from source
- **Cascade Deletes**: Deletes triggering related record deletions
- **Delete Propagation**: Handling deletes across related tables
- **Undeleting**: Records deleted then re-inserted

### Concurrent Modifications
- **Same Record, Multiple Sources**: Record modified in multiple systems
- **Rapid Updates**: Same record updated multiple times quickly
- **Race Conditions**: Concurrent syncs causing conflicts
- **Partial Updates**: Only some fields updated, others unchanged
- **Update Conflicts**: Different values for same field from different sources

### State Management Issues
- **State Corruption**: Sync state becomes inconsistent
- **State Loss**: Sync state lost due to storage failure
- **State Divergence**: State differs across multiple sync workers
- **Checkpoint Failures**: Checkpoint save fails mid-sync
- **State Recovery**: Recovering from inconsistent state

### Timezone & Timestamp Issues
- **Timezone Mismatches**: Source and destination in different timezones
- **DST Transitions**: Daylight saving time causing timestamp issues
- **Leap Seconds**: Leap seconds causing timestamp anomalies
- **Timestamp Precision**: Different timestamp precisions (seconds vs milliseconds)
- **Null Timestamps**: Records with null updated_at timestamps

### Data Quality Issues
- **Missing Timestamps**: Records without updated_at timestamps
- **Invalid Timestamps**: Timestamps in wrong format or invalid dates
- **Duplicate Timestamps**: Multiple records with same timestamp
- **Backdated Records**: Records with timestamps in the past
- **Future Timestamps**: Records with timestamps in the future

## Resilience Patterns

### Idempotent Operations
- **Idempotency Keys**: Use keys to ensure operations are idempotent
- **Upsert Logic**: Use upsert (insert or update) for idempotency
- **Idempotency Checks**: Check if operation already performed before executing
- **Retry Safety**: Safe to retry operations without side effects

### State Recovery
- **Checkpoint Validation**: Validate checkpoints before using
- **State Repair**: Repair corrupted state automatically when possible
- **State Reset**: Ability to reset state and start fresh
- **State Migration**: Migrate state format when engine updated
- **Backup & Restore**: Backup state regularly, restore on failure

### Conflict Resolution Policies
- **Policy Configuration**: Configurable conflict resolution policies
- **Field-Level Policies**: Different policies for different fields
- **Source Priority**: Prioritize certain sources over others
- **Manual Review Queue**: Queue conflicts for manual resolution
- **Resolution History**: Track all conflict resolutions

### Error Handling
- **Transient Error Retry**: Retry on transient errors (network, timeouts)
- **Permanent Error Handling**: Handle permanent errors (invalid data) differently
- **Error Classification**: Classify errors for appropriate handling
- **Error Recovery**: Recover from errors and continue processing
- **Dead Letter Queue**: Store unprocessable records for review

### Monitoring & Observability
- **Sync Metrics**: Track records processed, conflicts, errors
- **Latency Metrics**: Track sync latency and lag
- **State Metrics**: Track state size, checkpoint frequency
- **Health Checks**: Monitor sync engine health
- **Alerting**: Alert on sync failures, high latency, many conflicts

## Configuration Options

### Sync Configuration
```yaml
sync:
  source:
    type: "database" | "api" | "file"
    connection: "${SOURCE_CONNECTION}"
    tables: ["customers", "orders", "products"]
  
  destination:
    type: "database" | "api" | "data_warehouse"
    connection: "${DEST_CONNECTION}"
  
  cdc_method: "timestamp" | "version" | "changelog" | "trigger" | "polling"
  
  frequency: "realtime" | "hourly" | "daily"
  batch_size: 1000
  max_parallel_tables: 5
```

### CDC Configuration
```yaml
cdc:
  timestamp:
    updated_at_field: "updated_at"
    created_at_field: "created_at"
    timezone: "UTC"
    tolerance_window: "5 minutes"  # Handle late-arriving data
  
  version:
    version_field: "version"
    sequence_field: "sequence_id"
  
  changelog:
    type: "mysql_binlog" | "postgres_wal" | "mongo_oplog"
    position: "last_processed_position"
  
  polling:
    interval: "1 minute"
    query: "SELECT * FROM table WHERE updated_at > :last_sync"
```

### Conflict Resolution Configuration
```yaml
conflict_resolution:
  default_strategy: "last_write_wins" | "source_wins" | "manual_review"
  
  strategies:
    - field: "email"
      strategy: "source_wins"
      source_priority: ["system_a", "system_b"]
    
    - field: "status"
      strategy: "manual_review"
  
  tolerance:
    time_window: "1 hour"  # Conflicts within this window use default strategy
    manual_review_threshold: 0.8  # Confidence below this requires review
```

### State Management Configuration
```yaml
state:
  storage:
    type: "database" | "file" | "redis"
    connection: "${STATE_STORAGE_CONNECTION}"
  
  checkpointing:
    frequency: "every_batch" | "every_n_records" | "time_based"
    interval: 1000  # records or seconds
  
  recovery:
    validate_on_start: true
    auto_repair: true
    reset_on_corruption: false
```

## Output Specifications

### Sync Status Report
```json
{
  "metadata": {
    "sync_id": "sync_123456",
    "source": "customers_db",
    "destination": "data_warehouse",
    "started_at": "2024-01-15T10:00:00Z",
    "completed_at": "2024-01-15T10:30:00Z",
    "duration_seconds": 1800,
    "status": "completed" | "failed" | "partial"
  },
  "statistics": {
    "records_processed": 15234,
    "records_inserted": 1234,
    "records_updated": 14000,
    "records_deleted": 0,
    "conflicts_detected": 5,
    "conflicts_resolved": 5,
    "errors": 0
  },
  "tables": [
    {
      "table": "customers",
      "records_processed": 5000,
      "records_inserted": 500,
      "records_updated": 4500,
      "last_sync_timestamp": "2024-01-15T10:25:00Z",
      "status": "completed"
    }
  ],
  "conflicts": [
    {
      "record_id": "CUST123",
      "conflict_type": "update_conflict",
      "fields": ["email", "phone"],
      "source_values": {
        "system_a": {"email": "old@example.com", "phone": "555-1234"},
        "system_b": {"email": "new@example.com", "phone": "555-5678"}
      },
      "resolution": "last_write_wins",
      "resolved_value": {"email": "new@example.com", "phone": "555-5678"},
      "resolved_at": "2024-01-15T10:15:00Z"
    }
  ],
  "late_arriving_data": [
    {
      "record_id": "CUST456",
      "expected_timestamp": "2024-01-15T09:00:00Z",
      "actual_timestamp": "2024-01-15T10:20:00Z",
      "delay_seconds": 4800,
      "handled": true
    }
  ],
  "checkpoint": {
    "last_sync_timestamp": "2024-01-15T10:30:00Z",
    "processed_record_ids": ["CUST001", "CUST002", ...],
    "high_water_mark": "2024-01-15T10:30:00Z",
    "state_version": "1.0"
  },
  "errors": [],
  "warnings": [
    "5 records arrived out of order but were processed correctly",
    "Checkpoint saved successfully"
  ]
}
```

### Conflict Resolution Report
```json
{
  "conflict_id": "conflict_789",
  "record_id": "CUST123",
  "conflict_type": "update_conflict",
  "detected_at": "2024-01-15T10:15:00Z",
  "conflicting_fields": ["email", "phone"],
  "sources": [
    {
      "source": "system_a",
      "timestamp": "2024-01-15T09:00:00Z",
      "values": {"email": "old@example.com", "phone": "555-1234"}
    },
    {
      "source": "system_b",
      "timestamp": "2024-01-15T10:00:00Z",
      "values": {"email": "new@example.com", "phone": "555-5678"}
    }
  ],
  "resolution": {
    "strategy": "last_write_wins",
    "resolved_values": {"email": "new@example.com", "phone": "555-5678"},
    "resolved_at": "2024-01-15T10:15:30Z",
    "resolved_by": "system"
  }
}
```

### Success Criteria
- ✅ Successfully syncs only changed data using configured CDC method
- ✅ Handles late-arriving data with configurable tolerance windows
- ✅ Detects and resolves conflicts according to configured policies
- ✅ Maintains consistent state across failures and recoveries
- ✅ Processes large datasets (1M+ records) efficiently
- ✅ Supports multiple tables/endpoints with independent state tracking
- ✅ Provides detailed sync reports with metrics and conflicts
- ✅ Recovers from failures and resumes from last checkpoint

## Usage Example

### Customizing CDC Method
Replace `[CDC_METHOD]` with your CDC method (timestamp, version, changelog, etc.) and configure field names and settings. For changelog CDC, specify database type and position tracking.

### Customizing Conflict Resolution
Configure conflict resolution strategies per field or globally. Set up manual review queues for high-value conflicts.

### Customizing State Storage
Configure where to store sync state (database, file, Redis). Set checkpoint frequency based on your tolerance for re-processing on failure.

### Testing Requirements
1. **Unit Tests**: Test state management, conflict detection, CDC logic
2. **Integration Tests**: Test full sync with real data sources
3. **Failure Tests**: Test state recovery, checkpoint failures, network errors
4. **Conflict Tests**: Test various conflict scenarios and resolutions
5. **Performance Tests**: Test with large datasets, measure throughput and latency

## Implementation Notes

- Use database-specific CDC tools: Debezium for change log CDC, native database CDC features
- Implement efficient state storage using key-value stores or databases
- Use message queues (Kafka, RabbitMQ) for reliable change propagation
- Implement idempotency using unique keys or idempotency tokens
- Use distributed locks for multi-worker sync coordination
- Implement backpressure handling for downstream system capacity limits
- Use structured logging for all sync operations and conflicts
- Consider using event sourcing patterns for complete change history
- Implement monitoring dashboards for sync health and metrics

