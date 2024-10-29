import fitz  # PyMuPDF
from pypdf import PdfWriter, PdfReader
import os


def process_pdf(input_path):
    """
    Обрабатывает PDF, оставляя только уникальные страницы,
    и возвращает обработанные страницы как список объектов Page из pypdf.
    """
    input_pdf = fitz.open(input_path)
    page_names = {}  # Словарь для хранения последней страницы для каждого уникального имени

    # Проходим по страницам, чтобы найти уникальные имена
    for page_num in range(input_pdf.page_count):
        page = input_pdf[page_num]

        # Получаем текст страницы
        text = page.get_text("text")

        # Извлекаем "имя" страницы. Предположим, что первая строка является именем.
        page_name = text.splitlines()[0] if text else f"Page {page_num + 1}"

        # Сохраняем последнюю страницу с данным именем
        page_names[page_name] = page_num

    # Возвращаем обработанные страницы
    input_pdf_reader = PdfReader(input_path)
    processed_pages = [input_pdf_reader.pages[page_num] for page_num in page_names.values()]

    return processed_pages


def merge_processed_pdfs(folder_path, output_path):
    """
    Обрабатывает все PDF файлы в папке, оставляет только уникальные страницы для каждого PDF,
    а затем склеивает их в один файл в лексикографическом порядке.
    """
    output_pdf = PdfWriter()

    # Получаем список всех PDF файлов в папке и сортируем их в лексикографическом порядке
    pdf_files = sorted([f for f in os.listdir(folder_path) if f.lower().endswith(".pdf")], key=lambda name: int(name.split('-')[1].split('.')[0]))

    for filename in pdf_files:
        input_path = os.path.join(folder_path, filename)
        print(f"Обрабатываем файл: {filename}")

        # Получаем обработанные страницы для текущего PDF
        processed_pages = process_pdf(input_path)

        # Добавляем каждую уникальную страницу в итоговый PDF
        for page in processed_pages:
            output_pdf.add_page(page)

    # Сохраняем объединённый PDF
    with open(output_path, "wb") as output_file:
        output_pdf.write(output_file)

    print(f"Итоговый PDF сохранен как: {output_path}")


# Пример использования
folder_path = "1"  # Замените на путь к вашей папке с PDF файлами
output_pdf_path = "merged_output.pdf"  # Итоговый файл
merge_processed_pdfs(folder_path, output_pdf_path)
