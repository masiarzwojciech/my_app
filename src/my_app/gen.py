import csv
from functools import wraps
from datetime import datetime

# Dekorator logujący czas wykonania funkcji
def log_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = datetime.now()
        print(f"[{start}] Rozpoczęto: {func.__name__}")
        result = func(*args, **kwargs)
        end = datetime.now()
        print(f"[{end}] Zakończono: {func.__name__} (czas trwania: {end - start})")
        return result
    return wrapper

def extract(input_file):
    with open(input_file, newline='', encoding='utf-8') as f:
        for row in csv.reader(f):
            yield row

def transform(rows):
    for row in rows:
        idx = row[0]
        values = [float(x) if x != '-' else None for x in row[1:]]
        valid = [v for v in values if v is not None]
        total = sum(valid) if valid else 0
        mean = total / len(valid) if valid else 0
        missing = [i+1 for i, v in enumerate(values) if v is None]
        yield idx, total, mean, missing

def load(data):
    with open("values.csv", "w", newline='', encoding='utf-8') as v, \
         open("missing_values.csv", "w", newline='', encoding='utf-8') as m:
        val_writer = csv.writer(v)
        miss_writer = csv.writer(m)
        val_writer.writerow(["index", "sum", "mean"])
        miss_writer.writerow(["index", "missing_indexes"])
        for idx, total, mean, missing in data:
            val_writer.writerow([idx, total, mean])
            miss_writer.writerow([idx, missing])

# Funkcja główna opakowana dekoratorem
@log_time
def run(input_file):
    load(transform(extract(input_file)))

# Uruchomienie
if __name__ == "__main__":
    run("latest.csv")