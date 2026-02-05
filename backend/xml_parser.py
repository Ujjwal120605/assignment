import xml.etree.ElementTree as ET
import re

class XMLParser:
    def __init__(self, xml_content):
        self.root = ET.fromstring(xml_content)

    def parse_bounds(self, bounds_str):
        """Converts '[x1,y1][x2,y2]' to center coordinates (x, y)."""
        pattern = r"\[(\d+),(\d+)\]\[(\d+),(\d+)\]"
        match = re.search(pattern, bounds_str)
        if match:
            x1, y1, x2, y2 = map(int, match.groups())
            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2
            return center_x, center_y, x1, y1, x2, y2
        return None

    def find_elements(self):
        """Recursively parses XML to find interactive elements."""
        elements = []

        for node in self.root.iter():
            if 'bounds' not in node.attrib:
                continue
            
            bounds = node.attrib['bounds']
            parsed_bounds = self.parse_bounds(bounds)
            if not parsed_bounds:
                continue
            
            center_x, center_y, _, _, _, _ = parsed_bounds
            
            # Extract useful attributes
            text = node.attrib.get('text', '')
            content_desc = node.attrib.get('content-desc', '')
            resource_id = node.attrib.get('resource-id', '')
            class_name = node.attrib.get('class', '')
            clickable = node.attrib.get('clickable', 'false') == 'true'
            editable = node.attrib.get('editable', 'false') == 'true' or class_name.endswith('EditText')

            # We care about elements that have some content or are interactive
            if text or content_desc or clickable or editable:
                elements.append({
                    "text": text,
                    "content_desc": content_desc,
                    "resource_id": resource_id,
                    "class": class_name,
                    "bounds": bounds,
                    "center": (center_x, center_y),
                    "clickable": clickable,
                    "editable": editable
                })
        
        return elements

    def find_element_by_text(self, target_text):
        """Finds an element containing the target text (case-insensitive)."""
        target_text = target_text.lower()
        elements = self.find_elements()
        for el in elements:
            if target_text in el['text'].lower() or target_text in el['content_desc'].lower():
                return el
        return None
