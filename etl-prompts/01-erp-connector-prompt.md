# ETL Connector: Legacy ERP Systems

## Context

Enterprise Resource Planning (ERP) systems like SAP, Oracle, NetSuite, and Microsoft Dynamics contain critical business data but present significant integration challenges. These systems often use proprietary APIs, legacy protocols (SOAP, ODBC), and inconsistent data formats that reflect decades of organizational decisions, regional variations, and technical debt.

The reality of ERP data extraction is messy: customer IDs mean different things in different modules, dates are formatted inconsistently across regions, and critical fields are sometimes just missing. Your connector must handle the political reality that "customer_id" in the sales module might be a string, while in finance it's an integer, and in logistics it's a composite key.

## Core Functionality

Build a production-ready ETL connector that can extract data from legacy ERP systems with the following capabilities:

### Multi-Protocol Support
- **REST APIs**: Modern ERP systems (NetSuite, Dynamics 365) expose REST endpoints
- **SOAP APIs**: Legacy systems (older SAP, Oracle) use SOAP with WSDL definitions
- **ODBC/JDBC**: Direct database connections for systems that allow it
- **File Exports**: CSV, Excel, fixed-width files for systems with no API access
- **FTP/SFTP**: Scheduled file drops from ERP systems

### Authentication & Security
- OAuth2 flows for modern APIs
- Basic authentication with credential rotation
- Certificate-based authentication for SOAP
- Database connection strings with encrypted credentials
- Support for service accounts and impersonation

### Data Extraction
- **Pagination**: Handle cursor-based, offset-based, and token-based pagination
- **Batch Processing**: Extract large datasets in configurable batch sizes
- **Incremental Extraction**: Track last sync timestamp and extract only new/changed records
- **Field Selection**: Allow selective field extraction to reduce payload size
- **Filtering**: Support date ranges, status filters, and custom WHERE clauses

### Rate Limiting & Throttling
- Respect API rate limits with exponential backoff
- Queue management for high-volume extractions
- Parallel extraction with concurrency limits
- Request queuing and retry logic

## Edge Cases

### Data Format Inconsistencies
- **Date Formats**: "2024-01-15", "01/15/2024", "15.01.2024", "20240115", Unix timestamps
- **Null Representations**: `NULL`, `""`, `"N/A"`, `"NULL"`, `"null"`, `"-"`, `"NONE"`
- **Encoding Issues**: Latin-1 vs UTF-8, Windows-1252, mixed encodings in same field
- **Timezone Confusion**: UTC, local time, timezone-naive timestamps
- **Numeric Formats**: "1,234.56" vs "1234.56" vs "1.234,56" (regional differences)

### System-Specific Quirks
- **SAP**: BAPI calls, RFC functions, IDoc processing, German date formats
- **Oracle**: PL/SQL procedures, complex object types, CLOB/BLOB handling
- **NetSuite**: SuiteQL vs RESTlet, script execution limits, custom fields
- **Dynamics**: OData queries, complex entity relationships, option sets

### Data Quality Issues
- **Missing Required Fields**: Systems that claim fields are required but data shows otherwise
- **Inconsistent Schemas**: Same table/endpoint returning different fields across environments
- **Soft Deletes**: Records marked as deleted but still in database
- **Orphaned Records**: Foreign key violations, broken relationships
- **Duplicate Keys**: Systems allowing duplicate primary keys (yes, this happens)

## Resilience Patterns

### Connection Management
- **Connection Pooling**: Reuse connections to reduce overhead
- **Connection Timeout**: Configurable timeouts with clear error messages
- **Automatic Reconnection**: Detect connection drops and reconnect transparently
- **Health Checks**: Periodic connection validation

### Error Handling
- **Retry Logic**: Exponential backoff for transient failures (5xx errors, timeouts)
- **Circuit Breaker**: Stop attempting connections after repeated failures
- **Partial Failure Handling**: Continue processing other records when one fails
- **Error Classification**: Distinguish between retryable and non-retryable errors

### Transaction Safety
- **Atomic Operations**: Ensure all-or-nothing extraction for related records
- **Rollback Capability**: Ability to rollback partial extractions
- **Checkpointing**: Save progress to resume after failures
- **Idempotency**: Safe to re-run extractions without duplicating data

