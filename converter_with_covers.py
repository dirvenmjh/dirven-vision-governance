#!/usr/bin/env python3
"""
Create single DOCX with front/back covers
"""

import os
from pathlib import Path
from zipfile import ZipFile
from io import BytesIO

LOCAL_DIR = Path("c:/hashtag1")
OUTPUT_DIR = LOCAL_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

VOLUMES = [
    "Dirvens_Vision_Volume_I.md",
    "Dirvens_Vision_Volume_II.md",
    "Dirvens_Vision_Volume_III.md",
    "Dirvens_Vision_Volume_IV.md",
    "Dirvens_Vision_Volume_V.md",
    "Dirvens_Vision_Volume_VI.md",
    "Dirvens_Vision_Volume_VII.md",
    "COMPLETE_DIRVEN_NARRATIVE.md"
]

def escape_xml(text):
    """Escape XML special characters"""
    if not text:
        return ""
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&apos;')

def create_front_cover():
    """Create front cover XML"""
    return """        <w:p>
            <w:pPr>
                <w:spacing w:line="480"/>
            </w:pPr>
        </w:p>
        <w:p>
            <w:pPr>
                <w:spacing w:line="480"/>
            </w:pPr>
        </w:p>
        <w:p>
            <w:pPr>
                <w:spacing w:line="480"/>
            </w:pPr>
        </w:p>
        <w:p>
            <w:pPr>
                <w:jc w:val="center"/>
                <w:spacing w:line="480"/>
            </w:pPr>
            <w:r>
                <w:rPr>
                    <w:b/>
                    <w:sz w:val="64"/>
                </w:rPr>
                <w:t>DIRVEN'S VISION</w:t>
            </w:r>
        </w:p>
        <w:p>
            <w:pPr>
                <w:jc w:val="center"/>
                <w:spacing w:line="240"/>
            </w:pPr>
            <w:r>
                <w:rPr>
                    <w:sz w:val="32"/>
                </w:rPr>
                <w:t>Complete Collection</w:t>
            </w:r>
        </w:p>
        <w:p>
            <w:pPr>
                <w:spacing w:line="480"/>
            </w:pPr>
        </w:p>
        <w:p>
            <w:pPr>
                <w:spacing w:line="480"/>
            </w:pPr>
        </w:p>
        <w:p>
            <w:pPr>
                <w:jc w:val="center"/>
                <w:spacing w:line="240"/>
            </w:pPr>
            <w:r>
                <w:rPr>
                    <w:sz w:val="28"/>
                </w:rPr>
                <w:t>Volumes I - VII</w:t>
            </w:r>
        </w:p>
        <w:p>
            <w:pPr>
                <w:pageBreakBefore/>
            </w:pPr>
        </w:p>
"""

def create_back_cover():
    """Create back cover XML"""
    return """        <w:p>
            <w:pPr>
                <w:spacing w:line="480"/>
            </w:pPr>
        </w:p>
        <w:p>
            <w:pPr>
                <w:spacing w:line="480"/>
            </w:pPr>
        </w:p>
        <w:p>
            <w:pPr>
                <w:jc w:val="center"/>
                <w:spacing w:line="480"/>
            </w:pPr>
            <w:r>
                <w:rPr>
                    <w:b/>
                    <w:sz w:val="48"/>
                </w:rPr>
                <w:t>DIRVEN'S VISION</w:t>
            </w:r>
        </w:p>
        <w:p>
            <w:pPr>
                <w:jc w:val="center"/>
                <w:spacing w:line="240"/>
            </w:pPr>
            <w:r>
                <w:rPr>
                    <w:sz w:val="32"/>
                </w:rPr>
                <w:t>A Complete Narrative Journey</w:t>
            </w:r>
        </w:p>
        <w:p>
            <w:pPr>
                <w:spacing w:line="480"/>
            </w:pPr>
        </w:p>
        <w:p>
            <w:pPr>
                <w:jc w:val="center"/>
                <w:spacing w:line="240"/>
            </w:pPr>
            <w:r>
                <w:rPr>
                    <w:sz w:val="28"/>
                </w:rPr>
                <w:t>All Seven Volumes Combined</w:t>
            </w:r>
        </w:p>
"""

