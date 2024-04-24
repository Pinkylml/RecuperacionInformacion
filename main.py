import requests
from bs4 import BeautifulSoup

# Paso 2: Obtener el contenido HTML de la página principal
url = 'https://www.gutenberg.org/browse/scores/top#books-last1'
response = requests.get(url)
html = response.text

# Paso 3: Analizar el HTML y extraer los enlaces de los libros
soup = BeautifulSoup(html, 'html.parser')
h2_element = soup.find('h2', text='Top 100 EBooks yesterday')
book_list = h2_element.find_next('ol').find_all('a')

# Paso 4: Visitar las páginas de descarga y obtener los enlaces de descarga
for book_link in book_list:
    book_url = 'https://www.gutenberg.org' + book_link['href']
    book_response = requests.get(book_url)
    book_html = book_response.text
    book_soup = BeautifulSoup(book_html, 'html.parser')
    
    # Verificar si el enlace de descarga está disponible
    download_link = book_soup.find('a', title='Download', text='Plain Text UTF-8')
    if download_link:
        download_url = 'https://www.gutenberg.org' + download_link['href']
        book_content = requests.get(download_url).text
        
        # Guardar el contenido del libro en un archivo de texto
        book_title = book_link.text.split('by')[0].strip()  # Extraer el título del libro
        filename = f"{book_title}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(book_content)
        
        print(f'Descargado y guardado: {filename}')
    else:
        print(f'El libro "{book_link.text}" no está disponible en formato Plain Text UTF-8.')
