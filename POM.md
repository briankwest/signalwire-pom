# **Prompt Object Model (POM) Specification**

## **Overview**

The Prompt Object Model (POM) is a structured data format and Python SDK for composing, organizing, and rendering prompt instructions for large language models (LLMs). It models a document as a tree of nested sections. Each section may contain:

* A `title` (optional for top-level sections, required for nested ones)  
* A `body` (string content)  
* A list of `bullets` (for itemized points)  
* A list of nested `subsections`

POM supports both machine-readability (via JSON) and structured rendering (via Markdown), making it ideal for prompt templating, modular editing, traceable documentation, and direct LLM consumption.

---

## **Why Structured Prompts Matter**

Structured prompts are essential when building reliable and maintainable LLM instructions. As your prompts evolve, you may need to insert, remove, or rearrange entire sections, subsections, or even individual bullet points. Without a clean structure, such changes can introduce inconsistencies or reduce the LLM's effectiveness due to unclear or chaotic formatting. POM enforces hierarchy and organization to keep prompts modular, traceable, and performant.

---

## **Format Details**

### **Section Object**

Each section is an object with the following fields:

| Field | Type | Required | Description |
| :---- | :---- | :---- | :---- |
| `title` | string | No (top), Yes (nested) | Heading text. Optional only at the root level. |
| `body` | string | No | Paragraph or long-form instruction text. |
| `bullets` | string\[\] | No | Bulleted list of short statements or rules. |
| `subsections` | Section\[\] | No | Nested list of sections. Each must include a `title`. |
| `numbered` | boolean | No | If true, enables heading numbering for this and all subsequent sibling sections. |
| `numberedBullets` | boolean | No | If true, bullet points in this section are numbered instead of using dashes. |

### **JSON Structure**

The entire POM document is a JSON array of top-level section objects.

---

## **JSON Schema**

```
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://example.com/pom.schema.json",
  "title": "Prompt Object Model",
  "type": "array",
  "prefixItems": [
    { "$ref": "#/$defs/topLevelSectionFirst" }
  ],
  "items": { "$ref": "#/$defs/topLevelSectionRest" },
  "$defs": {
    "sectionContent": {
      "type": "object",
      "properties": {
        "title": { "type": "string" },
        "body": { "type": "string" },
        "bullets": {
          "type": "array",
          "items": { "type": "string" }
        },
        "subsections": {
          "type": "array",
          "items": { "$ref": "#/$defs/nestedSection" }
        },
        "numbered": { "type": "boolean" },
        "numberedBullets": { "type": "boolean" }
      },
      "additionalProperties": false
    },
    "topLevelSectionFirst": {
      "allOf": [
        { "$ref": "#/$defs/sectionContent" }
      ],
      "anyOf": [
        { "required": ["body"] },
        { "required": ["bullets"] }
      ]
    },
    "topLevelSectionRest": {
      "allOf": [
        { "$ref": "#/$defs/sectionContent" },
        { "required": ["title"] }
      ],
      "anyOf": [
        { "required": ["body"] },
        { "required": ["bullets"] }
      ]
    },
    "nestedSection": {
      "allOf": [
        { "$ref": "#/$defs/sectionContent" },
        { "required": ["title"] }
      ],
      "anyOf": [
        { "required": ["body"] },
        { "required": ["bullets"] }
      ]
    }
  }
}
```

The schema above defines these validation rules:

1. A POM document is a JSON array of section objects
2. The first top-level section must have either a body or bullets, but title is optional
3. Subsequent top-level sections must have a title and either a body or bullets
4. All nested sections (subsections) must have a title and either a body or bullets
5. Each section can include optional formatting properties (numbered, numberedBullets)

---

## **Markdown Rendering**

Each section is rendered as Markdown with heading levels corresponding to its depth:

* Top-level sections (with title) are `##`  
* Subsections are `###`, `####`, etc.  
* If a section has no title (valid only at root), it renders its children at the same level  
* If `numbered` is true, each section in the current array receives an incrementing number (starting at 1). This only applies to the level at which the `numbered` key appears, and does not cascade into nested `subsections` unless they explicitly include `numbered: true`  
* If `numberedBullets` is true, bullets are shown as numbered list items (1., 2., etc.)

### **Example Input JSON**

```
[
  {
    "title": "Objective",
    "body": "Define the task.",
    "bullets": ["Be concise", "Avoid repetition"],
    "numbered": true,
    "numberedBullets": true,
    "subsections": [
      {
        "title": "Main Goal",
        "body": "Provide helpful and direct responses."
      }
    ]
  }
]
```

### **Rendered Markdown**

```
## 1 Objective

Define the task.

1. Be concise
2. Avoid repetition

### 1 Main Goal

Provide helpful and direct responses.

### 2 Edge Cases

Clarify how to handle rare or ambiguous requests.

## 2 At Start

Greet the user and explain your role.
```

---

## **XML Rendering**

POM documents can also be rendered to XML as an alternative to Markdown. This format is especially useful when your LLM is tuned to expect or parse structured XML data.

Each section becomes a `<section>` element, with optional `<title>`, `<body>`, `<bullets>`, and nested `<subsections>`. Attributes like `numbered="true"` and `numberedBullets="true"` control formatting:

* `numbered="true"` applies to the current list of sibling sections only and starts at 1 for each array.  
* It does not automatically cascade to nested subsections unless they include `numbered: true` explicitly.  
* `numberedBullets="true"` only affects the bullet points in the current section.

### **Example Input JSON**

```
[
  {
    "title": "Objective",
    "body": "Define the task.",
    "bullets": ["Be concise", "Avoid repetition"],
    "numbered": true,
    "numberedBullets": true,
    "subsections": [
      {
        "title": "Main Goal",
        "body": "Provide helpful and direct responses."
      }
    ]
  }
]
```

### **Rendered XML**

```
<prompt>
  <section>
    <title>1 Objective</title>
    <body>Define the task.</body>
    <bullets>
      <bullet id="1">Be concise</bullet>
      <bullet id="2">Avoid repetition</bullet>
    </bullets>
    <subsections>
      <section>
        <title>1 Main Goal</title>
        <body>Provide helpful and direct responses.</body>
      </section>
      <section>
        <title>2 Edge Cases</title>
        <body>Clarify how to handle rare or ambiguous requests.</body>
      </section>
    </subsections>
  </section>
  <section>
    <title>2 At Start</title>
    <body>Greet the user and explain your role.</body>
  </section>
</prompt>
```

### **Token Cost Tradeoff**

While XML is highly structured and easy for LLMs to parse, it uses significantly more input tokens than Markdown or plain text. This may impact performance or cost in token-limited environments. Choose XML rendering when structure and reliability outweigh token efficiency.

---

## **Example Usage in Python**

```py
from POM import PromptObjectModel

pom = PromptObjectModel()
section = pom.add_section(title="Objective", body="Define the LLM's purpose.")
section.add_bullets(["Summarize clearly", "Answer efficiently"])
section.add_subsection(title="Main Goal", body="Be concise and helpful.")

print(pom.render_markdown())
```

To load from JSON:

```py
with open("prompt.json", "r") as f:
    pom = PromptObjectModel.from_json(f.read())
    print(pom.render_markdown())
```

---

## **Benefits of POM**

* **Clarity**: Clearly separates different types of instructions.  
* **Scalability**: Easily add, remove, or reorder sections.  
* **Auditability**: Render Markdown for human or LLM review.  
* **Portability**: Export to or import from JSON.  
* **Safety**: Prevents accidental formatting loss or unstructured instructions.

---

The Prompt Object Model is a lightweight but powerful structure for managing rich, reusable LLM instructions.

