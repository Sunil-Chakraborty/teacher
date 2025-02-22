from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
import os

import fitz  # PyMuPDF for extracting links from PDF
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import JsonResponse

import requests
import mimetypes
import magic  # pip install python-magic-bin  
              # Python-magic for detecting file types
from urllib.parse import urlparse, parse_qs
import urllib3


# Create your views here.

def extract_links_from_pdf(pdf_path):
    """Extracts all unique links from a PDF file."""
    doc = fitz.open(pdf_path)
    all_links = set()  # Use a set to store unique links
    
    for page in doc:
        for link in page.get_links():
            uri = link.get("uri", "")
            if uri:
                all_links.add(uri)  # Sets automatically remove duplicates
    
    return list(all_links)  # Convert back to a list before returning
    
    
def upload_pdf_extract_links(request):
    """Handles PDF file upload, extracts links, and saves the results dynamically."""
    
    
    if request.method == "POST" and request.FILES.get("pdf_file"):
        pdf_file = request.FILES["pdf_file"]
        save_dir = os.path.join(settings.MEDIA_ROOT, "extracted_links")
        os.makedirs(save_dir, exist_ok=True)
        
        file_path = os.path.join(save_dir, pdf_file.name)

        # Check if the file already exists
        if os.path.exists(file_path):
            return JsonResponse({"message": "A file with the same name already exists. Please rename and try again."}, status=400)

        # Save uploaded file temporarily
        file_name = default_storage.save(file_path, ContentFile(pdf_file.read()))

        # Extract links
        extracted_links = extract_links_from_pdf(default_storage.path(file_name))

        # Save extracted links to a text file
        links_file_path = os.path.join(save_dir, f"{pdf_file.name}_links.txt")
        with open(links_file_path, "w") as f:
            for link in extracted_links:
                f.write(link + "\n")

        return JsonResponse({
            "message": "Links extracted successfully",
            "links": extracted_links,
            "saved_file": links_file_path,
        })

    return render(request, "util/upload_pdf.html")
    
   
# Downloading file following extract_link.txt
 
# Disable SSL warnings (Optional, but recommended for production)

# Disable SSL warnings (Optional but useful for debugging)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Headers to mimic a real browser request
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Referer": "https://www.google.com",
    "Accept": "text/html,application/pdf,application/vnd.ms-excel,application/msword,*/*",
    "Connection": "keep-alive"
}

def log_missing_links(save_dir, message, url):
    """Logs skipped or failed links to a file."""
    log_file = os.path.join(save_dir, "missing_log.txt")
    with open(log_file, "a") as log:
        log.write(f"{message}: {url}\n")

def convert_google_links(url):
    """Convert Google Docs and Google Drive links to direct download links."""
    
    # Convert Google Docs link to direct DOCX download
    if "docs.google.com/document/d/" in url:
        file_id = url.split("/d/")[1].split("/")[0]
        return f"https://docs.google.com/document/d/{file_id}/export?format=docx"
    
    # Convert Google Drive link to direct download
    if "drive.google.com" in url and "/file/d/" in url:
        file_id = url.split("/file/d/")[1].split("/")[0]
        return f"https://drive.google.com/uc?export=download&id={file_id}"

    return url
    
def is_doi_link(url):
    """Checks if the URL is a DOI link and should be skipped."""
    return "doi.org" in url
    
def get_file_extension(response, url, file_bytes):
    """Determines the correct file extension from headers, magic bytes, or URL."""
    content_type = response.headers.get("Content-Type", "")
    content_disposition = response.headers.get("Content-Disposition", "")

    if "filename=" in content_disposition:
        filename = content_disposition.split("filename=")[-1].strip('"')
        ext = os.path.splitext(filename)[1]
        if ext:
            return ext

    if content_type:
        if "text/html" in content_type:
            return None  # Skip downloading HTML pages
        ext = mimetypes.guess_extension(content_type)
        if ext:
            return ext

    mime = magic.Magic(mime=True)
    detected_mime = mime.from_buffer(file_bytes[:2048])
    ext = mimetypes.guess_extension(detected_mime)
    if ext:
        return ext

    url_path = urlparse(url).path
    url_ext = os.path.splitext(url_path)[1]
    if url_ext:
        return url_ext

    return ".txt"  # Save unknown types as .txt with the URL inside

def download_file(url, save_dir, file_index):
    """Downloads a file and assigns the correct file extension."""
    if is_doi_link(url):
        print(f"⚠️ Skipping DOI link: {url}")
        log_missing_links(save_dir, "Skipped DOI Link", url)
        return None

    url = convert_google_links(url)

    session = requests.Session()
    session.headers.update(HEADERS)

    try:
        response = session.get(url, stream=True, allow_redirects=True, verify=False)
        response.raise_for_status()

        file_bytes = response.content[:2048]
        file_extension = get_file_extension(response, url, file_bytes)

        if file_extension is None:
            print(f"⚠️ Skipping {url} (appears to be a webpage, not a document)")
            log_missing_links(save_dir, "Skipped HTML Page", url)
            return None

        file_name = f"file_{file_index}{file_extension}"
        save_path = os.path.join(save_dir, file_name)

        if file_extension == ".txt":
            # Save the URL inside the .txt file
            with open(save_path, "w") as file:
                file.write(f"Failed to determine file type. Original URL: {url}\n")
        else:
            # Save the actual downloaded file
            with open(save_path, "wb") as file:
                file.write(response.content)

        print(f"✅ Downloaded: {save_path}")
        return file_name

    except requests.exceptions.HTTPError as e:
        if response.status_code == 403:
            print(f"❌ Forbidden: {url} - This site may require login")
            log_missing_links(save_dir, "403 Forbidden", url)
        else:
            print(f"❌ Error downloading {url}: {e}")
            log_missing_links(save_dir, "Download Error", url)
        return None
        
def upload_links_and_download(request):
    if request.method == "POST" and request.FILES.get("links_file"):
        links_file = request.FILES["links_file"]
        file_path = default_storage.save(f"uploads/{links_file.name}", ContentFile(links_file.read()))

        save_dir = os.path.join("downloads", os.path.splitext(links_file.name)[0])
        os.makedirs(save_dir, exist_ok=True)

        with default_storage.open(file_path, "r") as file:
            links = [line.strip() for line in file.readlines() if line.strip()]

        downloaded_files = []
        for index, link in enumerate(links, start=1):
            downloaded_file = download_file(link, save_dir, index)
            if downloaded_file:
                downloaded_files.append(downloaded_file)

        return JsonResponse({"status": "success", "downloaded_files": downloaded_files, "save_dir": save_dir})

    return render(request, "util/upload_links.html")
