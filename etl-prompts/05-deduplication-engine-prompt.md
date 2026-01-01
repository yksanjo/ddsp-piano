# Deduplication Engine

## Context

Duplicate records are the bane of data quality. They appear in every dataset: customer records with slight name variations ("John Smith" vs "J. Smith" vs "John A. Smith"), product listings with different formatting, transaction records that were imported twice. The challenge isn't just finding duplicates—it's distinguishing between true duplicates (same entity) and false positives (different entities with similar attributes).

Real-world duplicates are subtle. Two records might be the same customer with a typo in the email, a different phone format, or a name change (marriage, legal name change). Or they might be different customers with similar names living at the same address (family members). Your deduplication engine must handle these nuances while providing confidence scores and supporting manual review.

## Core Functionality

Build a production-ready deduplication engine with the following capabilities:

### Fuzzy String Matching
- **Levenshtein Distance**: Calculate edit distance between strings
- **Jaro-Winkler Similarity**: Optimized for names and short strings
- **Token-Based Matching**: Compare sets of tokens (words) rather than full strings
- **N-Gram Matching**: Compare character n-grams for partial matches
- **Configurable Thresholds**: Set similarity thresholds per field and overall

### Phonetic Matching
- **Soundex**: Phonetic algorithm for English names
- **Metaphone/Double Metaphone**: Improved phonetic matching
- **Match Rating Approach**: Alternative phonetic algorithm
- **Language Support**: Support for multiple languages

### Record Comparison
- **Multi-Field Comparison**: Compare records across multiple fields
- **Field Weighting**: Assign importance weights to different fields
- **Composite Scoring**: Combine similarity scores from multiple fields
- **Blocking**: Pre-filter candidate pairs using exact matches on key fields
- **Indexing**: Use inverted indexes for efficient candidate generation

### Merge Strategies
- **Keep Latest**: Use most recent record as master
- **Merge Fields**: Combine non-conflicting fields from all duplicates
- **Conflict Resolution**: Handle conflicting values with configurable rules
- **User Review**: Flag conflicts for manual review
- **Audit Trail**: Track all merge decisions and original values

### Entity Resolution
- **Entity Clustering**: Group duplicate records into entity clusters
- **Canonical Record**: Generate canonical record from cluster
- **Relationship Tracking**: Track relationships between entities
- **Temporal Resolution**: Handle same entity at different points in time

## Edge Cases

### False Positives
- **Similar Names, Different People**: "John Smith" and "Jon Smith" might be different people
- **Family Members**: Same address, similar names, but different entities
- **Business vs Personal**: Same name, different contexts (business vs personal account)
- **Common Names**: Very common names causing many false matches
- **Initials vs Full Names**: "J. Smith" vs "John Smith" vs "James Smith"

### False Negatives
- **Significant Variations**: Same entity with major data differences
- **Name Changes**: Legal name changes, marriage, divorce
- **Data Entry Errors**: Major typos causing low similarity scores
- **Format Differences**: Same data in completely different formats
- **Missing Fields**: Key matching fields missing from one record

### Partial Duplicates
- **Subset Relationships**: One record is subset of another
- **Overlapping Records**: Records with some shared and some unique fields
- **Hierarchical Data**: Parent-child relationships mistaken for duplicates
- **Versioned Records**: Same entity with version numbers or timestamps

### Temporal Duplicates
- **Same Entity, Different Times**: Customer record updated over time
- **Historical vs Current**: Old record vs current record of same entity
- **Snapshot Data**: Multiple snapshots of same entity at different times
- **Soft Deletes**: Deleted records that should match active records

### Data Quality Issues
- **Missing Key Fields**: Records missing fields used for matching
- **Inconsistent Formats**: Same data in different formats across records
- **Encoding Issues**: Encoding problems causing false differences
- **Abbreviations**: "St." vs "Street", "Inc." vs "Incorporated"

## Resilience Patterns

### Confidence Scoring
- **Similarity Scores**: Calculate similarity scores for each field and overall
- **Confidence Levels**: Classify matches as high/medium/low confidence
- **Threshold Configuration**: Configurable thresholds for automatic vs manual review
- **Score Explanation**: Explain why records matched (which fields, what scores)

### Manual Review Queue
- **Review Workflow**: Queue uncertain matches for human review
- **Review Interface**: Provide tools for reviewers to accept/reject matches
- **Learning from Reviews**: Use review decisions to improve matching
- **Bulk Actions**: Support bulk approve/reject for similar cases

### Merge Conflict Resolution
- **Conflict Detection**: Identify fields with conflicting values
- **Resolution Strategies**: Keep latest, keep longest, keep most complete, user choice
- **Conflict Reporting**: Report all conflicts with context
- **Merge Preview**: Show preview of merged record before applying

### Audit Trail
- **Match History**: Track all matches found and decisions made
- **Original Values**: Preserve original values before merging
- **Decision Logging**: Log all merge decisions with timestamps and users
- **Rollback Capability**: Ability to undo merges if mistakes discovered

### Performance Optimization
- **Blocking Strategies**: Reduce candidate pairs using blocking keys
- **Indexing**: Use efficient indexes for fast candidate generation
- **Parallel Processing**: Process matches in parallel for large datasets
- **Incremental Matching**: Only match new records against existing entities
- **Sampling**: Use sampling for very large datasets

## Configuration Options

