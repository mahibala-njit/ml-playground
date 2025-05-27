--------- Full Python Script ---------
import fitz  # PyMuPDF
import pdfplumber
import os

def extract_text_from_pdf(pdf_path):
    text_data = []
    with fitz.open(pdf_path) as doc:
        for page_num, page in enumerate(doc, start=1):
            text = page.get_text()
            if text.strip():
                text_data.append({
                    'page': page_num,
                    'text': text.strip()
                })
    return text_data

def extract_images_from_pdf(pdf_path, image_dir="extracted_images"):
    os.makedirs(image_dir, exist_ok=True)
    image_data = []

    with fitz.open(pdf_path) as doc:
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            images = page.get_images(full=True)
            for img_index, img in enumerate(images):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                image_filename = f"page_{page_num+1}_img_{img_index+1}.{image_ext}"
                filepath = os.path.join(image_dir, image_filename)
                with open(filepath, "wb") as f:
                    f.write(image_bytes)
                image_data.append({
                    'page': page_num + 1,
                    'image_path': filepath
                })
    return image_data

def extract_tables_from_pdf(pdf_path):
    table_data = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            tables = page.extract_tables()
            for table_index, table in enumerate(tables):
                table_data.append({
                    'page': page_num,
                    'table_index': table_index + 1,
                    'table': table
                })
    return table_data

# ---------- Example Usage ----------
pdf_file_path = "your_pdf_file.pdf"

text_results = extract_text_from_pdf(pdf_file_path)
image_results = extract_images_from_pdf(pdf_file_path)
table_results = extract_tables_from_pdf(pdf_file_path)

# Output Example
print("TEXT EXTRACTED:")
for item in text_results:
    print(f"Page {item['page']}:\n{item['text'][:200]}...\n")

print("\nIMAGES EXTRACTED:")
for img in image_results:
    print(f"Page {img['page']}: {img['image_path']}")

print("\nTABLES EXTRACTED:")
for tbl in table_results:
    print(f"Page {tbl['page']} - Table {tbl['table_index']}:\n{tbl['table']}\n")

--- Markdown ---------------

import fitz  # PyMuPDF
import pdfplumber
import os

def extract_text_from_pdf(pdf_path):
    text_data = []
    with fitz.open(pdf_path) as doc:
        for page_num, page in enumerate(doc, start=1):
            text = page.get_text()
            if text.strip():
                text_data.append({'page': page_num, 'text': text.strip()})
    return text_data

def extract_images_from_pdf(pdf_path, image_dir="extracted_images"):
    os.makedirs(image_dir, exist_ok=True)
    image_data = []
    with fitz.open(pdf_path) as doc:
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            images = page.get_images(full=True)
            for img_index, img in enumerate(images):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                image_filename = f"page_{page_num+1}_img_{img_index+1}.{image_ext}"
                filepath = os.path.join(image_dir, image_filename)
                with open(filepath, "wb") as f:
                    f.write(image_bytes)
                image_data.append({'page': page_num + 1, 'image_path': filepath})
    return image_data

def extract_tables_from_pdf(pdf_path):
    table_data = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            tables = page.extract_tables()
            for table_index, table in enumerate(tables):
                table_data.append({'page': page_num, 'table_index': table_index + 1, 'table': table})
    return table_data

def table_to_markdown(table):
    if not table:
        return ""
    header = "| " + " | ".join(table[0]) + " |"
    separator = "| " + " | ".join(["---"] * len(table[0])) + " |"
    rows = "\n".join("| " + " | ".join(row) + " |" for row in table[1:])
    return f"{header}\n{separator}\n{rows}"

def export_to_markdown(text_data, image_data, table_data, output_path="output.md"):
    with open(output_path, "w", encoding="utf-8") as md:
        md.write("# PDF Content Extracted\n\n")

        # Group data by page
        all_pages = set(
            [item['page'] for item in text_data] +
            [item['page'] for item in image_data] +
            [item['page'] for item in table_data]
        )

        for page_num in sorted(all_pages):
            md.write(f"## Page {page_num}\n\n")

            # Text
            text = next((item['text'] for item in text_data if item['page'] == page_num), "")
            if text:
                md.write("### Text\n")
                md.write(text + "\n\n")

            # Images
            imgs = [img['image_path'] for img in image_data if img['page'] == page_num]
            if imgs:
                md.write("### Images\n")
                for img_path in imgs:
                    rel_path = os.path.relpath(img_path)
                    md.write(f"![Image]({rel_path})\n\n")

            # Tables
            page_tables = [t['table'] for t in table_data if t['page'] == page_num]
            if page_tables:
                md.write("### Tables\n")
                for i, table in enumerate(page_tables, 1):
                    md.write(f"**Table {i}**\n\n")
                    md.write(table_to_markdown(table) + "\n\n")

    print(f"✅ Markdown exported to `{output_path}`")

# ------------- USAGE ----------------
pdf_file_path = "your_pdf_file.pdf"

text_results = extract_text_from_pdf(pdf_file_path)
image_results = extract_images_from_pdf(pdf_file_path)
table_results = extract_tables_from_pdf(pdf_file_path)

export_to_markdown(text_results, image_results, table_results)

