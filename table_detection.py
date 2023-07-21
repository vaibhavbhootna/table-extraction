import re
from collections import defaultdict

def detect_tables(text):
    # Step 1: Identify table-like patterns
    table_patterns = re.findall(r'((?:.*(?:\s\s+|\t).*)+\n)', text)

    # Step 2: Tokenize the text into lines
    lines = text.strip().split('\n')

    # Step 3: Column and Row Detection
    tables = []
    for pattern in table_patterns:
        rows = pattern.strip().split('\n')

        # Heuristic: Determine column positions based on irregular spacing
        columns_positions = [0]
        for i in range(1, len(rows[0])):
            if rows[0][i] != " " and rows[0][i-1] == " ":
                columns_positions.append(i)

        num_columns = len(columns_positions)
        table = defaultdict(list)

        for row in rows:
            columns = [row[columns_positions[i]:columns_positions[i+1]].strip() for i in range(num_columns - 1)]
            if len(columns) == num_columns:
                for i, col in enumerate(columns):
                    table[f"Column_{i + 1}"].append(col.strip())

        # Step 4: Data Validation
        if len(table) == num_columns:
            tables.append(table)

    return tables

if __name__ == "__main__":
    # Sample text containing tables (rows separated by '\n', columns separated by whitespace)
    sample_text = """
    Name    Age   Occupation
    John   30    Engineer
    Alice       25    Doctor

    Product   Price   Quantity
    Laptop      1000    5
    Phone     500     10
    """

    # Step 1-4: Detect and Extract Tables
    detected_tables = detect_tables(sample_text)

    # Step 5: Display the detected tables
    for i, table in enumerate(detected_tables, 1):
        print(f"Table {i}:")
        for column, values in table.items():
            print(f"{column}: {values}")
        print("\n")