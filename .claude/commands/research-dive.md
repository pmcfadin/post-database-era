---
description: Execute deep research using the researcher sub-agent
tools: Read, Task
---

# researcher-dive

Execute deep research by reading a prompt file and delegating to the researcher sub-agent.

## Usage
```
/research-dive <prompt-file>
```

## Example
```
/research-dive prompt.md
/research-dive theses/storage-infrastructure/prompts/counterevidence.md
```

## Implementation

1. Read the prompt file
2. Delegate to the researcher sub-agent
3. The researcher will handle all complexity

### Execution

```
Read the file: ${promptFile}

Use the researcher sub-agent to execute the research prompt from that file.

The researcher will:
- Use Opus 4.1 for maximum capability
- Execute web searches to verify all claims
- Find counterevidence
- ULTRATHINK through the analysis
- Output in the format specified in the prompt
- Save results with proper naming convention
```

That's it. The researcher sub-agent handles everything else.