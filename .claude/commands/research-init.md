---
description: Initialize a new research thesis with complete directory structure and metadata
tools: Write, Bash, Read
---

# researcher-init

Initialize a new research thesis project following the Post-Database Era program methodology.

## Usage
```
/research-init "<thesis statement>"
```

## Example
```
/research-init "In distributed systems, storage-first architectures will dominate compute-first by 2027 because of cost efficiency in HTAP workloads, leading to 60% reduction in TCO for analytics workloads by Q4 2027"
```

## Implementation

When invoked, execute the following steps:

### 1. Parse and Validate Thesis Statement

Extract components from the thesis statement using the template:
- **Scope**: The domain or context (e.g., "distributed systems")
- **Subject**: What will change (e.g., "storage-first architectures")
- **Change**: Specific transformation (e.g., "will dominate compute-first")
- **Mechanism**: Why it will happen (e.g., "cost efficiency in HTAP workloads")
- **Consequence**: Observable outcome (e.g., "60% reduction in TCO")
- **Timeline**: When it will occur (e.g., "by Q4 2027")

### 2. Generate Thesis Slug

Create a URL-safe slug from the subject and key mechanism:
- Convert to lowercase
- Replace spaces with hyphens
- Remove special characters
- Limit to 50 characters
- Example: "storage-first-htap-cost"

### 3. Create Directory Structure

```bash
# Create main thesis directory
mkdir -p theses/${THESIS_SLUG}

# Create all required subdirectories
mkdir -p theses/${THESIS_SLUG}/research
mkdir -p theses/${THESIS_SLUG}/notes
mkdir -p theses/${THESIS_SLUG}/lit-scans
mkdir -p theses/${THESIS_SLUG}/opinion
mkdir -p theses/${THESIS_SLUG}/figures
mkdir -p theses/${THESIS_SLUG}/datasets

```

### 5. Create Initial Metadata Files

Create `theses/${THESIS_SLUG}/meta.yaml` for the thesis root:

```yaml
# Thesis-level metadata
title: "${THESIS_TITLE}"
thesis: "${THESIS_SLUG}"
artifact: "thesis-root"
version: "1.0"
status: "active"
authors: ["Patrick McFadin"]
created: "${CURRENT_DATE}"
updated: "${CURRENT_DATE}"
license: "CC-BY-4.0"
keywords: [${EXTRACTED_KEYWORDS}]

```

### 6. Create README.md

Generate `theses/${THESIS_SLUG}/README.md`:

```markdown
# ${THESIS_TITLE}

## Thesis Statement
> ${FULL_THESIS_STATEMENT}

## Directory Structure
- `research/` - Deep research reports and PDFs
- `notes/` - Working notes and synthesis documents
- `lit-scans/` - Literature scans and recency checks
- `opinion/` - Essays and white papers
- `figures/` - Charts, diagrams, and visualizations
- `datasets/` - Data tables and CSVs
- `drafts/` - Work in progress documents
- `inbox/` - Intake drop zone for new materials

## Evidence Standards
- Major claims require ≥2 Tier A/B sources
- All artifacts must include counterevidence sections
- Chicago-style citations required
- Maximum 15-word quotes from sources

```

### 7. Create research prompt
In the `research/` directory, create a file called "prompt.md"

In that file put the following 
```
You are a research strategist. Draft bullet-level research questions that,
if answered, would confirm or falsify each sub-theme of: {THESIS}.

Create a file named outline_YYYY-MM-DD.md where YYYY-MM-DD is todays date.
In that file output: Markdown list, grouped by sub-theme, ≤120 chars per bullet.

```

Change the cwd to the new directory and await the next command. 

Output to user what directory you are in and that you are awaiting the next command. 

## Error Handling

- If thesis statement doesn't match expected template, prompt for clarification
- If directory already exists, ask whether to overwrite or create versioned directory
- Validate that all required components are present before proceeding
- Ensure all YAML files are valid before writing
