import pandas as pd
from pathlib import Path

# Пути к файлам
original_md_path = Path(r"1_PDF_Manual/instruction.md")  # оригинал
translation_table_path = Path("instruction_translation.xlsx")  # перевод
lang_to_translate = 'English'  # язык на который перводить
output_md_path = Path(f"translation/instruction_translated_on_{lang_to_translate}.md")  # результат
# Загружаем таблицу переводов
df = pd.read_excel(translation_table_path)

# Создаем словарь: оригинал -> перевод
translation_dict = dict(zip(df["Original (Russian)"].fillna("").str.strip(), df[f"Translation ({lang_to_translate})"].astype(str).fillna("").str.strip()))

# Загружаем оригинальный .md файл
with open(original_md_path, "r", encoding="utf-8") as f:
    original_lines = f.read().splitlines()

# Новый список строк
translated_lines = []

# Временная переменная для накопления многострочного блока
current_block = []


def flush_current_block():
    """Проверить накопленный блок и заменить его переводом"""
    if not current_block:
        return

    original_text = "\n".join(current_block).strip()
    translated_text = translation_dict.get(original_text)

    if translated_text:
        translated_lines.extend(translated_text.splitlines())
    else:
        translated_lines.extend(current_block)

    current_block.clear()


# Проходим построчно
for line in original_lines:
    stripped = line.strip()

    if stripped.startswith("![](") or stripped.startswith("<img "):
        # Сначала сбрасываем накопленный текст
        flush_current_block()
        # Изображения вставляем без изменений
        translated_lines.append(line)
    elif stripped == "":
        # Пустая строка — конец блока
        flush_current_block()
        translated_lines.append("")
    else:
        # Накопление текста
        current_block.append(line)

# Не забудем обработать оставшийся накопленный блок
flush_current_block()

# Сохраняем переведённый .md файл
with open(output_md_path, "w", encoding="utf-8") as f:
    f.write("\n".join(translated_lines))

print(f"Переведённый файл сохранён как {output_md_path}")
