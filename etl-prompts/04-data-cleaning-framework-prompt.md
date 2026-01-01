# Data Cleaning & Normalization Framework

## Context

Real-world data is messy. It arrives with inconsistent formats, encoding issues, missing values represented in a dozen different ways, and type mismatches that break downstream processing. A "date" field might contain "2024-01-15", "01/15/2024", "January 15, 2024", or "NULL". A "phone" field might have "(555) 123-4567", "555-123-4567", "+1 555 123 4567", or just "5551234567".

The challenge isn't just cleaning the data—it's doing so without losing information, handling edge cases gracefully, and providing transparency about what changed. Your framework must handle the reality that "customer_id" might be a string in one system and an integer in another, that dates are ambiguous (MM/DD vs DD/MM), and that encoding issues can corrupt entire fields.

## Core Functionality

Build a production-ready data cleaning and normalization framework with the following capabilities:

### String Normalization
- **Whitespace Handling**: Trim leading/trailing whitespace, normalize internal whitespace
- **Case Normalization**: Convert to uppercase, lowercase, or title case
- **Character Normalization**: Remove special characters, normalize Unicode (NFD/NFC)
- **Pattern Matching**: Extract patterns (emails, phone numbers, URLs) and normalize formats
- **Encoding Detection**: Auto-detect character encoding (UTF-8, Latin-1, Windows-1252)
- **Encoding Conversion**: Convert between encodings with error handling

### Type Inference & Coercion
- **Automatic Type Detection**: Infer data types from values (int, float, bool, date, string)
- **Type Coercion**: Safely convert between types with validation
- **Null Detection**: Identify null values across multiple representations
- **Type Validation**: Validate values match expected types before coercion
- **Type Preservation**: Preserve original type when coercion fails

### Date/Time Parsing
- **Multiple Format Support**: Parse dates in various formats (ISO 8601, US, European, etc.)
- **Format Detection**: Auto-detect date format from sample data
- **Ambiguity Resolution**: Handle ambiguous dates (MM/DD vs DD/MM) with configuration
- **Timezone Handling**: Parse timezone-aware and timezone-naive timestamps
- **Relative Dates**: Parse relative dates ("yesterday", "last week", "3 months ago")
- **Invalid Date Handling**: Gracefully handle invalid dates with configurable strategies

### Null Value Handling
- **Null Detection**: Identify null values: `NULL`, `""`, `"N/A"`, `"null"`, `"-"`, `"NONE"`, `None`, `NaN`
- **Null Standardization**: Convert all null representations to a single standard (None, null, or empty string)
- **Null Strategy**: Configurable strategies (keep null, fill with default, drop record, flag for review)
- **Null Propagation**: Handle nulls in calculations and aggregations

### Data Validation
- **Rule-Based Validation**: Validate data against custom rules (regex, ranges, enums)
- **Schema Validation**: Validate against JSON Schema or similar
- **Cross-Field Validation**: Validate relationships between fields
- **Business Rule Validation**: Apply domain-specific validation rules
- **Validation Reporting**: Report all validation failures with context

### Data Quality Scoring
- **Completeness**: Calculate percentage of non-null values per field
- **Consistency**: Measure format consistency across records
- **Accuracy**: Flag values that don't match expected patterns
- **Uniqueness**: Detect duplicate values
- **Timeliness**: Check data freshness (for time-series data)
- **Overall Quality Score**: Composite score across all dimensions

## Edge Cases

### Encoding Nightmares
- **Mixed Encodings**: Same field containing UTF-8 and Latin-1 characters
- **BOM Issues**: Byte Order Mark causing parsing issues
- **Invalid Byte Sequences**: Corrupted data with invalid UTF-8 sequences
- **Character Replacement**: Special characters replaced with question marks or boxes
- **Encoding Guessing**: Wrong encoding detection leading to mojibake

### Date Ambiguity
- **MM/DD vs DD/MM**: "01/02/2024" could be January 2 or February 1
- **Year Abbreviation**: "01/15/24" vs "01/15/2024"
- **Missing Components**: Dates missing day, month, or year
- **Invalid Dates**: "February 30" or "13/25/2024"
- **Multiple Formats**: Same dataset with dates in different formats
- **Timezone Confusion**: Dates with and without timezone information

