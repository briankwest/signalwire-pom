# SignalWire Prompt Object Model (POM)

A lightweight Python library for structured prompt management that helps organize and manipulate prompts for large language models (LLMs).

## Installation

```bash
pip install signalwire-pom
```

## Overview

The Prompt Object Model (POM) is a structured data format and accompanying Python SDK for composing, organizing, and rendering prompt instructions for large language models. It provides a tree-based representation of a prompt document composed of nested sections, each of which can include:

* A title
* A body of explanatory or instructional text
* An optional list of bullet points
* Arbitrarily nested subsections

POM supports both machine-readability (via JSON) and structured rendering (via Markdown), making it ideal for prompt templating, modular editing, and traceable documentation.

## Benefits

Structured prompts are essential when building reliable and maintainable LLM instructions. As your prompts evolve, you may need to insert, remove, or rearrange entire sections, subsections, or even individual bullet points. POM enforces a clear hierarchy and semantic organization to ensure that prompts remain modular, auditable, and easy to extend.

### 1. Clarity and Structure

Prompts can be clearly divided into reusable sections like `Objective`, `Personality`, `Rules`, `Knowledge`, etc. Each section and subsection can carry detailed instructions and examples.

### 2. Hierarchical Nesting

Subsections allow nesting of detail and context to any depth, matching how developers and authors think about complex instructions.

### 3. Markdown Rendering

Documents can be rendered as Markdown with proper heading levels (`##`, `###`, `####`, etc.), which is useful for:
* Documentation
* Prompt review and auditing
* Version control and diffs
* Direct inclusion in LLM inputs (most modern LLMs are trained to understand and prioritize Markdown structure)

### 4. JSON Export and Import

The full prompt specification can be exported and rehydrated in JSON for use in automation, testing, and templating pipelines.

### 5. Extensible

The model is designed to be extensible and can easily incorporate metadata, tags, conditions, or versioning as needed.

## Data Structure

Each prompt document consists of a top-level list of `Section` objects. Each `Section` has the following structure:

### Section

* `title` *(str)* — The name of the section.
* `body` *(str, optional)* — A paragraph of text associated with the section.
* `bullets` *(list of str, optional)* — Bullet-pointed items.
* `subsections` *(list of Section objects)* — Nested sections with the same structure.

## Usage

```python
from signalwire_pom import PromptObjectModel

# Create a new POM
pom = PromptObjectModel()

# Add sections with content
overview = pom.add_section("Overview", body="This is an overview of the project.")
overview.add_bullets(["Point 1", "Point 2", "Point 3"])

# Add subsections
details = overview.add_subsection("Details", body="More detailed information.")
details.add_bullets(["Detail 1", "Detail 2"])

# Generate markdown
markdown = pom.render_markdown()
print(markdown)

# Generate JSON representation
json_data = pom.to_json()
print(json_data)

# Create from JSON
json_string = '''
[
  {
    "title": "Section from JSON",
    "body": "This section was created from JSON",
    "bullets": ["Bullet 1", "Bullet 2"],
    "subsections": [
      {
        "title": "Subsection from JSON",
        "body": "This subsection was created from JSON",
        "bullets": ["Sub-bullet 1", "Sub-bullet 2"],
        "subsections": []
      }
    ]
  }
]
'''
loaded_pom = PromptObjectModel.from_json(json_string)
print(loaded_pom.render_markdown())
```

## Example JSON Representation

```json
{
  "title": "Objective",
  "body": "Define the LLM's purpose in this interaction.",
  "bullets": ["Summarize clearly", "Answer efficiently"],
  "subsections": [
    {
      "title": "Main Goal",
      "body": "Provide helpful and concise answers tailored to user intent.",
      "bullets": [],
      "subsections": []
    }
  ]
}
```

## Example Markdown Output

```markdown
## Objective

Define the LLM's purpose in this interaction.

- Summarize clearly
- Answer efficiently

### Main Goal

Provide helpful and concise answers tailored to user intent.
```

## Features

- Create structured hierarchical prompts
- Add sections, subsections, body text, and bullet points
- Export to markdown or JSON
- Import from JSON
- Find sections by title

## Intended Use Cases

- Designing modular prompt templates
- Explaining prompt logic to collaborators
- Embedding structured prompt metadata in software systems
- Managing evolving prompt strategies across products

## License

MIT 