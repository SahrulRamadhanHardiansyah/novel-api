import requests
from bs4 import BeautifulSoup

BASE_URL = "https://bacalightnovel.co/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
}

def get_soup(url):
    """Mengambil dan mem-parsing halaman web, mengembalikan objek BeautifulSoup."""
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()  # Cek jika ada error HTTP
        return BeautifulSoup(response.content, 'html.parser')
    except requests.exceptions.RequestException as e:
        print(f"Error saat mengakses {url}: {e}")
        return None

def scrape_rilisan_terbaru():
    """Mengambil daftar novel dari bagian 'Rilisan Terbaru'."""
    soup = get_soup(BASE_URL)
    if not soup:
        return []

    novels = []
    latest_release_section = soup.find('div', class_='bixbox')
    
    if not latest_release_section:
        return []
        
    list_items = latest_release_section.find_all('div', class_='utao')

    for item in list_items:
        title_element = item.find('h3')
        series_link = item.find('a', class_='series')
        image_element = item.find('img')
        
        if title_element and series_link and image_element:
            chapters = []
            chapter_list = item.find_all('li')
            for li in chapter_list:
                chapter_link = li.find('a')
                if chapter_link:
                    chapters.append({
                        'title': chapter_link.text.strip(),
                        'url': chapter_link['href']
                    })

            novel_data = {
                'title': title_element.text.strip(),
                'url': series_link['href'],
                'image_url': image_element['src'],
                'latest_chapters': chapters
            }
            novels.append(novel_data)
            
    return novels

def scrape_pilihan_editor():
    """Mengambil daftar novel dari bagian 'Pilihan Editor'."""
    soup = get_soup(BASE_URL)
    if not soup:
        return []

    novels = []
    editor_choice_section = soup.find('div', class_='sliderarea')
    if not editor_choice_section:
        return []

    slide_items = editor_choice_section.find_all('div', class_='slide-item')

    for item in slide_items:
        title_link = item.select_one('.title .ellipsis a')
        image_element = item.select_one('.poster img')
        synopsis_element = item.select_one('.excerpt p')
        genres = [a.text for a in item.select('.slid-gen a')]

        if title_link and image_element:
            novel_data = {
                'title': title_link.text.strip(),
                'url': title_link['href'],
                'image_url': image_element['src'],
                'synopsis': synopsis_element.text.strip() if synopsis_element else "Tidak ada sinopsis.",
                'genres': genres
            }
            if novel_data not in novels:
                novels.append(novel_data)

    return novels

def scrape_rekomendasi():
    """Mengambil daftar novel dari bagian 'Rekomendasi'."""
    soup = get_soup(BASE_URL)
    if not soup:
        return []

    novels = []
    recommendation_section = soup.select_one('div.series-gen div.tab-pane.active')
    
    if not recommendation_section:
        return []

    list_items = recommendation_section.find_all('article', class_='bs')

    for item in list_items:
        title_element = item.find('h2')
        link_element = item.find('a')
        image_element = item.find('img')
        chapter_element = item.find('span', class_='nchapter')
        rating_element = item.find('div', class_='numscore')

        if title_element and link_element and image_element:
            novel_data = {
                'title': title_element.text.strip(),
                'url': link_element['href'],
                'image_url': image_element['src'],
                'latest_chapter': chapter_element.text.strip() if chapter_element else None,
                'rating': float(rating_element.text.strip()) if rating_element else None
            }
            novels.append(novel_data)
            
    return novels

def scrape_novel_details(novel_slug):
    """Mengambil detail lengkap sebuah novel berdasarkan slug-nya (VERSI BARU)."""
    url = f"https://bacalightnovel.co/series/{novel_slug}/"
    soup = get_soup(url)
    if not soup:
        return None

    details = {}
    
    # --- Area Informasi Utama ---
    main_info = soup.find('div', class_='sertoinfo')
    if not main_info:
        # Jika struktur utama tidak ditemukan, kembalikan null
        return None

    details['title'] = main_info.find('h1', class_='entry-title').text.strip()
    # Mengambil gambar dari luar 'sertoinfo'
    details['image_url'] = soup.find('div', class_='sertothumb').find('img')['src']
    
    # --- Sinopsis ---
    synopsis_element = main_info.find('div', class_='sersys')
    if synopsis_element:
        details['synopsis'] = synopsis_element.find('p').text.strip()
    else:
        details['synopsis'] = "Tidak ada sinopsis."
        
    # --- Genre ---
    genre_elements = main_info.find('div', class_='sertogenre')
    if genre_elements:
        details['genres'] = [a.text for a in genre_elements.find_all('a')]
    else:
        details['genres'] = []

    # --- Rating ---
    rating_element = main_info.find('div', class_='numscore')
    details['rating'] = float(rating_element.text.strip()) if rating_element else None

    # --- Metadata (Author, Status, dll) ---
    details['metadata'] = {}
    metadata_container = main_info.find('div', class_='sertoauth')
    if metadata_container:
        for item in metadata_container.find_all('div', class_='serl'):
            key = item.find('span', class_='sername').text.strip().lower().replace(':', '')
            value = item.find('span', class_='serval').text.strip()
            details['metadata'][key] = value
    
    # Menambahkan status dari elemen terpisah
    status_element = main_info.find('span', class_='Ongoing') or main_info.find('span', class_='Completed')
    if status_element:
        details['metadata']['status'] = status_element.text.strip()


    # --- Daftar Chapter (Selector Baru) ---
    details['chapters'] = []
    chapter_list_container = soup.find('div', class_='eplister')
    if chapter_list_container:
        for item in chapter_list_container.find_all('li'):
            link_element = item.find('a')
            if link_element:
                chapter_url = link_element['href']
                chapter_slug = chapter_url.strip('/').split('/')[-1]
                
                details['chapters'].append({
                    'chapter_short_title': link_element.find('div', class_='epl-num').text.strip(),
                    'chapter_full_title': link_element.find('div', class_='epl-title').text.strip(),
                    'release_date': link_element.find('div', class_='epl-date').text.strip(),
                    'slug': chapter_slug,
                    'url': chapter_url
                })
        # Membalik urutan chapter agar dari awal ke akhir
        details['chapters'].reverse()
            
    return details


