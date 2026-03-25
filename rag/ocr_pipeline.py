import os
import pytesseract
from PIL import Image
from rag.text_pipeline import get_collection

async def ingest_ocr_folder(folder_path):
    collection = get_collection()

    for filename in os.listdir(folder_path):
        if filename.endswith((".png", ".jpg", ".jpeg")):
            file_path = os.path.join(folder_path, filename)

            try:
                img = Image.open(file_path)
                extracted_text = pytesseract.image_to_string(img)

                if extracted_text.strip():
                    collection.add(
                        documents=[extracted_text],
                        ids=[f"ocr_{filename}"],
                        metadatas=[{"source": "ocr", "type": "business_card"}]
                    )
            except Exception as e:
                print(f"Failed to process {filename}: {e}")

    print(f"Successfully indexed OCR images from {folder_path}")


from rag.text_pipeline import get_collection

def retrieve_ocr(query_text, n_results=2):
    try:
        collection = get_collection()
        results = collection.query(
            query_texts=[query_text],
            n_results=n_results,
            where={"source": "ocr"}
        )

        if results['documents'] and len(results['documents'][0]) > 0:
            return "\n".join(results['documents'][0])

        return "No relevant OCR data found."
    except Exception as e:
        return f"Error during OCR retrieval: {str(e)}"