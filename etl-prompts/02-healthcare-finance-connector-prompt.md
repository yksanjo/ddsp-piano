# ETL Connector: Healthcare & Finance Systems

## Context

Healthcare and financial systems operate under strict regulatory requirements (HIPAA, PCI-DSS, SOX) and use industry-standard formats that are simultaneously rigid and ambiguous. HL7 messages can have segments in any order, FHIR resources have optional fields that are sometimes required, and financial APIs return partial data that must be reconciled.

The challenge isn't just parsing these formats—it's handling the reality that a "required" field in the spec might be missing 30% of the time, that patient identifiers change formats mid-stream, and that financial transactions arrive out of order with no reliable sequence numbers.

## Core Functionality

Build a production-ready ETL connector for healthcare standards (HL7, FHIR) and financial APIs (Plaid, Stripe, QuickBooks, X12 EDI) with the following capabilities:

### Healthcare Standards Support

#### HL7 Message Processing
- **Message Parsing**: Parse HL7 v2.x messages (pipe-delimited format)
- **Segment Handling**: Process MSH, PID, PV1, OBR, OBX, and custom segments
- **Message Types**: ADT (admissions), ORU (results), ORM (orders), MDM (documents)
- **Encoding Detection**: Handle different character sets (ASCII, UTF-8, MLLP)
- **Acknowledgment Generation**: Generate ACK messages for message receipt

#### FHIR Resource Processing
- **Resource Parsing**: Parse FHIR R4 JSON/XML resources
- **Resource Types**: Patient, Observation, Encounter, Procedure, Medication
- **Bundle Processing**: Handle FHIR Bundles (collections of resources)
- **Reference Resolution**: Resolve internal references between resources
- **Version Handling**: Support multiple FHIR versions and profiles

### Financial API Integration

#### OAuth2 Authentication
- **Authorization Flow**: Complete OAuth2 authorization code flow
- **Token Management**: Automatic token refresh, secure token storage
- **Multi-Account Support**: Handle multiple connected accounts per user
- **Webhook Verification**: Validate webhook signatures for security

#### Transaction Processing
- **Transaction Extraction**: Pull transactions from Plaid, Stripe, QuickBooks
- **Account Management**: Sync account information and balances
- **Reconciliation**: Match transactions across systems
- **Categorization**: Support transaction categorization and tagging

#### X12 EDI Processing
- **Transaction Sets**: 837 (claims), 835 (payments), 270/271 (eligibility), 834 (enrollment)
- **Segment Parsing**: Parse ISA, GS, ST, and transaction-specific segments
- **Loop Handling**: Process hierarchical loop structures
- **Trading Partner Management**: Handle multiple trading partner configurations

### Webhook Processing
- **Event Receiving**: Accept webhooks from financial APIs and FHIR servers
- **Event Validation**: Verify webhook authenticity and integrity
- **Idempotency**: Handle duplicate webhook deliveries
- **Async Processing**: Queue webhooks for background processing

## Edge Cases

### Healthcare Data Challenges

