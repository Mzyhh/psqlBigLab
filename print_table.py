import textwrap

def print_table(headers, rows, max_width=30):
    """
    headers: список заголовков
    rows: список списков (строк) данных
    max_width: максимальная ширина одной ячейки перед переносом
    """
    
    wrapped_rows = []
    for row in rows:
        wrapped_row = []
        for cell in row:
            cell_str = str(cell) if cell is not None else ""
            # break_long_words=False не будет рвать слова посередине, если возможно
            wrapped_lines = textwrap.wrap(cell_str, width=max_width, break_long_words=True)
            if not wrapped_lines:
                wrapped_lines = [""]
            wrapped_row.append(wrapped_lines)
        wrapped_rows.append(wrapped_row)

    col_widths = [len(h) for h in headers]
    
    for wrapped_row in wrapped_rows:
        for i, lines in enumerate(wrapped_row):
            for line in lines:
                if len(line) > col_widths[i]:
                    col_widths[i] = len(line)
    def print_separator():
        parts = ["+" + "-" * (w + 2) for w in col_widths]
        print("".join(parts) + "+")

    def print_data_row(row_lines_list):
        max_height = max(len(lines) for lines in row_lines_list)
        
        for h in range(max_height):
            line_parts = []
            for i, lines in enumerate(row_lines_list):
                text = lines[h] if h < len(lines) else ""
                cell_content = f" {text:<{col_widths[i]}} "
                line_parts.append("|" + cell_content)
            print("".join(line_parts) + "|")

    print_separator()
    header_wrapped = [textwrap.wrap(h, width=max_width) for h in headers]
    print_data_row(header_wrapped)
    print_separator()
    
    for wrapped_row in wrapped_rows:
        print_data_row(wrapped_row)
        print_separator()

if __name__ == "__main__":
    headers = ["№", "Название", "Описание", "Начало", "Окончание"]
    data = [
        [1, "Античные Амфоры", "Коллекция греческих и римских сосудов VI-IV вв. до н.э.", "2026-01-01", "2026-08-24"],
        [2, "Сокровища Фараонов", "Реплики и оригиналы украшений эпохи Нового царства.", "2021-06-15", "2023-06-15"],
        [3, "Картины Да Винчи", "Сборник репродукций и эскизов мастера.", "2024-03-01", "2029-03-01"],
        [4, "Скифское Золото", "Украшения и оружие кочевников причерноморских степей.", "2022-01-01", "2032-01-01"],
        [5, "Авангард XX века", "Работы Малевича, Кандинского и их последователей.", "2023-09-01", "2033-09-01"]
    ]

    print_table(headers, data, max_width=25)
