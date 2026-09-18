# Ćwiczenie 2B - Dataflow Gen2: ta sama transformacja bez kodu

![Architektura warsztatu, podświetlony fragment: Ćwiczenie 2](../assets/architecture/architektura-cw2.png)

> [!NOTE]
> Czas: 15 minut
>
> [Powrót do agendy](./../README.md#agenda) | [Wstecz: Ćwiczenie 2](./exercise-2.md) | [Dalej: Ćwiczenie 3](./../exercise-3/exercise-3.md)
>
> #### Lista zadań:
> * [Zadanie 2B.1 Utwórz Dataflow Gen2 z poziomu Lakehouse silver](#zadanie-2b1-utwórz-dataflow-gen2-z-poziomu-lakehouse-silver)
> * [Zadanie 2B.2 Wczytaj plik CSV](#zadanie-2b2-wczytaj-plik-csv)
> * [Zadanie 2B.3 Zrób unpivot w Power Query](#zadanie-2b3-zrób-unpivot-w-power-query)
> * [Zadanie 2B.4 Zapisz wynik w Lakehouse i uruchom Dataflow Gen2](#zadanie-2b4-zapisz-wynik-w-lakehouse-i-uruchom-dataflow-gen2)
> * [Zadanie 2B.5 Porównaj oba podejścia](#zadanie-2b5-porównaj-oba-podejścia)

# Kontekst

W Ćwiczeniu 2 Notebook zamienił plik `NYC-Taxi-Discounts-Per-Day.csv` z układu szerokiego na długi. Plik ma jedną kolumnę `VendorID` i osobną kolumnę dla każdego dnia. Notebook zrobił z tego trzy kolumny: `VendorID`, `date` i `discount`. Użył do tego funkcji `pd.melt()`.

Teraz zrobisz dokładnie to samo w Dataflow Gen2, czyli w Power Query. Nie napiszesz ani jednej linii kodu. Jeśli pracujesz w Power BI albo w Excelu, ten edytor już znasz.

Po tym ćwiczeniu samodzielnie odpowiesz na pytanie z tytułu warsztatu: kiedy Dataflow Gen2, a kiedy Notebook. Podsumowanie znajdziesz na stronie [Decyzje projektowe](../decyzje-projektowe.md).

> [!IMPORTANT]
> Potrzebujesz pliku `NYC-Taxi-Discounts-Per-Day.csv` na swoim dysku. Pochodzi z [Zadania 2.2](./exercise-2.md). Jeśli go nie masz, pobierz go [stąd](https://raw.githubusercontent.com/DamianWidera/SQLDayLite2026/main/exercise-2/NYC-Taxi-Discounts-Per-Day.csv).

---

# Zadanie 2B.1 Utwórz Dataflow Gen2 z poziomu Lakehouse silver

1. W swoim workspace otwórz Lakehouse `silvercleansed`.
2. Na karcie `Home` kliknij `Get data`, a potem `New Dataflow Gen2`.
3. W polu `Name` wpisz `df_discounts_unpivot` i kliknij `Create`.

> [!TIP]
> Dataflow Gen2 utworzony z poziomu Lakehouse od razu zna miejsce docelowe. Nie musisz go potem wskazywać ręcznie. Gdy tworzysz Dataflow Gen2 z poziomu workspace, miejsce docelowe dodajesz przyciskiem `Add data destination`.

---

# Zadanie 2B.2 Wczytaj plik CSV

1. Na karcie `Home` edytora kliknij kafelek `Import from a Text/CSV file`.
2. Na ekranie `Connect to data source` zaznacz `Upload file`.
3. Wskaż plik `NYC-Taxi-Discounts-Per-Day.csv` i kliknij `Next`.
4. Na ekranie `Preview file data` sprawdź podgląd i kliknij `Create`.

> [!NOTE]
> Plik jest bardzo szeroki, bo ma osobną kolumnę dla każdego dnia od 1 stycznia 2015 roku do 26 marca 2024 roku. Podgląd może ładować się kilkanaście sekund. Poczekaj, aż zobaczysz dane.

Sprawdź, czy pierwszy wiersz został użyty jako nagłówki. Pierwsza kolumna ma się nazywać `VendorID`, a kolejne mają mieć daty w nazwach. Jeśli widzisz nazwy `Column1`, `Column2`, kliknij na karcie `Home` przycisk `Use first row as headers`.

---

# Zadanie 2B.3 Zrób unpivot w Power Query

1. Kliknij nagłówek kolumny `VendorID`, żeby ją zaznaczyć.
2. Przejdź na kartę `Transform`. Rozwiń `Unpivot columns` i wybierz `Unpivot other columns`.
3. Edytor utworzy dwie nowe kolumny: `Attribute` i `Value`. Kliknij dwukrotnie nagłówek `Attribute` i zmień nazwę na `date`. Tak samo zmień `Value` na `discount`.
4. Ustaw typy danych. Kliknij ikonę typu po lewej stronie nagłówka kolumny:
   - `VendorID`: `Whole number`
   - `date`: `Date`
   - `discount`: `Whole number`
5. W panelu `Query settings` po prawej stronie zmień `Name` na `discounts_dataflow`. Ta nazwa stanie się nazwą tabeli w Lakehouse. Pisz ją małymi literami i bez spacji.

> [!TIP]
> Spójrz na listę `Applied steps` w panelu `Query settings`. Każde kliknięcie stało się osobnym krokiem. Kliknij dowolny krok, żeby zobaczyć dane w tamtym momencie. To jest odpowiednik komórek w Notebooku.

**Po tym zadaniu widzisz:** trzy kolumny `VendorID`, `date`, `discount`. Wynik ma 6746 wierszy, czyli 2 dostawców razy 3373 dni.

---

# Zadanie 2B.4 Zapisz wynik w Lakehouse i uruchom Dataflow Gen2

1. W panelu `Query settings` sprawdź sekcję `Data destination`. Powinien tam być Lakehouse `silvercleansed`, bo Dataflow Gen2 powstał z jego poziomu.
2. Jeśli sekcja jest pusta, kliknij `Add data destination`, wybierz `Lakehouse`, wskaż `silvercleansed`, zostaw nazwę tabeli `discounts_dataflow` i metodę `Replace`. Zakończ przyciskiem `Save settings`.
3. Kliknij `Save and run` na pasku narzędzi.
4. Poczekaj, aż wskaźnik postępu zniknie. Status sprawdzisz też w `Monitoring hub`.
5. Otwórz Lakehouse `silvercleansed`. Kliknij trzy kropki obok `Tables` i wybierz `Refresh`. Zobaczysz nową tabelę `discounts_dataflow`.

> [!IMPORTANT]
> Przy pierwszym Dataflow Gen2 w workspace Fabric tworzy w tle elementy o nazwach zaczynających się od `DataflowsStaging`. Mogą być widoczne w Notebooku albo w SQL analytics endpoint. Nie usuwaj ich i nie używaj bezpośrednio.

---

# Zadanie 2B.5 Porównaj oba podejścia

Otwórz obie tabele w Lakehouse `silvercleansed` i porównaj je:

- `discounts_dataflow`: wynik z Dataflow Gen2, sam unpivot,
- `green_202201_202301_discounts`: wynik z Notebooka, unpivot połączony z przejazdami.

Porozmawiaj z osobą obok albo z prowadzącymi:

| ID | Pytanie | Dataflow Gen2 | Notebook |
| :- | :- | :- | :- |
| P1 | Ile czasu zajął ci unpivot? | kilka kliknięć | kilka linii kodu |
| P2 | Kto w twoim zespole to utrzyma? | osoby znające Power Query | osoby znające Python albo SQL |
| P3 | Co, gdy plik urośnie tysiąc razy? | sprawdź czas i zużycie capacity | Spark skaluje się na wiele węzłów |
| P4 | Jak sprawdzisz, co się zmieniło w logice? | lista `Applied steps` | historia kodu w Git |

> [!TIP]
> Nie ma jednej dobrej odpowiedzi. W wielu projektach oba narzędzia pracują obok siebie: Dataflow Gen2 dla małych słowników i plików od biznesu, Notebook dla dużych tabel faktów. Więcej wskazówek znajdziesz na stronie [Decyzje projektowe](../decyzje-projektowe.md).

---

> [!IMPORTANT]
> Po zakończeniu przejdź do [agendy](./../README.md#agenda) albo od razu do [Ćwiczenia 3](./../exercise-3/exercise-3.md).
