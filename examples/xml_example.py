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