### Monitoring & Observability
- **Extraction Metrics**: Records processed, bytes transferred, duration
- **Error Logging**: Detailed logs with context for debugging
- **Performance Tracking**: Track extraction times and identify bottlenecks
- **Alerting**: Notify on failures, rate limit hits, or data quality issues

## Configuration Options

### Connection Configuration
```yaml
erp_system:
  type: "sap" | "oracle" | "netsuite" | "dynamics"
  protocol: "rest" | "soap" | "odbc" | "file"
  connection_string: "encrypted_connection_string"
  credentials:
    username: "${ERP_USERNAME}"
    password: "${ERP_PASSWORD}"
    api_key: "${API_KEY}"
  timeout: 300  # seconds
  max_retries: 3
```

### Extraction Configuration
```yaml
extraction:
  source: "customers"  # table/endpoint name
  fields: ["id", "name", "email", "created_date"]  # optional: specific fields
  batch_size: 1000
  incremental: true
  last_sync_field: "updated_at"
  filters:
    status: "active"
    created_after: "2024-01-01"
```

### Data Transformation
```yaml
transformations:
  date_formats:
    - "YYYY-MM-DD"
    - "MM/DD/YYYY"
    - "DD.MM.YYYY"
  null_values: ["NULL", "N/A", "", "-"]
  encoding: "utf-8"
  timezone: "UTC"
```

## Output Specifications

### Standardized Output Format
The connector should output data in a consistent format regardless of source system:

```json
{
  "metadata": {
    "source_system": "sap",
    "source_table": "customers",
    "extraction_timestamp": "2024-01-15T10:30:00Z",
    "extraction_id": "ext_123456",
    "record_count": 1523,
    "batch_number": 1,
    "total_batches": 2
  },
  "records": [
    {
      "id": "CUST001",
      "name": "Acme Corporation",
      "email": "contact@acme.com",
      "created_date": "2024-01-15T08:00:00Z",
      "_source_metadata": {
        "original_id": "0000000123",
        "extracted_at": "2024-01-15T10:30:00Z"
      }
    }
  ],
  "errors": [],
  "warnings": [
    "Field 'phone' missing in 5 records",
    "Date parsing failed for 2 records, using original value"
  ]
}
```

### Success Criteria
- ✅ Successfully extracts data from configured ERP system
- ✅ Handles all specified edge cases gracefully
- ✅ Provides detailed error messages and warnings
- ✅ Outputs standardized format with metadata
- ✅ Supports resumable extractions via checkpointing
- ✅ Logs all operations for audit trail
- ✅ Respects rate limits and handles throttling
- ✅ Processes at least 10,000 records without memory issues

## Usage Example

### Customizing for SAP
Replace `[SYSTEM_TYPE]` with `sap`, `[PROTOCOL]` with `soap` or `rfc`, and specify:
- BAPI function names or RFC destinations
- SAP client number and system ID
- Language settings (important for date formats)

### Customizing for NetSuite
Replace `[SYSTEM_TYPE]` with `netsuite`, `[PROTOCOL]` with `rest`, and specify:
- Account ID and environment (sandbox/production)
- SuiteQL queries or RESTlet scripts
- Custom field mappings
- Script execution limits

### Testing Requirements
1. **Unit Tests**: Mock ERP responses, test date parsing, null handling
2. **Integration Tests**: Connect to test ERP instance, verify extraction
3. **Edge Case Tests**: Invalid dates, encoding issues, missing fields
4. **Performance Tests**: Large dataset extraction, rate limit handling
5. **Failure Tests**: Network failures, authentication errors, malformed responses

## Implementation Notes

- Use established libraries: `requests` for REST, `zeep` for SOAP, `pyodbc` for ODBC
- Implement connection pooling for database connections
- Use async/await for I/O-bound operations to improve performance
- Store credentials securely (environment variables, secret managers)
- Implement comprehensive logging with structured logs (JSON format)
- Add data validation before output to catch transformation errors early
- Consider using a message queue for large extractions to avoid timeouts

