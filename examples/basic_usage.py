from signalwire import PromptObjectModel

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
print("=== MARKDOWN OUTPUT ===")
print(markdown)
print()

# Generate JSON representation
json_data = pom.to_json()
print("=== JSON OUTPUT ===")
print(json_data)
print()

# Create from JSON
print("=== FROM JSON EXAMPLE ===")
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