# ETL Connector: Advertising Platforms

## Context

Marketing data lives across multiple advertising platforms—Meta (Facebook/Instagram), Google Ads, TikTok, LinkedIn, Twitter—each with different data models, API versions, rate limits, and quirks. Campaign performance data is critical for business decisions, but extracting it reliably requires handling API version changes, rate limit exhaustion, partial data availability, and timezone mismatches.

The reality is that these platforms change their APIs frequently, sometimes without notice. A field that worked yesterday might be deprecated today. Currency conversions vary by account settings. Timezone handling is inconsistent—some APIs return UTC, others return account timezone, and some mix both. Your connector must be resilient to these changes and provide a unified view across platforms.

## Core Functionality

Build a production-ready ETL connector for advertising platforms (Meta Marketing API, Google Ads API, TikTok Marketing API) with the following capabilities:

### OAuth2 Authentication
- **Authorization Flow**: Complete OAuth2 authorization code flow with PKCE
- **Token Management**: Automatic token refresh before expiration
- **Multi-Account Support**: Handle multiple ad accounts per platform
- **Token Storage**: Secure storage of access and refresh tokens
- **Scope Management**: Request and validate required API scopes

### Campaign Data Extraction
- **Campaigns**: Extract campaign metadata, status, budget, schedule
- **Ad Sets**: Extract ad set targeting, budget, schedule, optimization goals
- **Ads**: Extract ad creative, placement, status, performance
- **Audiences**: Extract custom audiences, lookalike audiences, audience insights
- **Insights**: Extract performance metrics (impressions, clicks, conversions, spend)

### Report Generation
- **Async Job Handling**: Submit report requests and poll for completion
- **Report Types**: Pre-defined reports (campaign performance, audience insights, etc.)
- **Custom Reports**: Build custom reports with selected dimensions and metrics
- **Date Ranges**: Support various date range types (last 7 days, custom range, lifetime)
- **Breakdowns**: Support dimension breakdowns (age, gender, device, placement)

### Performance Metrics
- **Standard Metrics**: Impressions, clicks, CTR, CPC, CPM, conversions, ROAS
- **Attribution Windows**: Handle different attribution models (1-day, 7-day, 28-day click/view)
- **Conversion Events**: Extract custom conversion events and values
- **Cross-Platform Metrics**: Normalize metrics across platforms for comparison

## Edge Cases

### API Version Changes
- **Deprecated Fields**: Fields that worked yesterday are deprecated today
- **New Required Fields**: New API versions require previously optional fields
- **Response Format Changes**: JSON structure changes between versions
- **Endpoint Changes**: Endpoints moved or renamed
- **Breaking Changes**: Changes that break existing integrations

### Rate Limiting
- **Rate Limit Exhaustion**: Hitting rate limits mid-extraction
- **Different Limits**: Each platform has different rate limits (requests/hour, requests/day)
- **Concurrent Requests**: Limits on parallel requests
- **Burst Limits**: Short-term burst limits in addition to sustained limits
- **Account-Level Limits**: Different limits per ad account

### Data Availability Issues
- **Partial Data**: Some metrics not available for all time periods
- **Delayed Data**: Performance data delayed by hours or days
- **Missing Historical Data**: Historical data not available after account changes
- **Data Gaps**: Missing data for specific date ranges
- **Estimated vs Actual**: Some metrics are estimates that change later

### Timezone & Currency Challenges
- **Timezone Mismatches**: APIs return data in different timezones
- **Account Timezone**: Account timezone vs UTC confusion
- **Day Boundaries**: Campaigns spanning multiple timezones
- **Currency Conversions**: Multi-currency accounts with conversion rates
- **Currency Formatting**: Different decimal separators and formatting

### Platform-Specific Quirks

#### Meta (Facebook/Instagram)
- **API Versioning**: Frequent version updates (v18.0, v19.0, etc.)
- **Async Jobs**: Long-running async jobs for large reports
- **Field Limitations**: Some fields only available in specific API versions
- **Attribution Windows**: Complex attribution window calculations
- **Breakdown Limitations**: Some breakdowns not available for all metrics

#### Google Ads
- **Query Language**: GAQL (Google Ads Query Language) for data extraction
- **Resource Names**: Complex resource naming conventions
- **Field Masks**: Must specify fields to retrieve (no "select *")
- **Paging**: Token-based pagination with large result sets
- **Report Types**: Different report types for different data needs

#### TikTok
- **API Maturity**: Newer API with frequent changes
- **Limited Historical Data**: Less historical data available
- **Report Generation**: Async report generation with polling
- **Metric Availability**: Some metrics only available for certain ad types
- **Regional Variations**: Different features available by region

## Resilience Patterns

### Rate Limit Handling
- **Exponential Backoff**: Retry with exponential backoff on rate limit errors
- **Rate Limit Detection**: Parse rate limit headers to determine wait time
- **Request Queuing**: Queue requests when approaching rate limits
- **Priority Queuing**: Prioritize critical requests (real-time data) over batch
- **Distributed Rate Limiting**: Coordinate rate limits across multiple workers

### API Version Management
- **Version Detection**: Detect API version from responses
- **Version Fallback**: Fall back to previous version if new version fails
- **Deprecation Warnings**: Log warnings when using deprecated fields
- **Version Pinning**: Pin to specific API versions for stability
- **Migration Support**: Support multiple API versions during migration

### Error Recovery
- **Transient Error Handling**: Retry on 5xx errors, timeouts, network issues
- **Partial Result Processing**: Process available data even if some requests fail
- **Checkpointing**: Save progress to resume after failures
- **Dead Letter Queue**: Store failed requests for manual review
- **Error Classification**: Distinguish retryable vs non-retryable errors