def scrape_chapter_content(chapter_slug):
    """Mengambil isi konten dari sebuah chapter (VERSI BARU)."""
    url = f"https://bacalightnovel.co/{chapter_slug}/"
    soup = get_soup(url)
    if not soup:
        return None

    # Ambil judul chapter
    chapter_title = soup.find('h1', class_='entry-title').text.strip() if soup.find('h1', class_='entry-title') else 'N/A'

    # Konten utama sekarang berada di dalam div 'epcontent'
    content_area = soup.find('div', class_='epcontent')
    if not content_area:
        return {'error': 'Area konten tidak ditemukan.'}
        
    # Menghapus elemen yang tidak diinginkan seperti iklan
    for ad_div in content_area.find_all('div', class_='code-block'):
        ad_div.decompose()
        
    # Mengambil semua paragraf dan menggabungkannya
    content_paragraphs = content_area.find_all('p')
    # Membersihkan teks dari tag span jika ada dan menggabungkan jadi satu blok teks
    content_text = '\n\n'.join(p.text.strip() for p in content_paragraphs if p.text.strip())
    
    return {
        'chapter_title': chapter_title,
        'content': content_text
    }
    """Mengambil isi konten dari sebuah chapter berdasarkan slug-nya."""
    url = f"https://bacalightnovel.co/{chapter_slug}/"
    soup = get_soup(url)
    if not soup:
        return None

    content_area = soup.select_one('div#readerarea')
    if not content_area:
        return {'error': 'Area konten tidak ditemukan.'}
        
    content_paragraphs = content_area.find_all('p')
    content_text = '\n\n'.join([p.text for p in content_paragraphs])
    
    chapter_title = soup.select_one('h1.entry-title').text.strip() if soup.select_one('h1.entry-title') else 'N/A'

    return {
        'chapter_title': chapter_title,
        'content': content_text
    }
    
def scrape_search_results(query):
    """Mengambil hasil pencarian novel berdasarkan query (VERSI BARU)."""
    url = f"https://bacalightnovel.co/?s={query}"
    soup = get_soup(url)
    if not soup:
        return []

    novels = []
    # Kontainer utamanya adalah 'div.listupd'
    search_results_container = soup.find('div', class_='listupd')
    if not search_results_container:
        return []

    # Setiap item sekarang adalah 'article.maindet'
    list_items = search_results_container.find_all('article', class_='maindet')

    for item in list_items:
        # Mencari elemen berdasarkan struktur baru
        title_link_element = item.select_one('h2 a')
        image_element = item.select_one('.mdthumb img')
        rating_element = item.select_one('.mdminf')
        synopsis_element = item.select_one('.contexcerpt p')
        genres = [a.text.strip('# ') for a in item.select('.mdgenre a')]

        if title_link_element and image_element:
            novel_url = title_link_element['href']
            # Ekstrak slug dari URL
            novel_slug = novel_url.strip('/').split('/')[-2]
            
            # Membersihkan rating dari ikon bintang
            rating_text = rating_element.text.strip() if rating_element else None
            
            novel_data = {
                'title': title_link_element.text.strip(),
                'slug': novel_slug,
                'url': novel_url,
                'image_url': image_element['src'],
                'synopsis': synopsis_element.text.strip() if synopsis_element else "Tidak ada sinopsis.",
                'rating': float(rating_text) if rating_text else None,
                'genres': genres
            }
            novels.append(novel_data)
            
    return novels

if __name__ == '__main__':
    print("--- Rilisan Terbaru ---")
    latest_novels = scrape_rilisan_terbaru()
    if latest_novels:
        print(f"Ditemukan {len(latest_novels)} novel.")
        for novel in latest_novels[:2]:
            print(novel)
    
    print("\n--- Pilihan Editor ---")
    editor_picks = scrape_pilihan_editor()
    if editor_picks:
        print(f"Ditemukan {len(editor_picks)} novel.")
        for novel in editor_picks[:2]:
            print(novel)
            
    print("\n--- Rekomendasi ---")
    recommendations = scrape_rekomendasi()
    if recommendations:
        print(f"Ditemukan {len(recommendations)} novel rekomendasi.")
        for novel in recommendations[:2]:
            print(novel)