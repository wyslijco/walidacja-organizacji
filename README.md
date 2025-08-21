# Walidacja Organizacji - GitHub Action

GitHub Action do walidacji plików YAML organizacji charytatywnych w Polsce. Action sprawdza poprawność struktury danych, zgodność ze schematem oraz konflikty adresów organizacji.

## 📋 Spis treści

- [Funkcjonalności](#-funkcjonalności)
- [Parametry wejściowe](#-parametry-wejściowe)
- [Przykłady użycia](#-przykłady-użycia)
- [Struktura danych organizacji](#-struktura-danych-organizacji)
- [Zasady walidacji](#-zasady-walidacji)
- [Rozwój lokalny](#-rozwój-lokalny)
- [Testy](#-testy)
- [Licencja](#-licencja)

## 🚀 Funkcjonalności

- **Walidacja struktury YAML** - sprawdza poprawność składni i wymaganych pól
- **Weryfikacja KRS** - sprawdza numery KRS w oficjalnym rejestrze oraz zgodność nazw
- **Kontrola konfliktów adresów** - wykrywa duplikaty adresów stron organizacji
- **Walidacja adresów dostawy** - sprawdza poprawność formatów kodów pocztowych i telefonów
- **Sprawdzanie produktów** - waliduje strukturę listy produktów organizacji
- **Zabezpieczenia przed zarezerwowanymi adresami** - blokuje użycie zarezerwowanych slugów

## 📥 Parametry wejściowe

| Parametr | Opis | Wymagany | Domyślna wartość |
|----------|------|----------|------------------|
| `files` | Lista plików YAML organizacji do walidacji (oddzielone spacjami) | Tak | - |
| `organizations-dir` | Katalog zawierający pliki YAML organizacji | Nie | `organizations` |
| `slug-field` | Nazwa pola YAML używanego jako adres strony organizacji | Nie | `adres` |

## 📖 Przykłady użycia

### Podstawowe użycie

```yaml
name: Walidacja organizacji
on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Walidacja plików organizacji
        uses: twoj-uzytkownik/walidacja-organizacji@v1
        with:
          files: 'organizations/nowa-organizacja.yaml organizations/zmieniona-organizacja.yaml'
```

### Użycie z niestandardowym katalogiem

```yaml
- name: Walidacja organizacji w niestandardowym katalogu
  uses: twoj-uzytkownik/walidacja-organizacji@v1
  with:
    files: 'dane/org1.yaml dane/org2.yaml'
    organizations-dir: 'dane'
    slug-field: 'identyfikator'
```

### Integracja z wykrywaniem zmienionych plików

```yaml
name: Walidacja zmienionych organizacji
on: [pull_request]

jobs:
  validate-changed:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      
      - name: Wykryj zmienione pliki
        id: changed-files
        uses: tj-actions/changed-files@v44
        with:
          files: organizations/*.yaml
          
      - name: Walidacja zmienionych organizacji
        if: steps.changed-files.outputs.any_changed == 'true'
        uses: twoj-uzytkownik/walidacja-organizacji@v1
        with:
          files: ${{ steps.changed-files.outputs.all_changed_files }}
```

## 📄 Struktura danych organizacji

Każdy plik YAML organizacji powinien zawierać następującą strukturę:

```yaml
nazwa: "Przykładowa Organizacja Charytatywna"
adres: "przykladowa-organizacja"
strona: "https://example.org"
krs: "1234567890"
dostawa:
  ulica: "ul. Główna 1"
  kod: "00-001"
  miasto: "Warszawa"
  telefon: "+48 123 456 789"
produkty:
  - nazwa: "Produkt 1"
    link: "https://example.org/produkt1"
    opis: "Opcjonalny opis produktu"
  - nazwa: "Produkt 2"
    link: "https://example.org/produkt2"
```

### Opis pól

- **`nazwa`** *(wymagane)* - Pełna nazwa organizacji
- **`adres`** *(wymagane)* - Unikalny identyfikator strony (slug), używany w URL
- **`strona`** *(wymagane)* - Adres URL strony internetowej organizacji
- **`krs`** *(wymagane)* - 10-cyfrowy numer KRS organizacji
- **`dostawa`** *(wymagane)* - Dane adresowe dla dostaw
  - **`ulica`** - Nazwa ulicy i numer domu
  - **`kod`** - Kod pocztowy w formacie XX-XXX
  - **`miasto`** - Nazwa miasta
  - **`telefon`** - Numer telefonu (akceptowane formaty polskie)
- **`produkty`** *(wymagane)* - Lista produktów oferowanych przez organizację
  - **`nazwa`** - Nazwa produktu
  - **`link`** - Link do produktu
  - **`opis`** *(opcjonalne)* - Opis produktu

## ✅ Zasady walidacji

### Walidacja struktury
- Wszystkie wymagane pola muszą być obecne
- Pole `nazwa` nie może być puste
- Pole `adres` może zawierać tylko małe litery, cyfry i myślniki

### Walidacja KRS
- Numer KRS musi składać się z dokładnie 10 cyfr
- Numer jest sprawdzany w oficjalnym rejestrze KRS
- Nazwa organizacji w pliku musi być zgodna z nazwą w rejestrze KRS

### Walidacja dostaw
- Kod pocztowy musi być w formacie XX-XXX (np. 00-001)
- Numer telefonu musi być w polskim formacie

### Walidacja produktów
- Lista produktów musi zawierać co najmniej jeden element
- Każdy produkt musi mieć nazwę i link

### Kontrola konfliktów
- Pole `adres` musi być unikalne w całym zbiorze organizacji
- Zarezerwowane adresy (`info`, `organizacje`, `404`) są niedozwolone

## 🔧 Rozwój lokalny

### Wymagania

- Python 3.11+
- uv (zarządzanie zależnościami)

### Instalacja

```bash
# Klonowanie repozytorium
git clone https://github.com/twoj-uzytkownik/walidacja-organizacji.git
cd walidacja-organizacji

# Instalacja zależności
uv sync

# Aktywacja środowiska wirtualnego
source .venv/bin/activate
```

### Uruchamianie walidacji lokalnie

```bash
# Walidacja konkretnych plików
uv run python validate.py \
  --files "organizations/org1.yaml organizations/org2.yaml" \
  --organizations-dir "organizations" \
  --slug-field "adres"

# Sprawdzenie pojedynczego pliku
uv run python validate.py \
  --files "organizations/nowa-organizacja.yaml"
```

### Formatowanie i linting

```bash
# Formatowanie kodu
uv run ruff format .

# Sprawdzenie stylu kodu
uv run ruff check .
```

## 🧪 Testy

Projekt zawiera kompletny zestaw testów jednostkowych i integracyjnych.

### Uruchamianie testów

```bash
# Uruchomienie wszystkich testów
uv run pytest

# Uruchomienie z detalami
uv run pytest -v

# Uruchomienie konkretnego testu
uv run pytest tests/test_organization_schema.py
```

### Struktura testów

- `tests/test_organization_schema.py` - testy walidacji struktury organizacji
- `tests/test_krs_validation.py` - testy weryfikacji numerów KRS
- `tests/test_slug_conflicts.py` - testy wykrywania konfliktów adresów
- `tests/test_file_repository.py` - testy wczytywania plików
- `tests/test_integration.py` - testy integracyjne
- `tests/fixtures/` - przykładowe pliki YAML do testów

## 📊 Przykładowe komunikaty walidacji

### Sukces
```
=================================================
🚀 Rozpoczynam walidację organizacji...
Walidacja 1 pliku/ów organizacji...
Pole adres: adres
Zarezerwowane adresy stron: 404, info, organizacje

Walidacja organizations/przykład.yaml...
  ✅ Walidacja struktury zakończona pomyślnie

Sprawdzanie konfliktów adresów...
  ✅ Nie znaleziono konfliktów adresów

🎉 Wszystkie walidacje zakończone pomyślnie!
=================================================
```

### Błędy walidacji
```
=================================================
🚀 Rozpoczynam walidację organizacji...
Walidacja 1 pliku/ów organizacji...

Walidacja organizations/błędny.yaml...
  ❌ Walidacja struktury nie powiodła się:
     - Nieprawidłowy format KRS: 123 (oczekiwano 10 cyfr)
     - Nieprawidłowy format adres: Błędny_Adres (dozwolone tylko małe litery, cyfry i myślniki)
     - Brakuje wymaganego pola dostawy: dostawa.telefon

💥 Walidacja nie powiodła się!
=================================================
```

## 🤝 Współpraca

1. Fork projektu
2. Stwórz branch dla swojej funkcjonalności (`git checkout -b feature/nowa-funkcjonalnosc`)
3. Zatwierdź zmiany (`git commit -am 'Dodanie nowej funkcjonalności'`)
4. Wypchnij do brancha (`git push origin feature/nowa-funkcjonalnosc`)
5. Stwórz Pull Request

### Zasady rozwoju

- Dodaj testy dla nowych funkcjonalności
- Upewnij się, że wszystkie testy przechodzą
- Zastosuj formatowanie kodu z `ruff`
- Aktualizuj dokumentację jeśli to konieczne

## 📄 Licencja

Projekt udostępniony na licencji określonej w pliku [LICENSE](LICENSE).

## 🆘 Pomoc

Jeśli napotkasz problemy lub masz pytania:

1. Sprawdź [sekcję Issues](../../issues) w poszukiwaniu podobnych problemów
2. Stwórz nowy Issue z detalowym opisem problemu
3. Dołącz przykładowe pliki YAML i logi błędów

---

**Uwaga**: Ten action jest dedykowany użyciu w projekcie [wyślij.co](https://github.com/wyslijco) do weryfikacji polskich organizacji charytatywnych i korzysta z polskiego rejestru KRS.