### Data Quality Assurance
- **Data Validation**: Validate extracted data against expected schemas
- **Anomaly Detection**: Flag unusual metrics (negative spend, zero impressions with clicks)
- **Completeness Checks**: Verify all expected data is present
- **Consistency Checks**: Cross-validate related metrics
- **Data Freshness**: Track data age and flag stale data

## Configuration Options

### Platform Configuration
```yaml
platforms:
  meta:
    app_id: "${META_APP_ID}"
    app_secret: "${META_APP_SECRET}"
    api_version: "v19.0"
    access_token: "${META_ACCESS_TOKEN}"
    ad_accounts: ["act_123456", "act_789012"]
  
  google_ads:
    client_id: "${GOOGLE_ADS_CLIENT_ID}"
    client_secret: "${GOOGLE_ADS_CLIENT_SECRET}"
    refresh_token: "${GOOGLE_ADS_REFRESH_TOKEN}"
    customer_id: "123-456-7890"
    api_version: "v14"
  
  tiktok:
    app_id: "${TIKTOK_APP_ID}"
    secret: "${TIKTOK_SECRET}"
    access_token: "${TIKTOK_ACCESS_TOKEN}"
    advertiser_ids: ["1234567890"]
```

### Extraction Configuration
```yaml
extraction:
  date_range:
    type: "last_n_days" | "custom" | "lifetime"
    days: 7
    start_date: "2024-01-01"
    end_date: "2024-01-15"
  
  metrics:
    - "impressions"
    - "clicks"
    - "spend"
    - "conversions"
    - "ctr"
    - "cpc"
  
  breakdowns:
    - "age"
    - "gender"
    - "device"
  
  report_type: "campaign_performance" | "audience_insights" | "custom"
```

### Rate Limiting Configuration
```yaml
rate_limiting:
  meta:
    requests_per_hour: 200
    requests_per_minute: 4
    backoff_multiplier: 2
    max_retries: 5
  
  google_ads:
    requests_per_minute: 15
    concurrent_requests: 10
```

## Output Specifications

### Unified Campaign Performance Schema
```json
{
  "metadata": {
    "platform": "meta" | "google_ads" | "tiktok",
    "account_id": "act_123456",
    "extraction_timestamp": "2024-01-15T10:30:00Z",
    "date_range": {
      "start": "2024-01-08",
      "end": "2024-01-15"
    },
    "timezone": "UTC",
    "currency": "USD"
  },
  "campaigns": [
    {
      "campaign_id": "camp_123",
      "campaign_name": "Summer Sale 2024",
      "status": "active",
      "objective": "conversions",
      "budget": 1000.00,
      "spend": 750.50,
      "impressions": 125000,
      "clicks": 2500,
      "ctr": 2.0,
      "cpc": 0.30,
      "cpm": 6.00,
      "conversions": 45,
      "conversion_value": 2250.00,
      "roas": 3.0,
      "start_date": "2024-01-08",
      "end_date": null,
      "breakdowns": {
        "age": [
          {"age_range": "18-24", "impressions": 50000, "clicks": 1000}
        ],
        "gender": [
          {"gender": "male", "impressions": 60000, "clicks": 1200}
        ],
        "device": [
          {"device": "mobile", "impressions": 100000, "clicks": 2000}
        ]
      }
    }
  ],
  "summary": {
    "total_campaigns": 10,
    "total_spend": 7500.50,
    "total_impressions": 1250000,
    "total_clicks": 25000,
    "total_conversions": 450
  },
  "warnings": [
    "Some metrics for campaign 'camp_456' are estimated and may change",
    "Historical data for 'camp_789' is incomplete due to account changes"
  ]
}
```

### Success Criteria
- ✅ Successfully authenticates with all configured platforms
- ✅ Extracts campaign, ad set, and ad data with performance metrics
- ✅ Handles rate limits gracefully with automatic backoff
- ✅ Processes async report jobs and polls for completion
- ✅ Normalizes data across platforms into unified schema
- ✅ Handles timezone and currency conversions correctly
- ✅ Provides warnings for partial or estimated data
- ✅ Supports incremental extraction (only new/changed data)

## Usage Example

### Customizing for Meta
Replace `[PLATFORM]` with `meta`, configure app credentials, specify API version, and list ad account IDs. Configure which insights and breakdowns to extract.

### Customizing for Google Ads
Replace `[PLATFORM]` with `google_ads`, configure OAuth credentials, specify customer ID, and define GAQL queries for data extraction. Configure which report types to generate.

### Customizing for TikTok
Replace `[PLATFORM]` with `tiktok`, configure app credentials, specify advertiser IDs, and configure report generation parameters.

### Testing Requirements
1. **Unit Tests**: Mock API responses, test rate limit handling, timezone conversion
2. **Integration Tests**: Connect to sandbox/test accounts, verify data extraction
3. **Rate Limit Tests**: Test behavior when hitting rate limits
4. **Error Handling Tests**: Test retry logic, partial failures, API version changes
5. **Data Quality Tests**: Verify metric calculations, timezone handling, currency conversion

## Implementation Notes

- Use official SDKs: `facebook-business` for Meta, `google-ads-api` for Google Ads
- Implement comprehensive retry logic with exponential backoff
- Cache API responses where appropriate to reduce rate limit issues
- Use async/await for I/O-bound operations (API calls, report polling)
- Store tokens securely and implement automatic refresh
- Log all API requests/responses for debugging (redact sensitive data)
- Implement data validation to catch API changes early
- Consider using a message queue for large batch extractions
- Monitor API version deprecation notices and plan migrations

