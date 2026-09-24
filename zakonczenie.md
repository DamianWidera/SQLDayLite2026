# Finał: pokaż swój raport

![Architektura rozwiązania zbudowanego na warsztacie](./assets/architecture/architektura.png)

> [!NOTE]
> Czas: 55 minut | [Powrót do agendy](./README.md#agenda) | [Decyzje projektowe](./decyzje-projektowe.md)
>
> #### Plan bloku:
> * [1. Sprawdź, co masz w workspace (5 minut)](#1-sprawdź-co-masz-w-workspace-5-minut)
> * [2. Pokaż swój raport (15 minut)](#2-pokaż-swój-raport-15-minut)
> * [3. Najczęstsze błędy początkujących (20 minut)](#3-najczęstsze-błędy-początkujących-20-minut)
> * [4. Twoja opinia (5 minut)](#4-twoja-opinia-5-minut)
> * [5. Co dalej (10 minut)](#5-co-dalej-10-minut)

Rano workspace był pusty. Teraz masz działające rozwiązanie: od plików źródłowych do raportu Power BI. Ten blok zamyka dzień.

## 1. Sprawdź, co masz w workspace (5 minut)

Otwórz swój workspace i odhacz listę:

| ID | Element | Gdzie to sprawdzisz |
| :- | :- | :- |
| F1 | Lakehouse `bronzerawdata` z tabelami `green_202201_202301` i `green202301` | Lakehouse explorer |
| F2 | Shortcut `2023` oraz plik `NYC-Taxi-Discounts-Per-Day.csv` w sekcji Files | Lakehouse `bronzerawdata` |
| F3 | Lakehouse `silvercleansed` z sześcioma tabelami `green_202201_202301_{cleansed, avg_fare_per_month, discounts}` i `green202301_{...}` oraz widokiem `viGetAverageFares` | Lakehouse explorer, SQL analytics endpoint |
| F4 | tabela `discounts_dataflow` z Dataflow Gen2 | Lakehouse `silvercleansed` |
| F5 | Pipeline z pętlą `ForEach` | lista elementów w workspace |
| F6 | Lakehouse `goldcurated` z tabelą `greentaxi_predicted` | Lakehouse explorer |
| F7 | semantic model w trybie Direct Lake i raport Power BI | lista elementów w workspace |

Nie masz któregoś elementu? To nic. Zapisz jego ID i wróć do niego po warsztacie. Repozytorium zostaje dostępne.

## 2. Pokaż swój raport (15 minut)

1. Otwórz swój raport Power BI z Ćwiczenia 4 na pełnym ekranie.
2. Pokaż go osobie obok. Masz dwie minuty.
3. Powiedz jedną rzecz, którą widać w danych, i jedną, którą warto zrobić inaczej.
4. Zamieńcie się rolami.

Chętni pokażą raport na dużym ekranie. Szukamy trzech różnych podejść, a nie najładniejszego raportu.

> [!TIP]
> Zrób zrzut ekranu raportu i widoku Lineage swojego workspace. To dobry materiał, żeby jutro pokazać zespołowi, co da się zbudować w Fabric w jeden dzień.

## 3. Najczęstsze błędy początkujących (20 minut)

Każdy błąd omawiamy tak samo: po czym go poznasz, czym się kończy i jak go uniknąć. Prowadzący dodają do każdego historię z projektu.

| ID | Błąd | Objaw | Skutek | Jak tego uniknąć |
| :- | :- | :- | :- | :- |
| B1 | Raportowanie na brudnych danych | raport czyta tabele z warstwy bronze albo pliki źródłowe | każda zmiana w źródle psuje raport, a liczby różnią się między raportami | raporty buduj tylko na warstwie gold. Czyszczenie rób raz, w warstwie silver |
| B2 | Mieszanie warstw | w jednym Lakehouse leżą dane surowe, oczyszczone i tabele do raportów | nikt nie wie, której tabeli można ufać | jeden Lakehouse na warstwę i nazwa, która mówi, co to za warstwa |
| B3 | Nadmiar narzędzi | ten sam krok raz jest w Dataflow Gen2, raz w Notebooku, raz w Pipeline | trudne szukanie błędów i wyższe zużycie capacity | jedno narzędzie na jeden typ zadania. Spisz tę zasadę na stronie projektu |
| B4 | Brak konwencji nazw | elementy `test2`, `Notebook 5`, `final_final` | po miesiącu nikt nie wie, co można usunąć | ustal konwencję pierwszego dnia, tak jak w [konwencji nazw](./exercise-0-setup/naming-convention.md) |
| B5 | Zbyt szerokie uprawnienia | wszyscy mają rolę Admin albo Member w workspace | przypadkowe usunięcia i dostęp do danych, których ktoś nie powinien widzieć | analitykom udostępniaj sam Lakehouse albo raport, tak jak w [Zadaniu 3.4](./exercise-3/exercise-3.md#zadanie-34-udostępnij-lakehouse) |
| B6 | Brak kontroli kosztów | Spark session działają godzinami, a capacity pracuje w nocy bez potrzeby | błędy HTTP 430 i rachunek wyższy niż w planie | mniejszy Spark pool, zatrzymywanie sesji, wstrzymywanie capacity z SKU F i przegląd aplikacji Fabric Capacity Metrics |

Historie prowadzących:

- B1: ⟦TBC historia z projektu⟧
- B2: ⟦TBC historia z projektu⟧
- B3: ⟦TBC historia z projektu⟧
- B4: ⟦TBC historia z projektu⟧
- B5: ⟦TBC historia z projektu⟧
- B6: ⟦TBC historia z projektu⟧

## 4. Twoja opinia (5 minut)

Wypełnij krótką ankietę, zanim zamkniesz laptop. Zeskanuj kod QR albo otwórz [formularz](https://forms.cloud.microsoft/e/hXHYaB8pDb).

<img src="assets/qr-ankieta.png" alt="Kod QR do ankiety o warsztacie" width="280">

## 5. Co dalej (10 minut)

| ID | Kiedy | Co zrobić |
| :- | :- | :- |
| N1 | jutro | pokaż zespołowi zrzut ekranu raportu i diagram architektury |
| N2 | w ciągu tygodnia | powtórz Ćwiczenie 1 i Ćwiczenie 2B na jednym własnym pliku z pracy |
| N3 | w ciągu tygodnia | przejdź [ćwiczenia dodatkowe](./exercise-extra/extra.md), na które dziś zabrakło czasu |
| N4 | w ciągu miesiąca | zbuduj jeden mały proces od źródła do raportu i przejdź z zespołem stronę [Decyzje projektowe](./decyzje-projektowe.md) |
| N5 | stale | śledź [Fabric Monthly Updates](https://blog.fabric.microsoft.com/en-us/blog/category/monthly-update) |

Na drogę weź [ściągę PDF](./assets/cheatsheet/sciaga-fabric.pdf): słowniczek i drzewka decyzji na jednej kartce.

Dziękujemy za wspólny dzień.
