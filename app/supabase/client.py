import os
from supabase import create_client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def upload_file(file, bucket="uploads"):
    """
    uploadt een bestand naar Supabase Storage
    en geeft de public URL terug
    """
    #alleen de bestandsnaam, geen pad
    file_path = os.path.basename(file.filename)

    #upload het bestand
    supabase.storage.from_(bucket).upload(
        file_path,
        file.read(),
        {"content-type": file.content_type}
    )

    #public url ophalen
    public_url = supabase.storage.from_(bucket).get_public_url(file_path)

    return public_url
