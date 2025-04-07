from typing import List, Optional, Union
import json

class Section:
    def __init__(self, title: str, *, body: str = '', bullets: Optional[List[str]] = None):
        self.title = title
        self.body = body
        self.bullets = bullets or []
        self.subsections: List['Section'] = []

    def add_body(self, body: str):
        self.body = body

    def add_bullets(self, bullets: List[str]):
        self.bullets.extend(bullets)

    def add_subsection(self, title: str, *, body: str = '', bullets: Optional[List[str]] = None) -> 'Section':
        subsection = Section(title, body=body, bullets=bullets)
        self.subsections.append(subsection)
        return subsection

    def to_dict(self):
        return {
            "title": self.title,
            "body": self.body,
            "bullets": self.bullets,
            "subsections": [s.to_dict() for s in self.subsections]
        }

    def render_markdown(self, level: int = 2) -> str:
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
    @staticmethod
    def from_json(json_data: Union[str, dict]) -> 'PromptObjectModel':
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
        section = Section(title, body=body, bullets=bullets)
        self.sections.append(section)
        return section

    def find_section(self, title: str) -> Optional[Section]:
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
        return json.dumps([s.to_dict() for s in self.sections], indent=2)

    def render_markdown(self) -> str:
        return "\n".join([section.render_markdown() for section in self.sections]) 