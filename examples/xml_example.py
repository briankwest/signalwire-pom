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
    "Draft concise, clear, and professional emails"
])

# Add a subsection
details = objective.add_subsection(
    "Implementation Details",
    body="Follow these specific guidelines when drafting emails:"
)
details.add_bullets([
    "Use proper salutations based on the context",
    "Keep paragraphs short and focused"
])

# Generate and display XML
print("=== XML OUTPUT ===")
xml_output = pom.render_xml()
print(xml_output)
print()

# Save XML to a file
with open("prompt_template.xml", "w") as f:
    f.write(xml_output)
print("XML saved to prompt_template.xml")
print()

# Example of creating manually structured XML
print("=== CUSTOM XML INPUT ===")
custom_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<prompt>
  <section>
    <title>Configuration</title>
    <body>System configuration parameters:</body>
    <bullets>
      <bullet>Language: English</bullet>
      <bullet>Tone: Professional</bullet>
    </bullets>
    <subsections>
      <section>
        <title>Advanced Settings</title>
        <body>These settings control advanced behavior:</body>
        <bullets>
          <bullet>Response length: Medium</bullet>
          <bullet>Creativity level: Balanced</bullet>
        </bullets>
      </section>
    </subsections>
  </section>
  <section>
    <title>Instructions</title>
    <body>Follow these operational guidelines:</body>
    <bullets>
      <bullet>Always verify user intent before proceeding</bullet>
      <bullet>Provide options when multiple approaches exist</bullet>
    </bullets>
  </section>
</prompt>
'''

# Convert between formats
print("=== XML TO JSON ===")
custom_pom = PromptObjectModel.from_xml(custom_xml)
print(custom_pom.to_json())
print()

print("=== XML TO MARKDOWN ===")
print(custom_pom.render_markdown())
