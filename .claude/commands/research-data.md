---
description: Find and collect research data on a topic
tools: Task
---

# researcher-data

Hunt for data sources on a topic and save them as CSV files with metadata.

## Usage
```
/project:researcher-data <topic>
```

## Example
```
/project:researcher-data "HTAP cost comparison"
/project:researcher-data "storage latency benchmarks"
/project:researcher-data "cloud pricing 2024-2025"
```

## Implementation

Delegate to the data-hunter sub-agent:

```
Use the data-hunter sub-agent to find and collect data about: ${topic}

The data-hunter will:
1. Search for credible data sources
2. Extract and clean the data
3. Save as CSV files in datasets/
4. Create metadata files describing each dataset
5. Generate a README listing all collected data

Focus on:
- Government and academic sources
- Industry benchmarks
- Recent data (2023-2025 preferred)
- Quantitative metrics
```

The data-hunter handles all complexity of web scraping and data organization.