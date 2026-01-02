import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL:
    raise ValueError("SUPABASE_URL is niet ingesteld.")
if not SUPABASE_KEY:
    raise ValueError("SUPABASE_KEY is niet ingesteld.")

# Zorg dat de URL eindigt met slash (vereiste voor storage)
if not SUPABASE_URL.endswith("/"):
    SUPABASE_URL += "/"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def upload_file(file, bucket="uploads"):
    import os
    file_path = os.path.basename(file.filename)

    supabase.storage.from_(bucket).upload(
        file_path,
        file.read(),
        {"content-type": file.content_type}
    )

    public_url = supabase.storage.from_(bucket).get_public_url(file_path)
    return public_url

def list_buckets():
    """
    Print alle buckets in Supabase Storage.
    Gebruik .name voor bucketnaam, want SyncBucket objecten zijn geen dicts.
    """
    buckets = supabase.storage.list_buckets()
    print("Buckets gevonden:")
    for bucket in buckets:
        print("-", bucket.name)
