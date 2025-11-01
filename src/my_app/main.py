import requests


# --- Definicje wyjątków ---

class DownloadError(Exception):
  """Bazowy wyjątek dla błędów pobierania pliku."""
  pass


class NotFoundError(DownloadError):
  """Wyjątek rzucany, gdy serwer zwróci kod 404 (plik nie znaleziony)."""
  pass


class AccessDeniedError(DownloadError):
  """Wyjątek rzucany, gdy serwer zwróci kod 403 (brak dostępu / serwis niedostępny)."""
  pass


# --- Funkcja pobierająca plik ---

def download_file(url: str, filename: str = "latest.csv"):
  """Pobiera plik z danego URL i zapisuje go lokalnie.

    Argumenty:
        url (str): Adres URL do pobrania pliku.
        filename (str, opcjonalnie): Nazwa pliku do zapisania. Domyślnie 'latest.txt'.
    """
  try:
    response = requests.get(url)

    # Obsługa konkretnych kodów odpowiedzi HTTP
    if response.status_code == 404:
      raise NotFoundError(f"Plik nie został znaleziony: {url}")
    elif response.status_code == 403:
      raise AccessDeniedError(
        f"Dostęp zabroniony lub serwer niedostępny: {url}")
    elif response.status_code != 200:
      raise DownloadError(f"Błąd pobierania: kod {response.status_code}")

    # Zapisanie pliku
    with open(filename, "wb") as f:
      f.write(response.content)

    print(f"Pobrano plik i zapisano jako: {filename}")

  except requests.exceptions.RequestException as e:
    raise DownloadError(f"Błąd połączenia: {e}")


# --- Część wykonywana tylko przy uruchomieniu bezpośrednim ---

if __name__ == "__main__":
  url = input("Podaj adres URL do pobrania: ").strip()
  filename = input(
    "Podaj nazwę pliku do zapisania (Enter = latest.csv): ").strip()

  try:
    if filename:
      download_file(url, filename)
    else:
      download_file(url)
  except NotFoundError as e:
    print(f"Błąd 404: {e}")
  except AccessDeniedError as e:
    print(f"Błąd 403: {e}")
  except DownloadError as e:
    print(f"Inny błąd pobierania: {e}")