### Null Representation Chaos
- **String "NULL"**: The string "NULL" vs actual null value
- **Empty Strings**: "" vs None vs " " (space)
- **Special Values**: "N/A", "NONE", "-", "TBD", "Unknown"
- **Numeric Nulls**: 0, -1, 999999 used as null placeholders
- **Whitespace-Only**: Fields containing only whitespace

### Type Coercion Issues
- **Scientific Notation**: "1.23e+10" in string fields
- **Formatted Numbers**: "1,234.56" vs "1234.56" vs "1.234,56"
- **Boolean Ambiguity**: "true", "True", "TRUE", "1", "yes", "Y"
- **Mixed Types**: Field containing both strings and numbers
- **Overflow**: Numbers exceeding type limits (int32, float precision)

### Unicode Normalization
- **Accented Characters**: "café" vs "cafe\u0301" (different Unicode representations)
- **Special Spaces**: Regular space vs non-breaking space vs zero-width space
- **Emoji**: Emoji in text fields causing encoding issues
- **Control Characters**: Invisible control characters breaking parsing

## Resilience Patterns

### Graceful Degradation
- **Keep Original**: When cleaning fails, keep original value and flag issue
- **Partial Cleaning**: Clean what can be cleaned, leave rest for manual review
- **Fallback Strategies**: Try multiple cleaning strategies, use best result
- **Error Recovery**: Continue processing other fields when one field fails

### Validation with Warnings
- **Non-Blocking Validation**: Warn about issues but don't stop processing
- **Severity Levels**: Classify issues as errors, warnings, or info
- **Validation Reports**: Generate detailed reports of all validation issues
- **Configurable Strictness**: Strict mode (fail on errors) vs lenient mode (warn and continue)

### Data Quality Metrics
- **Field-Level Metrics**: Completeness, consistency, accuracy per field
- **Record-Level Metrics**: Overall quality score per record
- **Dataset-Level Metrics**: Aggregate quality metrics for entire dataset
- **Trend Analysis**: Track quality metrics over time
- **Quality Thresholds**: Flag datasets below quality thresholds

### Audit Trail
- **Transformation Log**: Log all transformations applied to each field
- **Before/After Values**: Record original and cleaned values
- **Transformation Rules**: Document which rules were applied
- **Quality Scores**: Record quality scores at each cleaning stage
- **Manual Review Queue**: Flag records needing manual review

## Configuration Options

### Cleaning Rules Configuration
```yaml
cleaning_rules:
  strings:
    trim_whitespace: true
    normalize_whitespace: true
    case: "lower" | "upper" | "title" | "preserve"
    remove_special_chars: false
    unicode_normalization: "NFC" | "NFD" | "none"
  
  dates:
    formats:
      - "YYYY-MM-DD"
      - "MM/DD/YYYY"
      - "DD.MM.YYYY"
      - "YYYYMMDD"
    ambiguous_format_preference: "US" | "European" | "ISO"
    timezone: "UTC"
    invalid_date_strategy: "keep_original" | "set_null" | "flag_error"
  
  nulls:
    representations: ["NULL", "N/A", "", "-", "NONE", "null", "None"]
    standard_value: null
    strategy: "standardize" | "keep_original" | "fill_default"
    default_values:
      string: ""
      number: 0
      date: null
  
  encoding:
    detection: true
    default: "utf-8"
    fallback: "latin-1"
    error_handling: "replace" | "ignore" | "strict"
```

### Validation Rules Configuration
```yaml
validation:
  rules:
    - field: "email"
      type: "email"
      required: true
    
    - field: "phone"
      pattern: "^\\+?[1-9]\\d{1,14}$"
      required: false
    
    - field: "age"
      type: "integer"
      min: 0
      max: 150
    
    - field: "price"
      type: "float"
      min: 0
  
  mode: "strict" | "lenient"
  on_error: "fail" | "warn" | "log"
```

