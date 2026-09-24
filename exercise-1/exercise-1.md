# Ćwiczenie 1 - Ładowanie danych: Pipeline i Shortcut

![Architektura warsztatu, podświetlony fragment: Ćwiczenie 1](../assets/architecture/architektura-cw1.png)

> [!NOTE]
> Czas: 60 minut
>
> Zrzuty ekranu to orientacyjna pomoc, nie wzorzec jeden do jednego. Interfejs Fabric zmienia się co kilka tygodni, więc przyciski mogą być w innym miejscu, nazwy lekko inne, a część zrzutów pochodzi z wcześniejszych edycji warsztatu. Kieruj się tekstem kroku i nazwami w `kodzie`.
> 
> [Powrót do agendy](./../README.md#agenda) | [Wstecz: Start i konfiguracja](../exercise-0-setup/start.md) | [Dalej: Ćwiczenie 2](./../exercise-2/exercise-2.md)
> #### Lista zadań:
> * [Zadanie 1.1 Utwórz Pipeline, który ładuje dane z zewnętrznego konta Azure Blob Storage i zapisuje je w Lakehouse (warstwa bronze)](#zadanie-11-utwórz-pipeline-który-ładuje-dane-z-zewnętrznego-konta-azure-blob-storage-i-zapisuje-je-w-lakehouse-warstwa-bronze)
> * [Zadanie 1.2 Poznaj Lakehouse](#zadanie-12-poznaj-lakehouse)
> * [Zadanie 1.3 Utwórz Shortcut](#zadanie-13-utwórz-shortcut)
> * [Zadanie 1.4 Zarządzanie Spark session](#zadanie-14-zarządzanie-spark-session)

# Kontekst
Zintegrujemy dwa źródła danych NYC Taxi: jedno z okresu od stycznia 2022 do stycznia 2023 roku, drugie ze stycznia 2023 roku. Grafika poniżej pokazuje oba zbiory danych i sposób ich integracji:
![Dwa zbiory danych i dwa sposoby integracji](../assets/architecture/dane-cw1.png)

Przegląd zadań:
* Ładowanie danych: zacznij od załadowania danych historycznych z okresu od stycznia 2022 do stycznia 2023 roku. Leżą one w Azure Blob Storage, czyli w usłudze, która kiedyś była szczytowym osiągnięciem wśród rozwiązań do przechowywania danych. Ten krok symuluje przeniesienie starszych danych do nowoczesnego ekosystemu danych.
* Integracja i analiza danych: teraz zajmij się nowszymi danymi, ze stycznia 2023 roku. W tym czasie standardem przechowywania danych w Azure stało się Azure Data Lake Storage Gen 2 (ADLS Gen2). Zamiast tradycyjnie kopiować dane, użyjesz nowatorskiej funkcji `Shortcuts`, która upraszcza integrację w naszej architekturze Lakehouse.

Do końca warsztatu ukończymy pierwszy etap Medallion architecture, czyli warstwę bronze:
![Warstwa bronze: strefa lądowania danych surowych](../assets/architecture/bronze-landing.png)

Dla osób, które skończą główne zadania przed czasem, przygotowaliśmy [dodatkowe wyzwania](../exercise-extra/extra.md). Pomogą ci lepiej zrozumieć data engineering i rozwinąć umiejętności w tym obszarze. Znajdziesz je na dole strony. Pytania są mile widziane, a nawet do nich zachęcamy. W trakcie całej sesji możesz zwrócić się do każdego z prowadzących. Współpraca i ciekawość to klucz do sukcesu w tym ćwiczeniu.

---

> [!TIP]
> To ćwiczenie jest obszerne, ale polega głównie na pracy z UI. Będziesz dużo klikać w różne elementy. Przygotuj się na pracę praktyczną i zbierz energię na aktywny udział.

# Zadanie 1.1 Utwórz Pipeline, który ładuje dane z zewnętrznego konta Azure Blob Storage i zapisuje je w Lakehouse (warstwa bronze)

## 1.1.1. **Sprawdź sekcję Fabric i workspace**
Sprawdź, czy jesteś w sekcji Fabric i w swoim workspace `Fabric Workshop September NNN`. Wykonaj ponumerowane kroki ze zrzutu ekranu.

![Krok](../screenshots/1/new/1.jpg)

## 1.1.2. **Utwórz nowy Pipeline** 
Kliknij `New item`, a następnie `Pipeline`. W starszych wersjach interfejsu ten element nazywał się `Data pipeline` i tak wygląda na części zrzutów ekranu.

> [!IMPORTANT]  
> Okno konfiguracji Pipeline może pojawić się z krótkim opóźnieniem. Poczekaj kilka sekund, aż okno załaduje się w całości. W tym oknie podasz nazwę Pipeline. Nie klikaj w tym czasie kilka razy, bo możesz przypadkiem utworzyć kilka Data pipeline.

![Krok](../screenshots/1/new/2.jpg)

## 1.1.3. **Nazwij Pipeline**
Nadaj nazwę Pipeline. Zalecamy `LoadRawTaxiData`. 

![Krok](../screenshots/1/new/3.jpg)

## 1.1.4. **Utwórz Pipeline Activity**
Wybierz `Pipeline Activity`, a następnie `Copy Data`.
![Krok](../screenshots/1/new/4.jpg)

## 1.1.5. **Edytuj elementy Pipeline**
Wprowadź zmiany i obserwuj, jak zmienia się obszar edycji na głównym ekranie.
![Krok](../screenshots/1/new/5.jpg)


## 1.1.6. **Skonfiguruj źródło danych**
Na karcie `Source` wybierz połączenie (`Select`) i kliknij `Browse all`.
![Krok](../screenshots/1/new/6.jpg)


## 1.1.7. **Dodaj połączenie z Blob Storage**
Kliknij przycisk `View more` i wybierz `Azure Blobs` dla nowego połączenia.
![Krok](../screenshots/1/new/7.jpg)


## 1.1.8. **Podaj szczegóły połączenia** 
   - Skopiuj adres URL z opisu zadania i wklej go w odpowiednie pole.
     - Adres URL konta Blob Storage `https://nyctaxidataforfabric.blob.core.windows.net/`
   - Jako typ połączenia wybierz `Create a new connection`.
   - Zostaw automatycznie wygenerowaną nazwę połączenia albo zmień ją, jeśli trzeba.
   - Data gateway zostaw jako (none).
   - Jako metodę uwierzytelniania wybierz `Shared Access Signature (SAS)`.

![Krok](../screenshots/1/new/8.jpg)

## 1.1.9. **Wpisz SAS token**
Wklej poniższy SAS token w pole `SAS token`. Token daje dostęp tylko do odczytu i wygasa w sobotę 26 września 2026 wieczorem.

SAS token:

```
?se=2026-09-26T22%3A00Z&sp=rl&spr=https&sv=2022-11-02&ss=b&srt=sco&sig=JjzHVUUzDm/kMYhgfnQCA5gGsGLfnvSWU%2BVBOFyHMDQ%3D
```

> [!TIP]
> Skopiuj całą linię, razem ze znakiem `?` na początku. Jeśli kopiujesz z GitHuba, użyj ikony kopiowania przy bloku kodu, żeby nie zgubić żadnego znaku.
![Krok](../screenshots/1/new/9.jpg)

## 1.1.10. **Przetestuj połączenie**
Sprawdź, czy nazwa połączenia wyświetla się poprawnie, a potem przetestuj połączenie. Jeśli test się powiedzie, kliknij `Browse`.
![Krok](../screenshots/1/new/10.jpg)

## 1.1.11. **Przejrzyj Blob Storage**
Przejrzyj Blob Storage: wejdź do kontenera `nyc` i wybierz folder `green_202201_202301`.

> Root folder > nyc > green_202201_202301
<!-- ![Krok](../screenshots/1/new/11.jpg) -->

## 1.1.12. **Wybierz cały folder z danymi**
Zaznacz **folder** `green_202201_202301`, nie pojedynczy plik, i kliknij `OK`. W folderze jest 13 plików Parquet, od `green_tripdata_2022-01.parquet` do `green_tripdata_2023-01.parquet`, wszystkie o tym samym schemacie. Wszystkie mają trafić do jednej tabeli. Jeśli zaznaczysz jeden plik, załadujesz tylko jeden miesiąc i Ćwiczenia 2 i 3 dadzą inne wyniki niż w instrukcji.
![Krok](../screenshots/1/new/12.jpg)

> [!NOTE]
> Zrzuty 12 i 13 pochodzą ze starszego konta storage (kontener `taxidata`, jeden plik z 2015 roku). U ciebie kontener nazywa się `nyc`, folder `green_202201_202301`, a w środku jest 13 plików. Układ okna jest ten sam, różnią się tylko nazwy.

## 1.1.13. **Ścieżka i format pliku**
Zwróć uwagę na dodatkowe elementy w sekcji ścieżki pliku. Wypełnione mają być tylko dwa pola: kontener `nyc` i folder `green_202201_202301`. Trzecie pole (nazwa pliku) zostaw puste, a opcję `Recursively` zostaw zaznaczoną. Zmień format pliku na `Parquet` i kliknij `Preview Data`.
![Krok](../screenshots/1/new/13.jpg)

## 1.1.14. **Podgląd danych zewnętrznych**
Przejrzyj podgląd danych, który pokazuje zawartość tabeli z zewnętrznego Blob Storage, a potem zamknij okno podglądu.
![Krok](../screenshots/1/new/14.jpg)

## 1.1.15. **Określ miejsce docelowe danych**
Przejdź na kartę `Destination`, wybierz połączenie (`Select`) i kliknij `Browse all`.
![Krok](../screenshots/1/new/15.jpg)

## 1.1.16. **Utwórz i nazwij Lakehouse**
W sekcji `New Fabric item` wybierz `Lakehouse`, aby utworzyć nowy Lakehouse. Jako workspace wybierz swój bieżący workspace. Nazwę ustal zgodnie z [podaną konwencją nazw](../exercise-0-setup/naming-convention.md), wpisz ją i kliknij `Create and connect`.
![Krok](../screenshots/1/new/16.jpg)

> [!IMPORTANT]
> Zanim utworzysz Lakehouse, odznacz pole `Lakehouse schemas`. Pole jest domyślnie zaznaczone. Kod w Notebookach tego warsztatu używa nazw dwuczłonowych, np. `silvercleansed.nazwa_tabeli`. W Lakehouse z włączonym schema taka nazwa oznacza `schema.tabela`, więc zapis trafi w złe miejsce albo zakończy się błędem. Na zrzucie ekranu tego pola może jeszcze nie być.

## 1.1.17. **Sprawdź Lakehouse**
Sprawdź, czy nowo utworzony Lakehouse jest widoczny na odpowiedniej karcie.
![Krok](../screenshots/1/new/17.jpg)

## 1.1.18. **Skonfiguruj opcje**
Wybierz akcję dla tabeli. Na zrzucie widać `Append`, ale zalecamy `Overwrite`. Jeśli uruchomisz Pipeline drugi raz, np. po błędzie albo po poprawieniu ścieżki źródłowej, `Append` doda dane jeszcze raz i tabela będzie miała zdublowane wiersze. Wskaż tabelę, klikając `New`.
![Krok](../screenshots/1/new/18.jpg)

## 1.1.19. **Ustaw nazwę tabeli**
Nazwij tabelę dokładnie `green_202201_202301` zgodnie z [konwencją nazw](../exercise-0-setup/naming-convention.md), kliknij `Create`, a potem wróć na kartę `General`. Na zrzutach 19 i 42 widać starszą nazwę `green201501`. Zignoruj ją, u ciebie ma być `green_202201_202301`.
![Krok](../screenshots/1/new/19.jpg)

## 1.1.20. **Opisz Copy activity**
Nadaj Copy activity nazwę, która mówi, do czego służy, np. `Load NYC Taxi Green 202201-202301`. Przejrzyj timeout i zasady ponawiania, a w razie potrzeby je zmień. Zajrzyj też do opcji zaawansowanych.
![Krok](../screenshots/1/new/20.jpg)

## 1.1.21. **Zweryfikuj i zapisz Pipeline**
Kliknij `Validate`, aby sprawdzić, czy Pipeline nie zawiera błędów. Po walidacji zamknij panel boczny i zapisz ustawienia Pipeline, klikając `Save`.
![Krok](../screenshots/1/new/21.jpg)

## 1.1.22. **Uruchom Pipeline**
Uruchom Pipeline, klikając `Run`.
![Krok](../screenshots/1/new/22.jpg)


> [!NOTE]
> Fabric dynamicznie dopasowuje inteligentne zasoby obliczeniowe na podstawie historii użycia, szczytowego zapotrzebowania i bieżącej aktywności. Dziś cała grupa pracuje jednocześnie w tym samym regionie, więc instancje obliczeniowe Spark mogą uruchamiać się dłużej niż zwykle. Zazwyczaj Starter pool uruchamia nową Spark session w około 10 sekund. Przy dzisiejszym obciążeniu możemy jednak przejść na on-demand pool, a wtedy na niektóre Spark session poczekasz około 2–3 minut.

## 1.1.23. **Monitoruj wykonanie Pipeline**
Zwróć uwagę na powiadomienie, że Pipeline jest uruchomiony, a potem przejdź na kartę `Output`.
![Krok](../screenshots/1/new/23.jpg)

## 1.1.24. **Potwierdź, że Pipeline zakończył się sukcesem**
Sprawdź czas zakończenia i upewnij się, że Pipeline zakończył się sukcesem. Kliknij wyróżnioną nazwę activity, aby zobaczyć szczegóły.
![Krok](../screenshots/1/new/24.jpg)

## 1.1.25. **Przejrzyj szczegóły transferu danych**
W panelu bocznym przejrzyj szczegóły, np. łączny czas trwania i ilość przesłanych danych. Potem wróć do swojego workspace, klikając ikonę oznaczoną numerem trzy.
![Krok](../screenshots/1/new/25.jpg)

## 1.1.26. **Przejdź do swojego workspace**
W workspace powinien być widoczny Pipeline `LoadRawTaxiData` i Lakehouse `bronzerawdata`. Otwórz Lakehouse.
![Krok](../screenshots/1/new/26.jpg)

## 1.1.27. **Przejrzyj tabelę z danymi**
W sekcji `Tables` znajdź nową tabelę i otwórz podgląd jej danych.

Sprawdź, czy załadowały się wszystkie miesiące. Otwórz `SQL analytics endpoint` (przełącznik `Lakehouse` w prawym górnym rogu) i uruchom:

```sql
SELECT COUNT(*) AS rows_total,
       MIN(lpep_pickup_datetime) AS first_trip,
       MAX(lpep_pickup_datetime) AS last_trip
FROM green_202201_202301;
```

Oczekiwany wynik: około 908 tys. wierszy, pierwszy przejazd w styczniu 2022, ostatni w styczniu 2023. Jeśli widzisz około 60-80 tys. wierszy, załadował się jeden plik. Wróć do kroku 1.1.12, zaznacz cały folder i uruchom Pipeline jeszcze raz z akcją `Overwrite`.

![Krok](../screenshots/1/new/27.jpg)

---


# Zadanie 1.2 Poznaj Lakehouse 

> [!TIP]
> Gratulacje, pierwsze i najważniejsze zadanie (Zadanie 1.1) Ćwiczenia 1 za tobą. 
>
> **Sprawdź teraz czas. Jeśli minęła już połowa czasu przeznaczonego na całe Ćwiczenie 1, rozważ pominięcie Zadania 1.2 i przejdź od razu do [1.3 Utwórz Shortcut](#zadanie-13-utwórz-shortcut)**, bo Zadania 1.3 wymaga `Ćwiczenie 2 - Transformacja danych w Notebookach i na klastrach Spark`.
> 
> Pamiętaj, że do tego ćwiczenia zawsze możesz wrócić później.

<details>

<summary>Kliknij <ins>tutaj</ins>, aby rozwinąć Zadanie 1.2 Poznaj Lakehouse </summary>

Lakehouse w Microsoft Fabric daje inżynierom danych i analitykom zalety zarówno magazynu data lake, jak i relacyjnej hurtowni danych. Apache Spark to kluczowa technologia analityki big data. Dzięki obsłudze Spark w Microsoft Fabric możesz płynnie łączyć przetwarzanie big data w Spark z innymi narzędziami do analizy i wizualizacji danych dostępnymi na platformie. 
Lakehouse pozwala zbudować kompletne rozwiązanie analityczne, które obejmuje ładowanie danych, transformację, modelowanie i wizualizację. Lakehouse to jednolita i skalowalna platforma do przechowywania danych i zarządzania nimi. Ułatwia dostęp do danych ustrukturyzowanych i nieustrukturyzowanych oraz ich analizę. Wbudowane funkcje bezpieczeństwa i zgodności pomagają dbać o bezpieczeństwo danych i ich zgodność ze standardami branżowymi.


**Fundamentem Microsoft Fabric jest Lakehouse**, zbudowany na skalowalnej warstwie przechowywania **OneLake**. Do przetwarzania big data używa silników obliczeniowych **Apache Spark** i **SQL**. Lakehouse to jednolita platforma, która łączy:
- elastyczne i skalowalne przechowywanie danych znane z data lake,
- możliwość wykonywania zapytań i analizy danych znaną z hurtowni danych.

Wybrane zalety Lakehouse:
- Lakehouse używa silników Spark i SQL do przetwarzania danych na dużą skalę oraz obsługuje uczenie maszynowe i analitykę predykcyjną.
- Dane w Lakehouse są zorganizowane w podejściu schema-on-read. Oznacza to, że schema definiujesz wtedy, gdy jej potrzebujesz, zamiast ustalać ją z góry.
- Lakehouse obsługuje transakcje ACID (Atomicity, Consistency, Isolation, Durability) dzięki tabelom w formacie Delta Lake, co zapewnia spójność i integralność danych.
- Lakehouse to jedno miejsce, w którym inżynierzy danych, specjaliści data science i analitycy danych mają dostęp do danych i z nich korzystają.

Lakehouse to dobry wybór, jeśli potrzebujesz skalowalnego rozwiązania analitycznego, które zachowuje spójność danych.

Wyobraź sobie, że twoja firma przechowuje w hurtowni danych ustrukturyzowane dane z systemu transakcyjnego NYC Taxi, takie jak historia przejazdów, liczba pasażerów i opłaty za przejazd. Zebrała też dane nieustrukturyzowane związane z NYC Taxi: z mediów społecznościowych, logów stron internetowych i źródeł zewnętrznych. Takimi danymi trudno zarządzać i trudno je analizować w obecnej infrastrukturze hurtowni danych.

Nowa wytyczna firmy brzmi: podejmować lepsze decyzje dzięki analizie danych w różnych formatach i z wielu źródeł. Firma decyduje się więc **użyć możliwości Microsoft Fabric, aby sprawniej analizować te różnorodne zbiory danych i nimi zarządzać**.


Zanim utworzysz Shortcut w Lakehouse, musisz rozumieć strukturę folderów tego elementu. Lakehouse składa się z dwóch folderów najwyższego poziomu: Tables i Files. Folder Tables to zarządzana część Lakehouse, a folder Files to część niezarządzana. W folderze Tables Shortcut możesz utworzyć tylko na najwyższym poziomie. W pozostałych podkatalogach folderu Tables Shortcut nie jest obsługiwany. Jeśli cel Shortcut zawiera dane w formacie Delta\Parquet, Lakehouse automatycznie synchronizuje metadane i rozpoznaje folder jako tabelę. W folderze Files nie ma ograniczeń co do miejsca, w którym tworzysz Shortcut. Możesz go utworzyć na dowolnym poziomie hierarchii folderów. W folderze Files tabele nie są wykrywane automatycznie.

![Shortcuts](https://learn.microsoft.com/en-us/fabric/onelake/media/onelake-shortcuts/lake-view-table-view.png)


## 1.2.1. **Poznaj tryby Lakehouse**
Z danymi w Lakehouse możesz pracować w dwóch trybach:

1. Lake mode pozwala dodawać tabele, pliki i foldery w Lakehouse oraz z nimi pracować.
2. **SQL Endpoint pozwala odpytywać tabele w Lakehouse za pomocą SQL i zarządzać jego relacyjnym modelem danych. Możesz w nim uruchamiać instrukcje Transact-SQL, aby odpytywać, filtrować, agregować i na inne sposoby eksplorować dane w tabelach Lakehouse.**

Data Warehouse w Fabric pozwala przejść z widoku lake w Lakehouse (który obsługuje Data Engineering i Apache Spark) do pracy z SQL, jaką daje tradycyjna hurtownia danych.

![Krok](../screenshots/1/new/28.jpg)

## 1.2.2. **Sprawdź właściwości Lakehouse**
W sekcji `Tables` w Lakehouse kliknij trzy kropki obok nazwy tabeli i wybierz `Properties` z menu rozwijanego.
![Krok](../screenshots/1/new/29.jpg)

## 1.2.3. **Format danych i zarządzanie**
Zwróć uwagę, że format danych tabeli to `Managed`, czyli tabela jest zarządzana. Sprawdź też, czy tabela została zapisana z optymalizacją V-Order. Szczegóły znajdziesz w sekcji dodatkowej.
![Krok](../screenshots/1/new/30.jpg)

> [!TIP]
> Porównaj tabele zarządzane i niezarządzane w Fabric Spark. [Przeczytaj artykuł naszego kolegi z zespołu, Aitora, który pracuje w Customer Advisory Team](https://murggu.medium.com/creating-managed-and-external-spark-tables-in-fabric-lakehouse-ef6212e75e81).

## 1.2.4. **Przejrzyj pliki tabeli**
Wróć do przeglądu Lakehouse, rozwiń opcje tabeli i wybierz `View Files`, aby obejrzeć dane. Załadowane dane mają format Parquet, a po konwersji są częścią Delta Lake.
![Krok](../screenshots/1/new/31.jpg)
![Krok](../screenshots/1/new/32.jpg)

## 1.2.5. **Końcowy przegląd Lakehouse**
Wróć do głównego widoku Lakehouse, po raz ostatni rozwiń opcje tabeli i wybierz `Maintenance`.
![Krok](../screenshots/1/new/33.jpg)

## 1.2.6. **Opcje konserwacji i optymalizacja**
Znajdziesz tu opcje optymalizacji rozmiaru plików oraz VACUUM, czyli usuwania plików, które nie są już potrzebne. Oba procesy można zautomatyzować. W tej sekcji zobaczysz też, jak do twoich danych stosowana jest optymalizacja V-Order. Najedź kursorem na ikonę informacji, aby zobaczyć szczegóły. W workspace utworzonych od kwietnia 2025 roku V-Order jest domyślnie wyłączony dla zapisów Spark (profil `writeHeavy`). Włączysz go ustawieniem `spark.sql.parquet.vorder.default` albo profilem `readHeavyForPBI`.
![Krok](../screenshots/1/new/34.jpg)

## 1.2.7. **Zakończenie zadania**
Znasz już funkcje Lakehouse i opcje konserwacji. To zadanie jest ukończone.

</details>


---


# Zadanie 1.3 Utwórz Shortcut
W tym zadaniu uzyskasz dostęp do danych NYC Taxi z 2023 roku i z nich skorzystasz. Wzbogacisz Lakehouse o kluczowe informacje finansowe bez kosztów tradycyjnego przenoszenia danych.

Twoja misja: uzyskać dostęp do danych NYC Taxi z 2023 roku, które gromadzą się od 1982 roku, i sprawić, żeby były od ręki dostępne w naszym środowisku Lakehouse do analiz i podejmowania decyzji. Liczą się tu wydajność i innowacyjność, bo chcemy usprawnić nasze operacje na danych.

Szczegóły zadania:
* W tym zadaniu użyjesz funkcji `Shortcuts`. To potężne narzędzie, które daje bezpośredni dostęp do danych bez kopiowania ich do Lakehouse. Oszczędzasz w ten sposób czas, obniżasz koszty przechowywania i zachowujesz integralność danych, bo nie powstają zbędne duplikaty.
* Dzięki strategii `Shortcuts` osiągniesz `Zero Data Movement`. Oznacza to, że wskażesz bezpośrednio istniejące dane NYC Taxi z 2023 roku. Dostęp i analiza działają wtedy w czasie rzeczywistym, bez kosztów tradycyjnego przesyłania danych.

Zalety tego podejścia:
* Wydajność: masz dostęp do danych w czasie rzeczywistym, bez opóźnień związanych z kopiowaniem dużych zbiorów danych.
* Niższe koszty: nie duplikujesz danych w Lakehouse, więc płacisz mniej za przechowywanie.
* Integralność danych: sięgasz po dane bezpośrednio w ich pierwotnej lokalizacji, więc zachowujesz jedno źródło prawdy.

Pamiętaj, że nasz zespół przeprowadzi cię przez każdy krok. Daj znać, jeśli napotkasz trudności albo masz pytania o funkcję `Shortcuts` i jej wdrożenie.


## 1.3.1. Rozwiń opcje plików
Rozwiń opcje sekcji plików: kliknij trzy kropki przy `Files`. Następnie wybierz opcję `New Shortcut`.
![Krok](../screenshots/1/new/35.jpg)

## 1.3.2. Opcje Shortcut
Masz do wyboru wiele źródeł, z których możesz korzystać bezpośrednio, bez kopiowania danych. Obecnie Shortcut obsługuje dane z OneLake, Azure Data Lake Storage Gen2, Azure Blob Storage, Amazon S3, magazynów zgodnych z S3, Google Cloud Storage, Dataverse oraz OneDrive i SharePoint. Do źródeł on-premises połączysz się przez gateway. Shortcut może też wskazywać tabele Iceberg. Wybierz `Azure Data Lake Storage Gen2`.
![Krok](../screenshots/1/new/36.jpg)

## 1.3.3. Skonfiguruj nowy Shortcut
Skopiuj adres URL z opisu zadania i wklej go. Następnie wybierz połączenie i w miarę możliwości zostaw automatycznie wygenerowaną nazwę. Jako metodę uwierzytelniania wybierz `Shared Access Signature (SAS)` i wklej podany token. Gdy uzupełnisz wszystkie dane, kliknij `Next`.

* Adres URL konta ADLS Gen2 `https://nyctaxiforfabric.dfs.core.windows.net/`
* SAS token (tylko odczyt, ważny do soboty 26 września 2026 wieczorem):

```
?se=2026-09-26T22%3A00Z&sp=rl&spr=https&sv=2022-11-02&ss=b&srt=sco&sig=%2Bxt3nZ1WZvGDkepk3sSW1B86/bxWCTv6EE6FT4S1Z2M%3D
```

> [!TIP]
> To inny token niż w kroku 1.1.9, bo to inne konto storage. Skopiuj całą linię razem ze znakiem `?`.


![Krok](../screenshots/1/new/37.jpg)

**Jeśli zobaczysz komunikat o błędzie `The specified connection name already exists. Try choosing a different name`, upewnij się, że nazwa połączenia jest unikalna.**

## 1.3.4. Sprawdź dostęp do ADLS Gen2
Sprawdź konfigurację: w drzewie po lewej rozwiń kontener `nyc`, potem `green_all`, potem `year=2023` i zaznacz folder `month=01`. W środku jest jeden plik Parquet: `green_tripdata_2023-01.parquet`. Kliknij `Next`. Na kolejnej stronie `Transform (Optional)` Fabric zaproponuje konwersję do Delta. Kliknij `Skip`, nie klikaj kafelka `Delta table`, bo chcemy zwykły folder w sekcji `Files`. Dopiero na stronie z podsumowaniem zmień nazwę Shortcutu z `month=01` na `2023` (kliknij ikonę ołówka przy nazwie), a potem kliknij `Create`.

> nyc > green_all > year=2023 > month=01

> [!IMPORTANT]
> Nazwa Shortcutu `2023` jest ważna, bo w Ćwiczeniu 2 sprawdzamy, czy w sekcji `Files` jest jeden folder o tej nazwie. Zrzuty ekranu poniżej pochodzą z innego konta storage, gdzie folder od razu nazywał się `2023`. U ciebie drzewo jest głębsze, ale plik jest ten sam.

![Krok](../screenshots/1/new/38.jpg)
![Krok](../screenshots/1/new/39.jpg)
![Krok](../screenshots/1/new/40.jpg)

## 1.3.5. Shortcut skonfigurowany
Masz już dostęp do danych przez Shortcut, bez ich kopiowania. Shortcut powinien być teraz widoczny w sekcji `Files` jako link do folderu z plikami Parquet.
![Krok](../screenshots/1/new/41.jpg)

## 1.3.6. Załaduj dane Parquet do tabeli (Delta table)
W sekcji `Files` kliknij folder `2023` utworzony przez Shortcut. W środku zobaczysz plik `green_tripdata_2023-01.parquet`. Aby przekształcić go w Delta table, kliknij trzy kropki obok nazwy pliku, tak jak na ekranie. Następnie wybierz `Load to Tables` i opcję `New table`.
![Krok](../screenshots/1/new/42.jpg)

## 1.3.7. Wybierz i nazwij nową tabelę
Nazwij nową tabelę `green202301` zgodnie z [podaną konwencją nazw](../exercise-0-setup/naming-convention.md), a potem kliknij `Load`.
![Krok](../screenshots/1/new/43.jpg)

## 1.3.8. Powiadomienie o ładowaniu
Zwróć uwagę na powiadomienie, że plik jest właśnie ładowany do tabeli.
![Krok](../screenshots/1/new/44.jpg)

## 1.3.9. Odśwież Lakehouse
Gdy ładowanie się skończy, odśwież Lakehouse: kliknij trzy kropki obok tabeli i wybierz `Refresh`. Nowa tabela powinna być teraz widoczna.
![Krok](../screenshots/1/new/45.jpg)

## 1.3.10. Utwórz Notebook
Aby utworzyć Notebook, kliknij opcję `New notebook` w menu `Open Notebook`. Zwróć uwagę, że Fabric wygenerował dla ciebie nowy Notebook z jedną komórką.
![Krok](../screenshots/1/new/46.jpg)

![Krok](../screenshots/1/new/47.jpg)

## 1.3.11. Sprawdź konfigurację Notebooka
Jeśli wszystko poszło poprawnie, w sekcji `Tables` zobaczysz dwie tabele, a w `Files` jeden folder. Sprawdź, czy wszystko się zgadza.
![Krok](../screenshots/1/new/48.jpg)

## 1.3.12. Wykonaj zapytanie
Utwórz zapytanie: przeciągnij nazwę tabeli i upuść ją w treści Notebooka.
![Krok](../screenshots/1/new/49.jpg)

## 1.3.13. Wykonaj zapytanie
Aby uruchomić zapytanie, kliknij przycisk odtwarzania po lewej stronie komórki. Zapytanie powinno zakończyć się w kilka sekund. Widać tu płynną integrację i łatwość obsługi Fabric jako prawdziwego rozwiązania SaaS. Przejrzyj wyniki w tabeli.

> [!IMPORTANT]
> Fabric Spark stosuje throttling i kolejkowanie oparte na liczbie rdzeni. Użytkownicy mogą przesyłać Spark job w ramach zakupionego SKU Fabric capacity. Kolejka działa w prostym modelu FIFO: sprawdza dostępne sloty i automatycznie ponawia Spark job, gdy capacity się zwolni. Jeśli prześlesz Spark job z Notebooka lub Lakehouse, np. Load to Table, gdy capacity jest maksymalnie obciążone, bo równolegle działające Spark job zajmują wszystkie Spark Vcores dostępne w zakupionym SKU Fabric capacity, zobaczysz komunikat **HTTP Response code 430: Unable to submit this request because all the available capacity is currently being used. The suggested solutions are to cancel a currently running job, increase the available capacity, or try again later.**.

> [!NOTE]
> Stan na wrzesień 2026 roku: aktualny komunikat brzmi `[TooManyRequestsForCapacity] HTTP Response code 430: This Spark job can't be run because you have hit a Spark compute or API rate limit.` Kolejka obejmuje tylko joby uruchamiane z Pipeline, z harmonogramu i ze Spark Job Definition. Interaktywne joby z Notebooka nie trafiają do kolejki, tylko od razu dostają błąd 430. Na Fabric trial capacity kolejkowanie nie działa wcale.


![Krok](../screenshots/1/new/50.jpg)

> [!WARNING]
> Gdy w Fabric podłączasz Lakehouse do Notebooka, metadane zapisują się w pliku Notebooka. Jeśli udostępnisz ten Notebook przez eksport i pobranie, odbiorca zobaczy ostrzeżenie, że Notebook był połączony z innym Lakehouse. Aby tego uniknąć, przed udostępnieniem usuń z Notebooka podłączone elementy. Jeśli dostaniesz Notebook z podłączonymi elementami, przypisz go do nowego Lakehouse, aby uniknąć konfliktów. 
> W CI/CD pamiętaj, że artefakty zawierają metadane, które pokazują ich połączenia.
> 
> ![Krok](../screenshots/1/warning.png) 

## 1.3.14. Potwierdź domyślny Lakehouse
Upewnij się, że Lakehouse `bronzerawdata` jest ustawiony jako domyślny dla Notebooka. Jeśli tak, zadanie jest ukończone. Gratulacje.
![Krok](../screenshots/1/new/51.jpg)


## Zadanie 1.4 Zarządzanie Spark session
Naucz się zarządzać Spark session w swoim workspace i je zatrzymywać, aby efektywnie korzystać z zasobów i kontrolować koszty.

Domyślny czas wygaśnięcia Spark session dla Starter pool i Spark pool to 20 minut. Spark pool zostaje zwolniony, jeśli po wygaśnięciu Spark session nikt go nie używa przez 2 minuty.

**Działaj dopiero <ins>po</ins> przejściu przez poniższe zrzuty ekranu i opisy.**

### Kroki demo, czas wygaśnięcia Spark session:

1.  Na zrzucie ekranu pokazujemy (tylko na zrzutach ekranu, nie ma demo na żywo ani GIF-a), jak załadować dane Parquet do Delta table za pomocą funkcji 'Load to Table'.
   
     ![Ładowanie danych](../screenshots/extra/new/mh1.jpg)
2. Tabela została utworzona, co potwierdza powiadomienie na ekranie. Przechodzimy do Monitoring hub, aby pokazać bieżącą aktywność.

     ![Monitoring Hub](../screenshots/extra/new/mh2.jpg)


2. W Monitoring hub widzimy, że aktywność nadal trwa. Wyjaśnienie, dlaczego tak jest, znajdziesz na zrzucie ekranu. Kliknij trzy kropki "..." i wybierz "View details".

     ![View Details](../screenshots/extra/new/mh3.jpg)

3. W widoku szczegółów zwróć uwagę na kluczowe informacje, zwłaszcza na treści wyróżnione na zrzucie ekranu.
     ![Szczegóły Spark session](../screenshots/extra/new/mh4.jpg)

4. Po przejrzeniu wszystkich oznaczonych elementów widać, że Spark session trzeba anulować. Pokażemy, jak to zrobić. Ponownie kliknij trzy kropki, a potem 'cancel'.

     ![Anulowanie Spark session](../screenshots/extra/new/mh5.jpg)
   
    Potwierdź tę akcję, wybierając "Yes, stop".

    ![Potwierdzenie zatrzymania](../screenshots/extra/new/mh6.jpg)

5. Sprawdź na ekranie, czy udało się zatrzymać Spark session.

     ![Spark session zatrzymana](../screenshots/extra/new/mh7.jpg)

**Omów z prowadzącymi wpływ Fabric capacity i regionów Fabric, [limity współbieżności](https://learn.microsoft.com/en-us/fabric/data-engineering/spark-job-concurrency-and-queueing), mechanizm inteligentnego poolingu oraz różnice między warsztatem a rzeczywistymi scenariuszami.** 


> [!IMPORTANT]
> Gdy skończysz, przejdź do [następnego ćwiczenia (Ćwiczenie 2)](./../exercise-2/exercise-2.md). Jeśli przed kolejnym ćwiczeniem zostanie ci czas, zajmij się [krokami dodatkowymi](../exercise-extra/extra.md).