#### HL7 Message Issues
- **Out-of-Order Segments**: Segments can appear in any order (spec allows this)
- **Missing Required Fields**: Fields marked "required" in spec but missing in practice
- **Repeating Fields**: Fields that can repeat with different delimiters
- **Escape Sequences**: Special characters escaped with `\E\`, `\F\`, `\R\`, `\S\`, `\T\`
- **Continuation Messages**: Messages split across multiple transmissions
- **Character Encoding**: Mixed ASCII/UTF-8, special characters in names

#### FHIR Resource Issues
- **Optional Fields Required**: Fields marked optional but required by business logic
- **Missing References**: Resources referencing other resources that don't exist
- **Version Mismatches**: Resources using different FHIR versions
- **Profile Variations**: Custom profiles with additional required fields
- **Large Resources**: Resources exceeding API size limits
- **Nested Resources**: Deeply nested structures causing parsing issues

#### Compliance & Privacy
- **PII Handling**: Patient names, SSNs, addresses must be handled per HIPAA
- **De-identification**: Support for de-identified data extraction
- **Audit Logging**: Complete audit trail for compliance
- **Data Retention**: Handle data retention and deletion requirements

### Financial Data Challenges

#### API Limitations
- **Rate Limits**: Strict rate limits (e.g., Plaid: 500 requests/hour)
- **Partial Data**: Transactions missing merchant names, categories
- **Delayed Data**: Transactions appearing days after occurrence
- **Duplicate Transactions**: Same transaction from multiple sources
- **Failed Transactions**: Transactions that failed but still appear in feeds

#### Data Quality Issues
- **Missing Metadata**: Transactions without timestamps, locations
- **Currency Mismatches**: Multi-currency accounts with conversion issues
- **Timezone Confusion**: Transaction times in different timezones
- **Account Changes**: Accounts closed, merged, or renamed mid-sync

#### X12 EDI Challenges
- **Trading Partner Variations**: Each partner uses slightly different formats
- **Version Differences**: 4010 vs 5010, different transaction set versions
- **Loop Variations**: Optional loops that some partners include, others don't
- **Segment Ordering**: Segments can appear in different orders
- **Data Element Variations**: Same data element formatted differently

## Resilience Patterns

### Message Validation
- **Schema Validation**: Validate HL7/FHIR messages against schemas
- **Business Rule Validation**: Check business logic beyond schema
- **Error Reporting**: Detailed error messages with field-level issues
- **Validation Modes**: Strict (reject invalid) vs lenient (warn and continue)

### Compliance & Security
- **Encryption**: Encrypt PII at rest and in transit
- **Access Controls**: Role-based access to sensitive data
- **Audit Logging**: Log all data access and modifications
- **Data Masking**: Mask PII in logs and non-production environments
- **Token Security**: Secure storage and rotation of API tokens

### Error Recovery
- **Message Retry**: Retry failed message processing with exponential backoff
- **Partial Processing**: Process valid parts of message even if some parts fail
- **Dead Letter Queue**: Store unprocessable messages for manual review
- **Reconciliation**: Reconcile missing or duplicate transactions

### Rate Limit Handling
- **Request Throttling**: Automatically throttle requests to stay under limits
- **Queue Management**: Queue requests when rate limited
- **Backoff Strategies**: Exponential backoff with jitter
- **Priority Queuing**: Prioritize critical requests over batch operations

## Configuration Options

### Healthcare Configuration
```yaml
healthcare:
  hl7:
    version: "2.5"
    encoding: "utf-8"
    message_types: ["ADT^A01", "ORU^R01"]
    validation_mode: "strict" | "lenient"
    ack_required: true
  
  fhir:
    base_url: "https://fhir.example.com"
    version: "R4"
    resource_types: ["Patient", "Observation", "Encounter"]
    authentication:
      type: "oauth2" | "basic" | "bearer"
      token: "${FHIR_TOKEN}"
```

### Financial API Configuration
```yaml
financial:
  plaid:
    client_id: "${PLAID_CLIENT_ID}"
    secret: "${PLAID_SECRET}"
    environment: "sandbox" | "development" | "production"
    webhook_url: "https://api.example.com/webhooks/plaid"
  
  stripe:
    api_key: "${STRIPE_API_KEY}"
    webhook_secret: "${STRIPE_WEBHOOK_SECRET}"
  
  quickbooks:
    client_id: "${QB_CLIENT_ID}"
    client_secret: "${QB_CLIENT_SECRET}"
    realm_id: "${QB_REALM_ID}"
    oauth_token: "${QB_OAUTH_TOKEN}"