def process_markdown_to_xml(md_file):
    """Convert markdown content to Word XML"""
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    xml_content = ""
    lines = content.split('\n')
    
    for line in lines:
        if line.startswith('# '):
            title = line[2:].strip()
            xml_content += f"""        <w:p>
            <w:pPr>
                <w:pStyle w:val="Heading1"/>
                <w:pageBreakBefore/>
                <w:sz w:val="48"/>
            </w:pPr>
            <w:r>
                <w:rPr>
                    <w:b/>
                    <w:sz w:val="48"/>
                </w:rPr>
                <w:t>{escape_xml(title)}</w:t>
            </w:r>
        </w:p>
"""
        elif line.startswith('## '):
            heading = line[3:].strip()
            xml_content += f"""        <w:p>
            <w:pPr>
                <w:pStyle w:val="Heading2"/>
                <w:sz w:val="28"/>
            </w:pPr>
            <w:r>
                <w:rPr>
                    <w:b/>
                    <w:sz w:val="28"/>
                </w:rPr>
                <w:t>{escape_xml(heading)}</w:t>
            </w:r>
        </w:p>
"""
        elif line.startswith('### '):
            heading = line[4:].strip()
            xml_content += f"""        <w:p>
            <w:pPr>
                <w:pStyle w:val="Heading3"/>
            </w:pPr>
            <w:r>
                <w:rPr>
                    <w:b/>
                </w:rPr>
                <w:t>{escape_xml(heading)}</w:t>
            </w:r>
        </w:p>
"""
        elif line.startswith('- '):
            item = line[2:].strip()
            xml_content += f"""        <w:p>
            <w:pPr>
                <w:pStyle w:val="ListBullet"/>
            </w:pPr>
            <w:r>
                <w:t>{escape_xml(item)}</w:t>
            </w:r>
        </w:p>
"""
        elif line.startswith('> '):
            quote = line[2:].strip()
            xml_content += f"""        <w:p>
            <w:pPr>
                <w:pStyle w:val="IntenseQuote"/>
                <w:ind w:left="720"/>
            </w:pPr>
            <w:r>
                <w:rPr>
                    <w:i/>
                </w:rPr>
                <w:t>{escape_xml(quote)}</w:t>
            </w:r>
        </w:p>
"""
        elif line.strip():
            xml_content += f"""        <w:p>
            <w:r>
                <w:t>{escape_xml(line)}</w:t>
            </w:r>
        </w:p>
"""
        else:
            xml_content += """        <w:p/>
"""
    
    return xml_content

def create_docx_template(doc_xml):
    """Create DOCX file structure"""
    docx = BytesIO()
    
    with ZipFile(docx, 'w') as z:
        z.writestr('[Content_Types].xml', '''<?xml version="1.0"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
    <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
    <Default Extension="xml" ContentType="application/xml"/>
    <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
</Types>''')
        
        z.writestr('_rels/.rels', '''<?xml version="1.0"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
    <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>''')
        
        z.writestr('word/document.xml', doc_xml)
    
    return docx.getvalue()

def create_complete_docx():
    """Create single DOCX with all volumes, front and back covers"""
    
    docx_content = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" 
            xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
    <w:body>
"""
    
    # Add front cover
    docx_content += create_front_cover()
    
    # Add all volumes
    for vol_file in VOLUMES:
        file_path = LOCAL_DIR / vol_file
        if file_path.exists():
            print(f"  Processing: {vol_file}")
            docx_content += process_markdown_to_xml(file_path)
    
    # Add back cover
    docx_content += create_back_cover()
    
    # Close document
    docx_content += """    </w:body>
</w:document>"""
    
    # Create DOCX file
    output_path = OUTPUT_DIR / "Dirvens_Vision_Complete.docx"
    docx_template = create_docx_template(docx_content)
    
    with open(output_path, 'wb') as f:
        f.write(docx_template)
    
    return output_path

def main():
    print("=" * 60)
    print("CREATING COMPLETE DOCX WITH COVERS")
    print("=" * 60 + "\n")
    
    try:
        output_path = create_complete_docx()
        print("\n" + "=" * 60)
        print(f"[+] Success: Dirvens_Vision_Complete.docx")
        print(f"[+] Location: {output_path}")
        print("=" * 60)
    except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == "__main__":
    main()
