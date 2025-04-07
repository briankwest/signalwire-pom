from typing import List, Optional, Union
import json

class Section:
    """
    Represents a section in the Prompt Object Model.
    
    Each section contains a title, optional body text, optional bullet points,
    and can have any number of nested subsections.
    
    Attributes:
        title (str): The name of the section.
        body (str): A paragraph of text associated with the section.
        bullets (List[str]): Bullet-pointed items.
        subsections (List[Section]): Nested sections with the same structure.
    """
    def __init__(self, title: str, *, body: str = '', bullets: Optional[List[str]] = None):
        self.title = title
        self.body = body
        self.bullets = bullets or []
        self.subsections: List['Section'] = []

    def add_body(self, body: str):
        """Add or replace the body text for this section."""
        self.body = body

    def add_bullets(self, bullets: List[str]):
        """Add bullet points to this section."""
        self.bullets.extend(bullets)

    def add_subsection(self, title: str, *, body: str = '', bullets: Optional[List[str]] = None) -> 'Section':
        """
        Add a subsection to this section.
        
        Args:
            title: The title of the subsection
            body: Optional body text for the subsection
            bullets: Optional list of bullet points
            
        Returns:
            The newly created Section object
        """
        subsection = Section(title, body=body, bullets=bullets)
        self.subsections.append(subsection)
        return subsection

    def to_dict(self):
        """Convert the section to a dictionary representation."""
        return {
            "title": self.title,
            "body": self.body,
            "bullets": self.bullets,
            "subsections": [s.to_dict() for s in self.subsections]
        }

    def render_markdown(self, level: int = 2) -> str:
        """
        Render this section and all its subsections as markdown.
        
        Args:
            level: The heading level to start with (default: 2, which corresponds to ##)
            
        Returns:
            A string containing the markdown representation
        """
        md = [f"{'#' * level} {self.title}\n"]
        if self.body:
            md.append(f"{self.body}\n")
        for bullet in self.bullets:
            md.append(f"- {bullet}")
        if self.bullets:
            md.append("")
        for subsection in self.subsections:
            md.append(subsection.render_markdown(level + 1))
        return "\n".join(md)


class PromptObjectModel:
    """
    A structured data format for composing, organizing, and rendering prompt 
    instructions for large language models.
    
    The Prompt Object Model provides a tree-based representation of a prompt
    document composed of nested sections, each of which can include a title,
    body text, bullet points, and arbitrarily nested subsections.
    
    This class supports both machine-readability (via JSON) and structured 
    rendering (via Markdown), making it ideal for prompt templating, modular
    editing, and traceable documentation.
    """
    @staticmethod
    def from_json(json_data: Union[str, dict]) -> 'PromptObjectModel':
        """
        Create a PromptObjectModel instance from JSON data.
        
        Args:
            json_data: Either a JSON string or a parsed dictionary
            
        Returns:
            A new PromptObjectModel populated with the data from the JSON
            
        Raises:
            ValueError: If the JSON is not properly formatted
        """
        if isinstance(json_data, str):
            data = json.loads(json_data)
        else:
            data = json_data

        def build_section(d: dict) -> Section:
            if not isinstance(d, dict):
                raise ValueError("Each section must be a dictionary.")
            if 'title' not in d:
                raise ValueError("Each section must have a 'title' field.")
            if 'subsections' in d and not isinstance(d['subsections'], list):
                raise ValueError("'subsections' must be a list if provided.")
            if 'bullets' in d and not isinstance(d['bullets'], list):
                raise ValueError("'bullets' must be a list if provided.")

            section = Section(d['title'], body=d.get('body', ''), bullets=d.get('bullets', []))
            for sub in d.get('subsections', []):
                section.subsections.append(build_section(sub))
            return section

        pom = PromptObjectModel()
        for sec in data:
            pom.sections.append(build_section(sec))
        return pom

    def __init__(self):
        self.sections: List[Section] = []

    def add_section(self, title: str, *, body: str = '', bullets: Optional[List[str]] = None) -> Section:
        """
        Add a top-level section to the model.
        
        Args:
            title: The title of the section
            body: Optional body text for the section
            bullets: Optional list of bullet points
            
        Returns:
            The newly created Section object
        """
        section = Section(title, body=body, bullets=bullets)
        self.sections.append(section)
        return section

    def find_section(self, title: str) -> Optional[Section]:
        """
        Find a section by its title.
        
        Performs a recursive search through all sections and subsections.
        
        Args:
            title: The title to search for
            
        Returns:
            The Section object if found, None otherwise
        """
        def recurse(sections: List[Section]) -> Optional[Section]:
            for section in sections:
                if section.title == title:
                    return section
                found = recurse(section.subsections)
                if found:
                    return found
            return None
        return recurse(self.sections)

    def to_json(self) -> str:
        """
        Convert the entire model to a JSON string.
        
        Returns:
            A JSON string representation of the model
        """
        return json.dumps([s.to_dict() for s in self.sections], indent=2)

    def render_markdown(self) -> str:
        """
        Render the entire model as markdown.
        
        Returns:
            A string containing the markdown representation
        """
        return "\n".join([section.render_markdown() for section in self.sections]) 