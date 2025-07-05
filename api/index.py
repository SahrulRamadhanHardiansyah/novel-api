from flask import Flask, jsonify,  request, render_template
from scraper import (
    scrape_rilisan_terbaru, 
    scrape_pilihan_editor, 
    scrape_rekomendasi,
    scrape_novel_details,
    scrape_chapter_content,
    scrape_search_results
)

app = Flask(__name__)

@app.route('/')
def home():
    """Menampilkan halaman dokumentasi API dalam format HTML."""
    api_data = {
        'author': 'Sahrul Ramadhan',
        'message': 'Selamat datang di API Novel tidak resmi bacalightnovel.co',
        'endpoints': {
            '/api/terbaru': 'Menampilkan daftar novel rilisan terbaru.',
            '/api/pilihan-editor': 'Menampilkan daftar novel pilihan editor.',
            '/api/rekomendasi': 'Menampilkan daftar novel rekomendasi.',
            '/api/novel/<novel_slug>': 'Menampilkan detail sebuah novel.',
            '/api/chapter/<chapter_slug>': 'Menampilkan isi dari sebuah chapter.',
            '/api/search?q=<keyword>': 'Mencari novel berdasarkan query.'
        },
        'example_usage': {
            'get_novel_details': '/api/novel/martial-god-asura',
            'get_novel_by_search': '/api/search?q=martial-god-asura',
            'get_chapter_content': '/api/chapter/martial-god-asura-chapter-1'
        }
    }
    return render_template('index.html', data=api_data)

@app.route('/api/terbaru', methods=['GET'])
def get_rilisan_terbaru():
    data = scrape_rilisan_terbaru()
    if not data: return jsonify({'error': 'Gagal mengambil data.'}), 500
    return jsonify(data)

@app.route('/api/pilihan-editor', methods=['GET'])
def get_pilihan_editor():
    data = scrape_pilihan_editor()
    if not data: return jsonify({'error': 'Gagal mengambil data.'}), 500
    return jsonify(data)

@app.route('/api/rekomendasi', methods=['GET'])
def get_rekomendasi():
    data = scrape_rekomendasi()
    if not data: return jsonify({'error': 'Gagal mengambil data.'}), 500
    return jsonify(data)


@app.route('/api/novel/<string:novel_slug>', methods=['GET'])
def get_novel_details(novel_slug):
    """Endpoint untuk mendapatkan detail novel."""
    data = scrape_novel_details(novel_slug)
    if not data:
        return jsonify({'error': f'Novel dengan slug "{novel_slug}" tidak ditemukan atau gagal di-scrape.'}), 404
    return jsonify(data)

@app.route('/api/chapter/<path:chapter_slug>', methods=['GET'])
def get_chapter_content(chapter_slug):
    """Endpoint untuk mendapatkan isi chapter. Menggunakan <path> untuk menangani slug yang mungkin berisi '/'."""
    data = scrape_chapter_content(chapter_slug)
    if not data or 'error' in data:
        return jsonify({'error': f'Chapter dengan slug "{chapter_slug}" tidak ditemukan atau gagal di-scrape.'}), 404
    return jsonify(data)

@app.route('/api/search', methods=['GET'])
def search():
    """Endpoint untuk mencari novel."""
    # 3. Ambil query dari parameter URL (?q=...)
    query = request.args.get('q')

    if not query:
        return jsonify({'error': 'Parameter "q" untuk query pencarian dibutuhkan.'}), 400

    data = scrape_search_results(query)
    
    # Jika tidak ada hasil, kembalikan array kosong (ini bukan error)
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True, port=5001)