# Ćwiczenie 2 - Transformacja danych w Notebookach i na klastrach Spark

![Architektura warsztatu, podświetlony fragment: Ćwiczenie 2](../assets/architecture/architektura-cw2.png)

> [!NOTE]
> Czas: 75 minut
> 
> [Powrót do agendy](./../README.md#agenda) | [Wstecz: Ćwiczenie 1](./../exercise-1/exercise-1.md) | [Dalej: Ćwiczenie 2B](./exercise-2b-dataflow-gen2.md)
> #### Lista zadań:
> * [Zadanie 2.1 Różne sposoby pobierania danych z Lakehouse](#zadanie-21-różne-sposoby-pobierania-danych-z-lakehouse)
> * [Zadanie 2.2 Side Loading (przesłanie pliku z dysku) i Load to Delta dla pliku CSV](#zadanie-22-side-loading-przesłanie-pliku-z-dysku-i-load-to-delta-dla-pliku-csv)
> * [Zadanie 2.3 Zaimportuj gotowy Notebook](#zadanie-23-zaimportuj-gotowy-notebook)
> * [Zadanie 2.4 Podłącz Lakehouse bronze](#zadanie-24-podłącz-lakehouse-bronze)
> * [Zadanie 2.5 Utwórz Lakehouse silver](#zadanie-25-utwórz-lakehouse-silver)
> * [Zadanie 2.6 Wykonaj Notebook krok po kroku](#zadanie-26-wykonaj-notebook-krok-po-kroku)
> * [Zadanie 2.7 Automatyzacja](#zadanie-27-automatyzacja)
> * [Zadanie 2.8 Potwierdź wyniki końcowe](#zadanie-28-potwierdź-wyniki-końcowe)
> * [Zadanie 2.9 Utwórz Lakehouse gold (wymagany w Ćwiczeniu 4)](#zadanie-29-utwórz-lakehouse-gold-wymagany-w-ćwiczeniu-4)



# Kontekst
W tym ćwiczeniu zajmiemy się pracą z obszaru Data Engineering. Przekształcimy dane surowe w dopracowaną warstwę silver.

Do końca warsztatu wdrożymy całą architekturę Medallion:
![Przegląd danych](../screenshots/2/intro.png)



> [!NOTE]
> Fabric dynamicznie dopasowuje zasoby obliczeniowe do historii użycia, szczytowego zapotrzebowania i bieżącej aktywności. Dziś pracuje nas jednocześnie prawie 600, głównie w tym samym regionie. Dlatego instancje obliczeniowe Spark mogą uruchamiać się dłużej niż zwykle. Zazwyczaj Starter pool uruchamia nową Spark session w około 10 sekund. Przy dzisiejszym obciążeniu możemy jednak przejść na pulę on-demand. Wtedy część sesji wystartuje dopiero po około 2–3 minutach.

---

# Zadanie 2.1 Różne sposoby pobierania danych z Lakehouse

W tym zadaniu poznasz różne metody pobierania danych z Lakehouse do Notebooka na potrzeby analizy. Poniżej znajdziesz instrukcje krok po kroku, które wykonasz w swoim Notebooku.

## 2.1.1. Podstawy uruchamiania kodu
Pamiętaj: żeby uruchomić kod w komórce, naciśnij CTRL + Enter w systemie Windows albo ⌘ + Enter w systemie macOS. Możesz też kliknąć ikonę `Run` (▶️) obok komórki z kodem.

## 2.1.2. Pobieranie danych za pomocą PySpark
Wpisz poniższy kod PySpark w nowej komórce swojego Notebooka w Fabric. Skrypt pobierze dane ze wskazanej tabeli w Lakehouse. Jeśli twój Lakehouse i twoja tabela nazywają się inaczej, zastąp `bronzerawdata` i green202301 swoimi nazwami.

> [!TIP]
> To powtórka z Ćwiczenia 1.3.11, ale z dodatkowym objaśnieniem. Pomiń ten krok, jeśli nie potrzebujesz objaśnienia kodu.

```python
df = spark.sql("SELECT * FROM bronzerawdata.green202301 LIMIT 1000")
display(df)
```

Objaśnienie kodu:
`df = spark.sql("SELECT * FROM bronzerawdata.green202301 LIMIT 1000")` - Ta linia kodu używa funkcji `spark.sql()`, żeby uruchomić zapytanie SQL na tabeli `green202301`, która znajduje się w Lakehouse `bronzerawdata`. Zapytanie wybiera wszystkie kolumny `(*)` z tabeli, a klauzula `LIMIT 1000` ogranicza wynik do pierwszych 1000 wierszy. Wynik zapytania trafia do PySpark DataFrame o nazwie `df`. `display(df)` - funkcja `display()` pokazuje zawartość DataFrame w postaci tabeli. W tym przypadku pokazuje zawartość DataFrame df utworzonego w poprzedniej linii.


## 2.1.3. Wiele języków programowania w Notebookach Fabric
Notebooki Fabric obsługują różne języki programowania, między innymi PySpark, Scala, SQL i R. Żeby przełączyć się na przykład na SQL, wpisz magiczne polecenie %%sql na początku komórki Notebooka.

![Krok](../screenshots/2/new/6.jpg)

```python
%%sql
SELECT * FROM bronzerawdata.green202301 LIMIT 1000
```

Teraz uruchomimy konkretne polecenie wyboru danych. Polecenie wybiera określone kolumny z DataFrame i wyświetla pierwsze pięć wierszy:

```python
%%pyspark
df.select("VendorID", "trip_distance", "fare_amount", "tip_amount").show(5)
```

Kod `df.select("VendorID", "trip_distance", "fare_amount", "tip_amount").show(5)` wyświetla pierwsze pięć wierszy DataFrame o nazwie df i tylko kolumny o nazwach: `vendorID`, `tripDistance`, `fareAmount`, `tipAmount`. Ta funkcja przydaje się przy dużych zbiorach danych. Pozwala szybko obejrzeć dane i sprawdzić, czy załadowały się poprawnie.


## 2.1.4. Jak wygląda przepływ pracy z danymi
Przy dużych zbiorach danych pracę zaczynasz od pobrania danych. To podstawa kolejnych zadań analitycznych, takich jak filtrowanie, sortowanie i agregowanie danych. Z czasem trafisz na bardziej złożone zadania z obszaru Data Engineering, takie jak oczyszczanie, transformacja i agregacja. Bez nich nie da się prowadzić zaawansowanej analizy danych ani wyciągać z nich wniosków.


---


# Zadanie 2.2 Side Loading (przesłanie pliku z dysku) i Load to Delta dla pliku CSV

Chcemy rozszerzyć warstwę bronze o dodatkowe dane. Poniższa tabela pokazuje aktualny obraz tego, jakie dane ładujemy do warstwy bronze i jakimi metodami to robimy.
![Trzy zbiory danych i trzy sposoby integracji](../assets/architecture/dane-cw2.png)


Ta instrukcja przeprowadzi cię przez pobranie danych zewnętrznych i dołączenie ich do twojego Lakehouse, żeby analiza była pełna.

## 2.2.1. Pobierz dane
Otwórz w nowej karcie [podany adres URL](https://raw.githubusercontent.com/DamianWidera/SQLDayLite2026/main/exercise-2/NYC-Taxi-Discounts-Per-Day.csv) i pobierz plik CSV z informacjami o zniżkach przyznanych użytkownikom w danym dniu. Te dane są niezbędne do pełnej analizy. Wygenerowaliśmy je dla twojej wygody. 

> [!TIP]
> Pobierz plik na swój komputer z tego linku: [Pobierz dane o zniżkach](https://raw.githubusercontent.com/DamianWidera/SQLDayLite2026/main/exercise-2/NYC-Taxi-Discounts-Per-Day.csv).

![Krok](../screenshots/2/new/7.jpg)

## 2.2.2. Prześlij dane do Lakehouse
Żeby połączyć dane o zniżkach z istniejącymi zbiorami danych:
* Przejdź do sekcji `Files` w swoim Lakehouse. 
* Kliknij trzy kropki, żeby zobaczyć dodatkowe opcje, i wybierz przycisk `Upload`. 
* Wybierz z menu `Upload Files`.
![Krok](../screenshots/2/new/10.jpg)

## 2.2.3. Wybierz plik do przesłania
Wybierz pobrany przed chwilą plik, który prawdopodobnie nazywa się NYC-Taxi-Discounts-Per-Day.csv. Następnie kliknij przycisk `Upload`, żeby rozpocząć przesyłanie.
![Krok](../screenshots/2/new/11.jpg)

## 2.2.4. Sprawdź, czy plik trafił do Lakehouse
Plik powinien przesłać się w kilka sekund. To prosty sposób na uzupełnienie danych w Lakehouse.
![Krok](../screenshots/2/new/12.jpg)

## 2.2.5. Odśwież widok i znajdź plik
Odśwież sekcję `Files` w Lakehouse, żeby zobaczyć nowo przesłany plik. Przeciągnij ten plik i upuść go w swoim Notebooku. Powstanie komórka z gotowym kodem. Uruchom ją, żeby obejrzeć nowe dane.
![Krok](../screenshots/2/new/13.jpg)

## 2.2.6. Zmień nazwę Notebooka
Nadaj Notebookowi nazwę, która oddaje jego przeznaczenie, na przykład `Data Exploration` albo `Discount Analysis`. Dzięki temu utrzymasz porządek w swoich projektach.
![Krok](../screenshots/2/new/14.jpg)

[//]: # (![Krok]&#40;../media/2/8.jpg&#41;)

---

# Zadanie 2.3 Zaimportuj gotowy Notebook

> [!NOTE]  
> Do workspace w Fabric możesz zaimportować jeden lub więcej istniejących Notebooków ze swojego komputera. Notebooki Fabric rozpoznają standardowe pliki Jupyter Notebook .ipynb oraz pliki źródłowe, takie jak .py, .scala i .sql, i tworzą z nich odpowiednie nowe elementy typu Notebook.

## 2.3.1. Zaimportuj Notebook
Jeśli nie masz pobranego repozytorium ([Krok 14. Pobierz pliki do ćwiczeń](../exercise-0-setup/start.md#14-pobierz-pliki-do-ćwiczeń)), **możesz pobrać sam Notebook. [Ten zrzut ekranu pokazuje, jak to zrobić.](../screenshots/extra/download-notebook.jpg)**

Przejdź do swojego workspace i wybierz `Import`. Znajdziesz tam opcję przesyłania Notebooków, oznaczoną ikoną Notebooka. 

Kliknij tę ikonę, żeby otworzyć boczny panel przesyłania, znany ci z wcześniejszego przesyłania pliku. Wybierz w nim pobrany przed chwilą Notebook o nazwie [notebook-2.ipynb](https://github.com/DamianWidera/SQLDayLite2026/blob/main/exercise-2/notebook-2.ipynb) i rozpocznij przesyłanie.
![Krok](../screenshots/2/new/importnotebook.jpg)

## 2.3.2. Powiadomienie
Gdy rozpoczniesz przesyłanie, zobaczysz powiadomienie, że trwa import pliku. Poczekaj, aż proces się zakończy. Zwykle trwa to tylko chwilę.
![Krok](../screenshots/2/new/15.jpg)

## 2.3.3. Otwórz zaimportowany Notebook
Po zakończeniu importu znajdź nowo zaimportowany Notebook w swoim workspace `Fabric Workshop September NNN`. Kliknij trzy kropki przy Notebooku i wybierz `Open Notebook`. Dla wygody możesz otworzyć Notebook w tle. Wtedy jego ikona będzie stale dostępna na pionowym pasku bocznym po lewej stronie.
![Krok](../screenshots/2/new/16.jpg)


Gratulacje, zadanie wykonane. Gotowy Notebook poszerza twoje możliwości w obszarze Data Engineering.

---


# Zadanie 2.4 Podłącz Lakehouse bronze
Ta instrukcja krok po kroku pomoże ci połączyć Lakehouse z gotowym Notebookiem, żeby sprawnie przetwarzać i analizować dane.

## 2.4.1. Otwórz opcje Lakehouse
W otwartym Notebooku znajdź sekcję Data items w panelu Explorer po lewej stronie.
![Krok](../screenshots/2/new/17.jpg)

## 2.4.2. Dodaj Lakehouse
W opcjach Lakehouse kliknij przycisk `Add data items`, żeby rozpocząć łączenie Lakehouse z Notebookiem. Następnie wybierz `Existing Lakehouse` spośród dostępnych opcji.
![Krok](../screenshots/2/new/18.jpg)

## 2.4.3. Wybierz swój Lakehouse
Na liście dostępnych Lakehouse znajdź i wybierz swój, o nazwie `bronzerawdata`. Uważaj, żeby wybrać właściwy, bo od tego zależy poprawność analizy danych. Po upewnieniu się kliknij `Connect`, żeby podłączyć go do Notebooka.
![Krok](../screenshots/2/new/19.jpg)

## 2.4.4. Potwierdzenie
Sprawdź, czy twój Lakehouse `bronzerawdata` jest teraz poprawnie połączony i widoczny w ustawieniach Notebooka. Jeśli tak, możesz wykonywać w Notebooku zadania na danych.
![Krok](../screenshots/2/new/20.jpg)


---


# Zadanie 2.5 Utwórz Lakehouse silver
Zanim w pełni zajmiemy się pracą z obszaru Data Engineering w Notebooku, zostało ostatnie zadanie: utworzyć i podłączyć nowy Lakehouse silver. Wykonaj te kroki:

## 2.5.1. Kliknij ikonę pinezki `Add data items` nad domyślnym Lakehouse `bronzerawdata`. Następnie wybierz opcję `New lakehouse`.
![Krok](../screenshots/2/new/21.jpg)

## 2.5.2. Wpisz nazwę Lakehouse zgodną z konwencją nazw. Sugerowana nazwa to `silvercleansed`.
![Krok](../screenshots/2/new/22.jpg)

> [!IMPORTANT]
> Zanim utworzysz Lakehouse, odznacz pole `Lakehouse schemas`. Pole jest domyślnie zaznaczone. Kod w Notebookach tego warsztatu używa nazw dwuczłonowych, np. `silvercleansed.nazwa_tabeli`. W Lakehouse z włączonym schema taka nazwa oznacza `schema.tabela`, więc zapis trafi w złe miejsce albo zakończy się błędem. Na zrzucie ekranu tego pola może jeszcze nie być.

## 2.5.3. Sprawdź, czy twój Notebook jest teraz połączony z dwoma Lakehouse: domyślnym (bronze) i nowo dodanym (silver). Gdy to potwierdzisz, możemy zacząć pracę z obszaru Data Engineering.
![Krok](../screenshots/2/new/23.jpg)

---

# Zadanie 2.6 Wykonaj Notebook krok po kroku

W tym zadaniu postępuj zgodnie z Notebookiem, zawartym w nim kodem i wszystkimi instrukcjami zapisanymi w kodzie. **Uruchom tam wszystkie komórki z kodem i wykonaj wszystkie kroki.** 

> [!IMPORTANT]
> Fabric Spark stosuje throttling i kolejkuje Spark joby na podstawie liczby rdzeni. Użytkownicy mogą przesyłać joby w granicach zakupionego SKU Fabric capacity. Kolejka działa według prostej zasady FIFO: sprawdza, czy są wolne miejsca na joby, i automatycznie ponawia je, gdy capacity się zwolni. Może się zdarzyć, że prześlesz job z Notebooka lub Lakehouse, np. Load to Table, gdy capacity jest w pełni wykorzystane, bo równolegle działające joby zajmują wszystkie Spark Vcores dostępne w zakupionym SKU Fabric capacity. Wtedy zadziała throttling i zobaczysz komunikat **HTTP Response code 430: Unable to submit this request because all the available capacity is currently being used. The suggested solutions are to cancel a currently running job, increase the available capacity, or try again later.**

> [!NOTE]
> Stan na wrzesień 2026 roku: aktualny komunikat brzmi `[TooManyRequestsForCapacity] HTTP Response code 430: This Spark job can't be run because you have hit a Spark compute or API rate limit.` Kolejka obejmuje tylko joby uruchamiane z Pipeline, z harmonogramu i ze Spark Job Definition. Interaktywne joby z Notebooka nie trafiają do kolejki, tylko od razu dostają błąd 430. Na Fabric trial capacity kolejkowanie nie działa wcale.

Zadanie 2.6 w Notebooku zakończysz, gdy dojdziesz do ostatniej komórki z kodem. Odeśle cię ona z powrotem tutaj, do Zadania 2.7. 

> [!TIP]  
> Jeśli masz już za sobą Notebook 2.6 i szukasz trudniejszych wyzwań, przejrzyj Notebook i wypisz wszystkie ulepszenia, które proponujesz. Celowo zostawiliśmy kilka miejsc, które można poprawić. Gdy je znajdziesz, porozmawiaj o nich z prowadzącymi.
> 
> **Powtórz ćwiczenie z [Zadania 1.4 Zarządzanie Spark session](./../exercise-1/exercise-1.md#zadanie-14-zarządzanie-spark-session) i sprawdź, czy masz jeszcze inne trwające, aktywne Spark session. Jeśli tak, anuluj je.**

---

# Zadanie 2.7 Automatyzacja

Gratulacje, masz za sobą zaawansowany Notebook z obszaru Data Engineering. Teraz zajmiemy się automatyzacją. Mamy tylko dwie tabele, ale wyobraź sobie, że musisz przetworzyć 50 tabel albo 50 różnych źródeł danych Parquet. W takiej sytuacji najlepiej postawić na Data pipeline i go zbudować. Taki jest cel tego zadania: wprowadzić automatyzację.


> [!TIP]
> Odśwież swój Lakehouse i sprawdź jeszcze raz, czy tabele w nim są.
> ![Krok](../screenshots/2/new/24.jpg)

## Kontrola jakości przed automatyzacją
Zanim zaczniesz automatyzację, sprawdź, czy:
* Lakehouse `bronzerawdata` zawiera dwie tabele: `green_202201_202301` i `green202301`.
* Lakehouse `bronzerawdata` ma w sekcji Files jeden folder o nazwie `2023`, utworzony przez Shortcut.
* Lakehouse `bronzerawdata` ma w sekcji Files jeden plik: `NYC-Taxi-Discounts-Per-Day.csv`.
* Lakehouse `silvercleansed` zawiera trzy tabele: `green_202201_202301_avg_fare_per_month`, `green_202201_202301_cleansed` i `green_202201_202301_discounts`.

Gdy wszystko się zgadza, przejdź do automatyzacji.

## 2.7.1. **Punkt wyjścia**
Upewnij się, że jesteś w swoim workspace w Fabric. Wybierz `New item`, a następnie `Pipeline`.
![Krok](../screenshots/2/new/25.jpg)

## 2.7.2. **Nazwij i utwórz Pipeline**
Nazwij nowy Pipeline `Bronze2Silver` i kliknij `Create`.
![Krok](../screenshots/2/new/26.jpg)

## 2.7.3. **Activity w Pipeline**
Wybierz activity `ForEach`, tak jak na zrzucie ekranu.
![Krok](../screenshots/2/new/27.jpg)

## 2.7.4. **Ustawienia ogólne activity ForEach**
Nadaj nazwę elementowi `ForEach`.
![Krok](../screenshots/2/new/28.jpg)

## 2.7.5. **Zmienne Pipeline**
Najpierw kliknij tło kanwy Pipeline (pierwszy krok na zrzucie ekranu, w różowym prostokącie), żeby zobaczyć kartę z parametrami i zmiennymi.

Na karcie ustawień Pipeline przejdź do `Variables`. Utwórz tam nową zmienną o nazwie `table_name`, ustaw jej typ na `Array` i przypisz wartość domyślną `["green_202201_202301", "green202301"]`. **Wykonaj dokładnie kroki pokazane na zrzucie ekranu.**

![Krok](../screenshots/2/new/29.jpg)

## 2.7.6. **Ustawienia ForEach**
W ustawieniach `ForEach` zaznacz `Sequential`. Żeby dodać dynamic content, otwórz panel boczny i wybierz zmienną `table_name`. Potwierdź, klikając `OK`. **Wykonaj dokładnie kroki pokazane na zrzucie ekranu.**

![Krok](../screenshots/2/new/30.jpg)
![Krok](../screenshots/2/new/31.jpg)

> [!NOTE]  
> Sequential określa, czy pętla ma się wykonywać sekwencyjnie, czy równolegle. Równolegle może się wykonywać jednocześnie najwyżej 50 iteracji pętli. Przykład: masz activity ForEach, która iteruje po Copy activity z 10 różnymi zestawami danych źródłowych i docelowych, a isSequential ma wartość False. Wtedy wszystkie kopie wykonują się naraz.
> 
> Tryb "Sequential" nie musi być najlepszą strategią w tym zadaniu, zwłaszcza że chcemy uruchomić ten sam Notebook dla dwóch różnych tabel równolegle. Jeśli masz ten sam wniosek, to bardzo trafne spostrzeżenie. Porozmawiaj o tym z prowadzącymi.


## 2.7.7. **Dodaj activity Notebook**
W `Activities` wybierz `Notebook`.
![Krok](../screenshots/2/new/32.jpg)

## 2.7.8. **Ustawienia Notebooka**
Zaznacz activity Notebook i przejdź na kartę `Settings` Notebooka, tak jak na zrzucie ekranu. Ustaw workspace i Notebook: jako workspace wybierz swój bieżący workspace, a jako Notebook wskaż przesłany wcześniej `notebook-2`.
![Krok](../screenshots/2/new/33.jpg)

## 2.7.9. **Wybierz Base Parameters**
Dodaj nowy parametr o nazwie `table_name`, typu `String`, z wartością `@item()`. `@item()` znów pochodzi z dynamic content (Pipeline expression builder).
![Krok](../screenshots/2/new/34.jpg)

## 2.7.10. **Walidacja**
Po konfiguracji kliknij `Validate`, żeby sprawdzić, czy nie ma błędów.
![Krok](../screenshots/2/new/35.jpg)

## 2.7.11. **Uruchomienie**
Zapisz ustawienia i uruchom Pipeline przyciskiem `Run`.
![Krok](../screenshots/2/new/36.jpg)

## 2.7.12. **Obserwacja i optymalizacja**
Zwróć uwagę, że dwa Notebooki wykonują się jeden po drugim, a każdy trwa zwykle około dwóch minut. Te Notebooki nie zależą jednak od siebie. Rozważ więc taką zmianę Pipeline, żeby dla większej wydajności uruchamiał Notebooki równolegle.

![Krok](../screenshots/2/new/37.jpg)

> [!TIP]
> (1) Zamiast iterować po Notebookach w pętli ForEach, możesz przekazać różne wartości do jednego uruchomienia Notebooka. Uzupełnieniem mogą być pętle zakodowane w samym Notebooku. 
> 
> (2) Użyj metody `notebookutils.notebook.runMultiple()`, żeby uruchomić wiele Notebooków równolegle. Zyskasz wydajność i oszczędzisz czas. Ta metoda przydaje się szczególnie wtedy, gdy nie musisz czekać na zakończenie jednego Notebooka, żeby uruchomić następny. Wprowadzenie i szczegóły użycia zobaczysz po uruchomieniu `notebookutils.notebook.help("runMultiple")`. Przykład: 
> `notebookutils.notebook.runMultiple(["NotebookA", "NotebookB"])`
> 
> Dawna nazwa `mssparkutils` nadal działa, ale zostanie wycofana. Szczegóły znajdziesz w [dokumentacji NotebookUtils](https://learn.microsoft.com/fabric/data-engineering/notebook-utilities).
> 
> Więcej o tej funkcji przeczytasz [w dokumentacji](https://learn.microsoft.com/en-us/fabric/data-engineering/microsoft-spark-utilities#reference-run-multiple-notebooks-in-parallel).

--- 

**Gratulacje, to ważny kamień milowy w automatyzacji z obszaru Data Engineering. Znacznie lepiej radzisz sobie teraz z automatyzacją procesów przetwarzania danych.**

---

# Zadanie 2.8 Potwierdź wyniki końcowe

Po ukończeniu Ćwiczeń 1 i 2 koniecznie sprawdź w swoich Lakehouse poniższe wyniki:

## Potwierdzenie dla Lakehouse `bronzerawdata`:
1. **Tabele**: Sprawdź, czy są dwie tabele: `green_202201_202301` i `green202301`.
2. **Sekcja Files**: Sprawdź, czy jest jeden folder o nazwie `2023`, utworzony przez Shortcut.
3. **Plik**: Sprawdź, czy w sekcji Files jest jeden plik: `NYC-Taxi-Discounts-Per-Day.csv`.

![Krok](../screenshots/2/52.jpg)

## Potwierdzenie dla Lakehouse `silvercleansed`:
1. **Tabele**: Sprawdź, czy jest sześć tabel:
   - `green_202201_202301_avg_fare_per_month`
   - `green_202201_202301_cleansed`
   - `green_202201_202301_discounts`
   - `green202301_avg_fare_per_month`
   - `green202301_cleansed`
   - `green202301_discounts`.

![Krok](../screenshots/2/51.jpg)

Porównaj swoje Lakehouse ze zrzutami ekranu i potwierdź, że ich zawartość odpowiada oczekiwanej strukturze.

---

# Zadanie 2.9 Utwórz Lakehouse gold (wymagany w Ćwiczeniu 4)

Zanim zajmiemy się w Notebooku pracą z obszaru Data Science (Ćwiczenie 4), zostało ostatnie zadanie: utworzyć nowy Lakehouse gold o nazwie `goldcurated`.

Wykonaj te kroki:
## 2.9.1. W widoku wszystkich artefaktów utworzonych w twoim workspace kliknij przycisk `New Item`.
![Krok](../screenshots/2/new/38.jpg)

## 2.9.2. Następnie wybierz `Lakehouse` z długiej listy.
![Krok](../screenshots/2/new/39.jpg)

## 2.9.3. Wpisz nazwę Lakehouse zgodną z konwencją nazw. Sugerowana nazwa to `goldcurated`.
![Krok](../screenshots/2/new/40.jpg)

> [!IMPORTANT]
> Zanim utworzysz Lakehouse, odznacz pole `Lakehouse schemas`. Pole jest domyślnie zaznaczone. Kod w Notebookach tego warsztatu używa nazw dwuczłonowych, np. `silvercleansed.nazwa_tabeli`. W Lakehouse z włączonym schema taka nazwa oznacza `schema.tabela`, więc zapis trafi w złe miejsce albo zakończy się błędem. Na zrzucie ekranu tego pola może jeszcze nie być.

## 2.9.4. Sprawdź, czy twój Lakehouse gold został utworzony.
![Krok](../screenshots/2/new/41.jpg)



> [!IMPORTANT]
> Po zakończeniu przejdź do [następnego ćwiczenia (Ćwiczenie 3)](./../exercise-3/exercise-3.md). Jeśli przed kolejnym ćwiczeniem zostanie ci czas, możesz zająć się [krokami dodatkowymi](../exercise-extra/extra.md).

