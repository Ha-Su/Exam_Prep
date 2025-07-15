import pathlib
from docling.document_converter import DocumentConverter

# Paths
in_dir  = pathlib.Path("slides_pdfs")
out_dir = pathlib.Path("slides_md")
out_dir.mkdir(exist_ok=True)

# Initialize once
converter = DocumentConverter()

for pdf_path in in_dir.glob("*.pdf"):
    # convert
    result = converter.convert(str(pdf_path))
    md_text = result.document.export_to_markdown()
    # write
    md_path = out_dir / (pdf_path.stem + ".md")
    md_path.write_text(md_text, encoding="utf-8")
    print(f"Converted {pdf_path.name} → {md_path.name}")
