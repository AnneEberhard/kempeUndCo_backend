import csv


# checks csv coding
def check_csv_structure(file_path):
    with open(file_path, 'r', encoding='UTF-8') as file:
        reader = csv.reader(file)
        headers = next(reader)
        num_columns = len(headers)
        print("Headers:", headers)
        for row_number, row in enumerate(reader, start=2):
            if len(row) != num_columns:
                print(f"Row {row_number} length mismatch: {row} (expected {num_columns} columns)")
                # Optional: Maßnahmen zur Bereinigung der Zeile ergreifen


file_path = 'kempe_source_file.csv'
check_csv_structure(file_path)