```

### X12 EDI Configuration
```yaml
x12:
  trading_partners:
    - name: "insurance_company_a"
      id: "123456789"
      isa_id: "00"
      gs_id: "HC"
      transaction_sets: ["837", "835"]
      version: "5010"
  
  processing:
    validate_isa: true
    validate_gs: true
    strict_segment_order: false
```

## Output Specifications

### Healthcare Output Format
```json
{
  "metadata": {
    "source_system": "hl7" | "fhir",
    "message_type": "ADT^A01",
    "message_id": "MSG123456",
    "received_at": "2024-01-15T10:30:00Z",
    "processed_at": "2024-01-15T10:30:01Z",
    "validation_status": "valid" | "warning" | "error"
  },
  "patient": {
    "id": "PAT001",
    "name": "John Doe",
    "dob": "1980-01-15",
    "gender": "M",
    "identifiers": [
      {"type": "MRN", "value": "12345"},
      {"type": "SSN", "value": "***-**-1234"}  # masked
    ]
  },
  "encounter": {
    "id": "ENC001",
    "admit_date": "2024-01-15T08:00:00Z",
    "discharge_date": null,
    "type": "inpatient"
  },
  "compliance": {
    "hipaa_compliant": true,
    "pii_masked": true,
    "audit_log_id": "AUD123456"
  },
  "errors": [],
  "warnings": []
}
```

### Financial Output Format
```json
{
  "metadata": {
    "source": "plaid" | "stripe" | "quickbooks",
    "account_id": "acc_123456",
    "sync_timestamp": "2024-01-15T10:30:00Z",
    "transaction_count": 45
  },
  "account": {
    "id": "acc_123456",
    "name": "Checking Account",
    "type": "depository",
    "balance": 1234.56,
    "currency": "USD"
  },
  "transactions": [
    {
      "id": "txn_789",
      "date": "2024-01-14",
      "amount": -25.50,
      "merchant": "Coffee Shop",
      "category": "Food and Drink",
      "pending": false,
      "reconciled": true
    }
  ],
  "reconciliation": {
    "matched": 43,
    "unmatched": 2,
    "duplicates": 0
  }
}
```

### Success Criteria
- ✅ Successfully parses HL7 v2.x messages with all edge cases
- ✅ Processes FHIR R4 resources with reference resolution
- ✅ Integrates with financial APIs (Plaid, Stripe, QuickBooks)
- ✅ Handles X12 EDI transaction sets correctly
- ✅ Maintains HIPAA/PCI-DSS compliance
- ✅ Processes webhooks with idempotency
- ✅ Validates all messages/resources before processing
- ✅ Provides complete audit trail

## Usage Example

### Customizing for HL7
Specify the HL7 version, message types to process, and validation strictness. Configure segment mappings for your specific use case.

### Customizing for FHIR
Set the FHIR server base URL, resource types to extract, and authentication method. Configure custom profiles if your server uses them.

### Customizing for Financial APIs
Replace `[API_NAME]` with `plaid`, `stripe`, or `quickbooks`. Configure OAuth credentials and webhook endpoints. Specify which account types and transaction categories to sync.

### Testing Requirements
1. **Unit Tests**: Mock HL7/FHIR messages, test parsing edge cases
2. **Integration Tests**: Connect to test FHIR server, verify resource extraction
3. **Compliance Tests**: Verify PII masking, audit logging
4. **API Tests**: Test OAuth flows, webhook processing, rate limiting
5. **EDI Tests**: Validate X12 parsing with multiple trading partners

## Implementation Notes

- Use `hl7apy` or `python-hl7` for HL7 parsing
- Use `fhir.resources` or `fhirclient` for FHIR processing
- Use official SDKs for financial APIs (Plaid Python, Stripe Python)
- Implement comprehensive validation before processing
- Store sensitive credentials in secure vaults (AWS Secrets Manager, HashiCorp Vault)
- Implement idempotency keys for webhook processing
- Use structured logging with PII redaction
- Consider using message queues (RabbitMQ, Kafka) for async processing