### Matching Configuration
```yaml
matching:
  algorithms:
    - name: "levenshtein"
      threshold: 0.85
      fields: ["name", "address"]
    
    - name: "jaro_winkler"
      threshold: 0.90
      fields: ["name"]
    
    - name: "phonetic"
      algorithm: "metaphone"
      fields: ["name"]
  
  field_weights:
    name: 0.4
    email: 0.3
    phone: 0.2
    address: 0.1
  
  blocking:
    enabled: true
    keys:
      - ["email"]  # Exact match on email
      - ["phone"]  # Exact match on phone
      - ["name_first", "name_last"]  # Exact match on name components
```

### Merge Configuration
```yaml
merging:
  strategy: "merge_fields" | "keep_latest" | "keep_most_complete" | "user_review"
  
  conflict_resolution:
    default: "keep_latest"
    rules:
      - field: "email"
        strategy: "keep_most_recent"
      - field: "phone"
        strategy: "merge_all"  # Keep all phone numbers
  
  field_priority:
    - "email"  # Highest priority
    - "phone"
    - "address"
    - "name"
  
  confidence_thresholds:
    auto_merge: 0.95
    manual_review: 0.75
    reject: 0.50
```

### Entity Resolution Configuration
```yaml
entity_resolution:
  clustering:
    algorithm: "connected_components" | "hierarchical"
    min_similarity: 0.75
  
  canonical_record:
    strategy: "most_complete" | "most_recent" | "merge_all"
  
  temporal_handling:
    enabled: true
    time_field: "updated_at"
    max_time_diff: "30 days"  # Records within this time are more likely duplicates
```

## Output Specifications

### Deduplication Results
```json
{
  "metadata": {
    "source": "customers.csv",
    "processed_at": "2024-01-15T10:30:00Z",
    "total_records": 10000,
    "duplicate_groups": 450,
    "records_merged": 900,
    "final_record_count": 9550
  },
  "duplicate_groups": [
    {
      "group_id": "group_001",
      "canonical_record_id": "CUST123",
      "confidence": 0.92,
      "match_reason": "High similarity on name, email, and phone",
      "records": [
        {
          "record_id": "CUST123",
          "name": "John Smith",
          "email": "john.smith@example.com",
          "phone": "+15551234567",
          "status": "canonical"
        },
        {
          "record_id": "CUST456",
          "name": "J. Smith",
          "email": "john.smith@example.com",
          "phone": "+1 (555) 123-4567",
          "status": "merged",
          "similarity_score": 0.92,
          "matching_fields": {
            "email": 1.0,
            "phone": 0.95,
            "name": 0.85
          }
        }
      ],
      "merge_conflicts": [],
      "merged_record": {
        "record_id": "CUST123",
        "name": "John Smith",
        "email": "john.smith@example.com",
        "phone": ["+15551234567", "+1 (555) 123-4567"],
        "merged_at": "2024-01-15T10:30:00Z"
      }
    }
  ],
  "manual_review_queue": [
    {
      "group_id": "group_042",
      "confidence": 0.78,
      "records": ["CUST789", "CUST790"],
      "reason": "Medium confidence match, potential false positive",
      "review_priority": "high"
    }
  ],
  "statistics": {
    "high_confidence_matches": 380,
    "medium_confidence_matches": 60,
    "low_confidence_matches": 10,
    "false_positives_flagged": 5,
    "merge_conflicts": 12
  }
}
```

### Match Details
```json
{
  "match_details": {
    "record_1": "CUST123",
    "record_2": "CUST456",
    "overall_similarity": 0.92,
    "field_similarities": {
      "name": {
        "similarity": 0.85,
        "algorithm": "jaro_winkler",
        "value_1": "John Smith",
        "value_2": "J. Smith"
      },
      "email": {
        "similarity": 1.0,
        "algorithm": "exact",
        "value_1": "john.smith@example.com",
        "value_2": "john.smith@example.com"
      },
      "phone": {
        "similarity": 0.95,
        "algorithm": "normalized",
        "value_1": "+15551234567",
        "value_2": "+1 (555) 123-4567"
      }
    },
    "blocking_keys_matched": ["email"],
    "confidence": "high"
  }
}
```

### Success Criteria
- ✅ Identifies duplicate records with configurable similarity thresholds
- ✅ Handles false positives and false negatives appropriately
- ✅ Provides confidence scores and match explanations
- ✅ Supports multiple merge strategies with conflict resolution
- ✅ Queues uncertain matches for manual review
- ✅ Maintains complete audit trail of all decisions
- ✅ Processes large datasets (100K+ records) efficiently
- ✅ Supports incremental deduplication (only match new records)

## Usage Example

### Customizing Matching Rules
Replace `[FIELD_NAMES]` with your field names and configure similarity thresholds. Adjust field weights based on which fields are most reliable for matching in your domain.

### Customizing Merge Strategy
Choose merge strategy based on your use case: keep latest for transactional data, merge fields for customer data, user review for critical data.

### Testing Requirements
1. **Unit Tests**: Test each matching algorithm with known duplicates
2. **Integration Tests**: Test full deduplication pipeline on sample datasets
3. **Edge Case Tests**: Test false positives, false negatives, partial duplicates
4. **Performance Tests**: Test on large datasets, measure processing time
5. **Accuracy Tests**: Measure precision and recall against known ground truth

## Implementation Notes

- Use libraries: `rapidfuzz` or `fuzzywuzzy` for fuzzy matching, `jellyfish` for phonetic matching
- Implement efficient blocking strategies to reduce candidate pairs (O(n²) to O(n))
- Use graph algorithms (connected components) for entity clustering
- Implement parallel processing for large-scale matching
- Store match results and decisions in a database for audit trail
- Consider using machine learning for match classification (supervised learning from reviews)
- Implement incremental matching by maintaining entity index
- Use efficient data structures (inverted indexes, hash tables) for fast candidate generation

