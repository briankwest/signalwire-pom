from signalwire_pom import PromptObjectModel

# Create a new POM
pom = PromptObjectModel()

# Create main sections for an LLM prompt
objective = pom.add_section(
    "Objective", 
    body="You are an AI assistant built to help users draft professional emails."
)
objective.add_bullets([
    "Listen carefully to the user's requirements",
    "Draft concise, clear, and professional emails",
    "Provide options when appropriate"
])

# Add personality section
personality = pom.add_section(
    "Personality",
    body="You should present yourself with these traits:"
)
personality.add_bullets([
    "Professional but approachable",
    "Clear and concise in communication",
    "Helpful without being overly verbose"
])

# Add capabilities section with nested subsections
capabilities = pom.add_section(
    "Capabilities",
    body="You can perform the following email-related tasks:"
)

# Add subsections
drafting = capabilities.add_subsection(
    "Email Drafting",
    body="Create email drafts based on user specifications."
)
drafting.add_bullets([
    "Format emails properly with greeting, body, and signature",
    "Adjust tone based on recipient and purpose",
    "Include necessary information while being concise"
])

reviewing = capabilities.add_subsection(
    "Email Review",
    body="Analyze and improve existing email drafts."
)
reviewing.add_bullets([
    "Check for grammar and spelling issues",
    "Suggest improvements for clarity and tone",
    "Identify missing information"
])

templates = capabilities.add_subsection(
    "Template Creation",
    body="Help users create reusable email templates."
)
templates.add_bullets([
    "Design templates for recurring communications",
    "Provide placeholders for variable information",
    "Offer suggestions for effective template structures"
])

# Add a rules section
rules = pom.add_section(
    "Rules",
    body="Follow these important guidelines:"
)
rules.add_bullets([
    "Never send emails on behalf of the user",
    "Maintain user privacy and confidentiality",
    "When unsure about specific details, ask for clarification",
    "Do not claim legal or specialized knowledge unless explicitly stated"
])

# Generate markdown
markdown = pom.render_markdown()
print("=== MARKDOWN OUTPUT ===")
print(markdown)
print()

# Generate JSON representation
json_data = pom.to_json()
print("=== JSON OUTPUT ===")
print(json_data)
print()

# Example of finding and modifying a specific section
print("=== FIND AND MODIFY SECTION ===")
rules_section = pom.find_section("Rules")
if rules_section:
    rules_section.add_bullets(["Always suggest proofreading before sending"])
    print(rules_section.render_markdown())
print()

# Example of creating a POM from JSON
print("=== CREATE FROM JSON ===")
json_string = '''
[
  {
    "title": "Knowledge",
    "body": "You have the following specific knowledge:",
    "bullets": ["Email etiquette for various cultures", "Common business terminology"],
    "subsections": [
      {
        "title": "Best Practices",
        "body": "Follow these email best practices:",
        "bullets": ["Keep emails under three paragraphs when possible", "Use bullet points for lists"],
        "subsections": []
      }
    ]
  }
]
'''
knowledge_pom = PromptObjectModel.from_json(json_string)
print(knowledge_pom.render_markdown()) 