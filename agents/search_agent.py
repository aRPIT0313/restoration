import requests
import os
from PIL import Image
from io import BytesIO
import json
import re

def build_search_query(damage_report):
    """Build a SHORT simple search query"""
    murti_type = damage_report.get("murti_type", "Hindu statue")
    # strip brackets and extra info
    murti_type = murti_type.split("(")[0].strip()
    query = f"{murti_type} statue intact full body"
    return query

def search_duckduckgo_images(query, num_results=6):
    """Search DuckDuckGo for images - no API key needed"""
    try:
        session = requests.Session()
        session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
        })

        # step 1 - get vqd token
        resp = session.get(
            "https://duckduckgo.com/",
            params={"q": query},
            timeout=10
        )
        print(f"DDG token page status: {resp.status_code}")

        # try multiple vqd patterns
        vqd = None
        patterns = [
            r'vqd="([^"]+)"',
            r"vqd='([^']+)'",
            r'vqd=([0-9-]+)',
            r'"vqd":"([^"]+)"',
        ]
        for pattern in patterns:
            match = re.search(pattern, resp.text)
            if match:
                vqd = match.group(1)
                print(f"Found vqd: {vqd[:20]}...")
                break

        if not vqd:
            print("Could not extract vqd token from DuckDuckGo")
            return []

        # step 2 - search images
        img_resp = session.get(
            "https://duckduckgo.com/i.js",
            params={
                "q": query,
                "vqd": vqd,
                "f": ",,,,,",
                "p": "1",
                "v7exp": "a"
            },
            headers={
                "Referer": "https://duckduckgo.com/",
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "X-Requested-With": "XMLHttpRequest"
            },
            timeout=10
        )

        print(f"DDG image search status: {img_resp.status_code}")

        if img_resp.status_code != 200:
            print(f"DDG image search failed: {img_resp.text[:200]}")
            return []

        data = img_resp.json()
        results = []

        for item in data.get("results", [])[:num_results]:
            img_url = item.get("image", "")
            if img_url:
                results.append({
                    "title": item.get("title", ""),
                    "url": img_url,
                    "thumbnail": item.get("thumbnail", img_url),
                    "source": item.get("url", "DuckDuckGo")
                })

        print(f"DuckDuckGo found {len(results)} results")
        return results

    except Exception as e:
        print(f"DuckDuckGo error: {e}")
        return []

def search_wikimedia(query, num_results=8):
    """Search Wikimedia Commons for murti images"""
    try:
        url = "https://commons.wikimedia.org/w/api.php"
        params = {
            "action": "query",
            "generator": "search",
            "gsrnamespace": "6",
            "gsrsearch": query,
            "gsrlimit": str(num_results),
            "prop": "imageinfo",
            "iiprop": "url|mime|thumburl",
            "iiurlwidth": "500",
            "format": "json",
            "origin": "*"
        }
        headers = {
            "User-Agent": "MurtiRestorationBot/1.0 (college project)"
        }

        resp = requests.get(url, params=params, timeout=15, headers=headers)
        print(f"Wikimedia status: {resp.status_code}")

        if resp.status_code != 200:
            return []

        data = resp.json()
        results = []
        pages = data.get("query", {}).get("pages", {})

        for page in pages.values():
            info = page.get("imageinfo", [{}])[0]
            img_url = info.get("url", "")
            thumb_url = info.get("thumburl", "")
            mime = info.get("mime", "")
            best_url = thumb_url if thumb_url else img_url

            if best_url and mime.startswith("image"):
                results.append({
                    "title": page.get("title", "").replace("File:", ""),
                    "url": best_url,
                    "thumbnail": thumb_url or img_url,
                    "source": "Wikimedia Commons"
                })

        print(f"Wikimedia found {len(results)} results")
        return results

    except Exception as e:
        print(f"Wikimedia error: {e}")
        return []

def download_image(url, save_path):
    """Download image from URL"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
            "Accept": "image/jpeg,image/png,image/gif,image/*,*/*",
            "Referer": "https://duckduckgo.com/"
        }

        response = requests.get(url, timeout=15, headers=headers, stream=True)
        print(f"    Download status: {response.status_code} for {url[:70]}")

        if response.status_code != 200:
            return False

        content_type = response.headers.get("content-type", "")
        if "image" not in content_type and "octet-stream" not in content_type:
            print(f"    Not an image: {content_type}")
            return False

        img = Image.open(BytesIO(response.content)).convert("RGB")

        if img.width < 100 or img.height < 100:
            print(f"    Image too small: {img.width}x{img.height}")
            return False

        img.save(save_path, "JPEG", quality=85)
        print(f"    Saved {img.width}x{img.height}")
        return True

    except Exception as e:
        print(f"    Download failed: {e}")
        return False

def find_similar(image_path, damage_report, top_k=3):
    """Main function - searches for similar intact murti images"""
    query = build_search_query(damage_report)
    print(f"\nSearching for: '{query}'")

    # try DuckDuckGo first
    results = search_duckduckgo_images(query, num_results=top_k + 3)

    # fallback to Wikimedia
    if not results:
        print("DuckDuckGo failed, trying Wikimedia...")
        results = search_wikimedia(query, num_results=top_k + 5)

    # last resort - generic search
    if not results:
        print("Trying generic fallback search...")
        murti_type = damage_report.get("murti_type", "Shiva").split("(")[0].strip()
        results = search_wikimedia(f"{murti_type} sculpture India bronze", num_results=top_k + 5)

    temp_dir = "outputs/temp_references"
    os.makedirs(temp_dir, exist_ok=True)

    downloaded_paths = []
    downloaded_meta = []

    for i, result in enumerate(results):
        if len(downloaded_paths) >= top_k:
            break

        if not result.get("url"):
            continue

        save_path = os.path.join(temp_dir, f"ref_{i+1}.jpg")
        success = download_image(result["url"], save_path)

        if success:
            downloaded_paths.append(save_path)
            downloaded_meta.append(result)
            print(f"  ✓ Downloaded: {result['title'][:60]}")
        else:
            print(f"  ✗ Skipped: {result['title'][:60]}")

    # save metadata
    meta_path = os.path.join(temp_dir, "references_meta.json")
    with open(meta_path, "w") as f:
        json.dump(downloaded_meta, f, indent=2)

    print(f"\nTotal downloaded: {len(downloaded_paths)} reference images")
    return downloaded_paths, downloaded_meta