### Quality Scoring Configuration
```yaml
quality_scoring:
  enabled: true
  weights:
    completeness: 0.3
    consistency: 0.2
    accuracy: 0.2
    uniqueness: 0.15
    timeliness: 0.15
  
  thresholds:
    warning: 0.7
    error: 0.5
```

## Output Specifications

### Cleaned Dataset with Metadata
```json
{
  "metadata": {
    "source": "raw_customers.csv",
    "cleaned_at": "2024-01-15T10:30:00Z",
    "records_processed": 1000,
    "records_failed": 5,
    "transformations_applied": 15,
    "quality_score": 0.92
  },
  "records": [
    {
      "customer_id": "CUST001",
      "name": "john doe",
      "email": "john.doe@example.com",
      "phone": "+15551234567",
      "created_date": "2024-01-15",
      "_cleaning_metadata": {
        "original_name": "  John Doe  ",
        "original_phone": "(555) 123-4567",
        "transformations": [
          {"field": "name", "action": "trim_whitespace"},
          {"field": "name", "action": "lowercase"},
          {"field": "phone", "action": "normalize_phone"}
        ],
        "quality_score": 0.95
      }
    }
  ],
  "quality_metrics": {
    "completeness": 0.98,
    "consistency": 0.95,
    "accuracy": 0.90,
    "uniqueness": 0.99,
    "timeliness": 0.85
  },
  "errors": [
    {
      "record_index": 42,
      "field": "email",
      "error": "Invalid email format",
      "original_value": "not-an-email",
      "severity": "error"
    }
  ],
  "warnings": [
    {
      "record_index": 123,
      "field": "date",
      "warning": "Ambiguous date format, assuming MM/DD/YYYY",
      "original_value": "01/02/2024",
      "severity": "warning"
    }
  ]
}
```

### Transformation Log
```json
{
  "transformation_log": [
    {
      "timestamp": "2024-01-15T10:30:01Z",
      "record_index": 0,
      "field": "name",
      "transformation": "trim_whitespace",
      "before": "  John Doe  ",
      "after": "John Doe",
      "success": true
    },
    {
      "timestamp": "2024-01-15T10:30:02Z",
      "record_index": 0,
      "field": "phone",
      "transformation": "normalize_phone",
      "before": "(555) 123-4567",
      "after": "+15551234567",
      "success": true
    }
  ]
}
```

### Success Criteria
- ✅ Successfully cleans and normalizes data according to configuration
- ✅ Handles all specified edge cases gracefully
- ✅ Provides detailed transformation logs and quality metrics
- ✅ Preserves original data when cleaning fails (graceful degradation)
- ✅ Validates data against rules and reports all issues
- ✅ Generates quality scores at field, record, and dataset levels
- ✅ Processes large datasets (100K+ records) efficiently
- ✅ Supports incremental cleaning (only process new/changed records)

## Usage Example

### Customizing Cleaning Rules
Replace `[FIELD_NAME]` with your field names and specify cleaning rules. For dates, specify format preferences based on your data source region. For nulls, list all null representations found in your data.

### Customizing Validation Rules
Define validation rules for each field: required fields, type constraints, pattern matching, range validation. Set validation mode (strict vs lenient) based on your use case.

### Testing Requirements
1. **Unit Tests**: Test each cleaning function with edge cases
2. **Integration Tests**: Test full cleaning pipeline on sample datasets
3. **Edge Case Tests**: Test encoding issues, ambiguous dates, null representations
4. **Performance Tests**: Test on large datasets, measure processing time
5. **Quality Tests**: Verify quality scores are calculated correctly

## Implementation Notes

- Use libraries: `chardet` for encoding detection, `dateutil` for date parsing, `phonenumbers` for phone normalization
- Implement caching for compiled regex patterns and date format parsers
- Use pandas or polars for efficient data processing on large datasets
- Implement parallel processing for independent field cleaning
- Store transformation logs in a queryable format (database, parquet)
- Consider using schema evolution tools (Great Expectations, Pandera) for validation
- Implement incremental cleaning by tracking which records have been cleaned
- Use type hints and data classes for better code maintainability

