import os
import asyncio
import sys
from typing import List, Dict, Any

# Add the project root to the Python path to allow for absolute imports
# This is a common pattern for scripts within a larger project structure.
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.core.embeddings import chunk_text, generate_embeddings, prepare_qdrant_points
from src.db.qdrant_client import qdrant_manager
from src.config import settings

BOOK_CONTENT_DIR = os.path.abspath(os.path.join(project_root, '..', 'book-content', 'modules'))

async def ingest_book_data():
    """
    Scans the book-content directory, processes all .mdx files, generates embeddings,
    and upserts them into the Qdrant vector database.
    """
    print("Starting book content ingestion process...")
    
    # 1. Ensure the Qdrant collection exists
    print(f"Ensuring Qdrant collection '{settings.QDRANT_COLLECTION_NAME}' exists...")
    qdrant_manager.create_collection_if_not_exists()
    
    all_chunks = []
    all_metadatas = []
    
    # 2. Walk through the book content directory
    print(f"Scanning directory: {BOOK_CONTENT_DIR}")
    for root, _, files in os.walk(BOOK_CONTENT_DIR):
        for file in files:
            if file.endswith(".mdx"):
                file_path = os.path.join(root, file)
                print(f"Processing file: {file_path}")
                
                module_name = os.path.basename(root)
                chapter_name = os.path.splitext(file)[0]
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 3. Chunk the text
                chunks = chunk_text(content, chunk_size=512, chunk_overlap=50)
                
                # 4. Create metadata for each chunk
                for i, chunk in enumerate(chunks):
                    metadata = {
                        "module": module_name,
                        "chapter": chapter_name,
                        "file_path": file_path,
                        "chunk_index": i,
                    }
                    all_chunks.append(chunk)
                    all_metadatas.append(metadata)
    
    if not all_chunks:
        print("No content to ingest. Exiting.")
        return

    print(f"Generated a total of {len(all_chunks)} chunks from the book content.")
    
    # 5. Generate embeddings for all chunks in batches
    print("Generating embeddings for all chunks (this may take a while)...")
    # Note: Depending on the API and number of chunks, you might need to batch this.
    # The `generate_gemini_embeddings` function is assumed to handle batching if necessary.
    embeddings = await generate_embeddings(all_chunks, "gemini") # Hardcoding to 'gemini' to bypass environment variable issues
    
    # 6. Prepare Qdrant points
    print("Preparing data points for Qdrant...")
    qdrant_points = prepare_qdrant_points(all_chunks, embeddings, all_metadatas)
    
    # 7. Upsert points into Qdrant
    print(f"Upserting {len(qdrant_points)} points into Qdrant collection...")
    operation_info = qdrant_manager.upsert_vectors(qdrant_points)
    
    if operation_info.status == 'completed':
        print("Successfully upserted all points to Qdrant.")
    else:
        print(f"Qdrant upsert failed with status: {operation_info.status}")
        print(f"Error details: {operation_info.error}")

if __name__ == "__main__":
    # Ensure you have a .env file in the `backend` directory with your
    # QDRANT_HOST, QDRANT_API_KEY, and GEMINI_API_KEY
    print("Running the ingestion script...")
    asyncio.run(ingest_book_data())
    print("Ingestion script finished.")
