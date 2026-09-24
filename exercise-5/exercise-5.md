# Ćwiczenie 5 - Nowości w Fabric i Data Wrangler

![Architektura warsztatu, podświetlony fragment: Ćwiczenie 5](../assets/architecture/architektura-cw5.png)

> [!NOTE]
> Czas: 60 minut
>
> Zrzuty ekranu to orientacyjna pomoc, nie wzorzec jeden do jednego. Interfejs Fabric zmienia się co kilka tygodni, więc przyciski mogą być w innym miejscu, nazwy lekko inne, a część zrzutów pochodzi z wcześniejszych edycji warsztatu. Kieruj się tekstem kroku i nazwami w `kodzie`.
> 
> [Powrót do agendy](./../README.md#agenda) | [Wstecz: Ćwiczenie 4](./../exercise-4/exercise-4.md) | [Dalej: ćwiczenia dodatkowe](../exercise-extra/extra.md)
> #### Lista zadań:
> *  [Bądź na bieżąco i dodaj do zakładek najważniejsze strony](#bądź-na-bieżąco-i-dodaj-do-zakładek-najważniejsze-strony)
> *  [Runtime w Fabric i Python User-defined Table Functions (UDTFs)](#runtime-w-fabric-i-python-user-defined-table-functions-udtfs)
> *  [Managed Private Endpoints](#managed-private-endpoints)
> *  [Autotune Query Tuning](#autotune-query-tuning)
> *  [Spark czy Pandas](#spark-czy-pandas)
> *  [Zaprzyjaźnij się z Data Wrangler](#zaprzyjaźnij-się-z-data-wrangler)
> *  [VSCode (WEB)](#vscode-web)


# Bądź na bieżąco i dodaj do zakładek najważniejsze strony
Poznaj najnowsze funkcje Fabric.
* **Comiesięczne podsumowania**: Nie przegap nowości. Wejdź na [Fabric Monthly Updates](https://blog.fabric.microsoft.com/en-us/blog/category/monthly-update) i nadrób zaległości z ostatnich trzech miesięcy. Znajdziesz tam nowe funkcje i usprawnienia wdrażane co tydzień, zebrane w jednym miejscu. Dodaj tę stronę do zakładek, żeby twoja wiedza była zawsze aktualna.
* **Najnowsze ogłoszenia**: Śledź najświeższe wiadomości na [Fabric's Blog](https://blog.fabric.microsoft.com/en-US/blog). Znajdziesz tam szczegółowe omówienia dużych zmian, takich jak funkcje Managed Private Endpoints. To bogate źródło wiedzy i ogłoszeń, którego nie warto pomijać.
* **Przypnij wizualizacje**: Doceń twórczą pracę wewnętrznego zespołu Microsoft na stronie [Fabric Notes](https://microsoft.github.io/fabricnotes/). Zespół świetnie zwizualizował często używane pojęcia Fabric i w pełni zasłużył na uznanie. Przypnij tę stronę, żeby mieć pod ręką źródło inspiracji i nowych pomysłów.
* **Zgłaszaj swoje pomysły**: W Fabric twój głos się liczy. Jeśli chcesz, żebyśmy coś poprawili albo dodali, opisz swój pomysł na [Fabric Ideas](https://ideas.fabric.microsoft.com/). Przypisz propozycję do konkretnego obciążenia, żeby była jasna. Słuchamy uważnie i jesteśmy gotowi dopasować plany półroczne do twoich potrzeb. Dzięki temu przestajesz tylko reagować na zmiany i zaczynasz wpływać na kierunek rozwoju Fabric. Dobrym przykładem są eksperymentalne wersje runtime, które wprowadziliśmy po opiniach użytkowników. Na co więc czekać? Podziel się swoimi uwagami i współtwórz rozwój Fabric.

> [!IMPORTANT]
> To także dobra okazja, żeby przypomnieć: zawsze używaj najnowszej wersji runtime ze statusem GA. Eksperymentuj z wersją Preview, ale w obciążeniach produkcyjnych używaj wersji GA. Cykl życia wersji runtime znajdziesz w [dokumentacji](https://learn.microsoft.com/fabric/data-engineering/lifecycle). Spark wydaje nowe wersje co sześć do dziewięciu miesięcy, więc przestarzałe wersje runtime są regularnie wycofywane. Przenieś obciążenia produkcyjne przed datą końca wsparcia. Po tej dacie wersja runtime znika z ustawień workspace i z Environment, a Spark job, które jej używają, przestają działać.

---

# Runtime w Fabric i Python User-defined Table Functions (UDTFs)

## Jak działają wersje runtime Apache Spark w Fabric
Fabric Runtime to platforma zintegrowana z Azure i zbudowana na Apache Spark. Umożliwia pracę z zakresu data engineering i data science na dużą skalę. Łączy najważniejsze komponenty własnościowe i open source, dzięki czemu daje rozbudowane środowisko przetwarzania danych. Dla uproszczenia nazywamy ją tutaj Fabric Runtime.

Najważniejsze komponenty Fabric Runtime:

- **Apache Spark**: wydajny system obliczeń rozproszonych, pełna platforma do przetwarzania danych na dużą skalę.
- **Delta Lake**: dodaje do Apache Spark w Fabric Runtime transakcje ACID i mechanizmy niezawodności, co poprawia integralność danych.
- **Pakiety języków programowania**: Java/Scala, Python i R są obsługiwane od razu, bez dodatkowej konfiguracji, więc możesz pracować w wybranym języku.
- Całość opiera się na **solidnych fundamentach open source**, co zapewnia szeroką zgodność i wydajność.

W tabeli poniżej znajdziesz szczegółowe porównanie wersji Apache Spark i obsługiwanych konfiguracji w poszczególnych wersjach runtime:

| Składnik | Runtime 1.3 | Runtime 2.0 |
|---|---|---|
| **Etap cyklu życia** | koniec wsparcia ogłoszony na 30 września 2026 roku, potem LTS do marca 2027 roku | GA |
| **Apache Spark** | 3.5.5 | 4.1 |
| **System operacyjny** | Mariner 2.0 | Mariner 3.0 |
| **Java** | 11 | 21 |
| **Scala** | 2.12.17 | 2.13.16 |
| **Python** | 3.11 | 3.13 |
| **Delta Lake** | 3.2 | 4.2 |

Runtime 1.1 i Runtime 1.2 nie są już obsługiwane. Runtime 1.2 stracił wsparcie 31 marca 2026 roku.

> [!TIP] 
> Najnowsza wersja GA to [Runtime 2.0](https://learn.microsoft.com/fabric/data-engineering/runtime-2-0). Microsoft zapowiedział, że pod koniec września 2026 roku stanie się ona domyślna w nowych workspace. Na tym warsztacie pracujemy na [Runtime 1.3](https://learn.microsoft.com/fabric/data-engineering/runtime-1-3), bo na nim przygotowaliśmy Notebooki.

Celem tego zadania jest użycie Python User-defined Table Functions (UDTFs), które pojawiły się w Spark 3.5. UDTFs świetnie sprawdzają się w transformacji danych, zwłaszcza gdy jeden wiersz trzeba rozwinąć w wiele wierszy. Więcej o Python UDTFs przeczytasz [tutaj](https://spark.apache.org/docs/latest/api/python/user_guide/sql/python_udtf.html).

## 1. Ustaw Runtime 1.3

Upewnij się, że używasz Runtime w wersji 1.3. Tę wersję sprawdza [krok 13 konfiguracji startowej](../exercise-0-setup/start.md#13-sprawdź-spark-pool-i-runtime). Teraz tylko to sprawdź:

1. Przejdź do 'Workspace settings' w swoim workspace w Fabric.
2. Otwórz kartę 'Data Engineering/Science' i wybierz 'Spark Settings'.
3. W sekcji 'Environment' wybierz 'Runtime Versions', zaznacz '1.3 (Spark 3.5, Delta 3.2)' i zatwierdź zmiany. W ten sposób ustawisz Runtime 1.3 jako domyślny.

![Kroki](../screenshots/5/new/1.jpg)

## 2. Utwórz nowy Notebook
Utwórz i skonfiguruj nowy Notebook:

1. Rozpocznij nową sesję Notebooka w swoim workspace.
2. W panelu `Explorer` kliknij `Add data items` i podepnij Lakehouse `bronzerawdata`. Bez tego kroku Spark nie rozpozna nazwy `bronzerawdata.<tabela>` w zadaniu 3. Możesz też użyć zaimportowanego `notebook-2`, który ma już podpięty `bronzerawdata`.
3. Sprawdź wersję Spark: uruchom `sc.version` w Notebooku i potwierdź, że działa Spark 3.5.

## 3. Poznaj UDTFs w Fabric
Sprawdź, co UDTFs potrafią w złożonych transformacjach danych:
1. Weź pod uwagę rzeczywisty scenariusz opłat za taksówkę. Na końcowy koszt składają się, poza opłatą podstawową, także podatki, napiwki i dodatkowe opłaty.
2. Użyj UDTFs, żeby obliczyć i doliczyć te koszty w jednej operacji. Ułatwi to analizę danych i wyciąganie wniosków z twoich zbiorów danych.
3. Zastosuj podany przykładowy kod do wybranej tabeli z danych w Lakehouse bronze albo silver. Skup się na kolumnie 'fare_amount'.
4. Wykonaj transformacje i sprawdź wynik na podzbiorze danych. Jako przykład zastosuj rabat 5%.

![Krok](../screenshots/5/new/2.jpg)

<details>

<summary>Kliknij <ins>tutaj</ins>, żeby rozwinąć szczegóły i sprawdzić odpowiedź.</summary>

```python
from pyspark.sql.functions import udtf
from pyspark.sql.types import Row

# Python User-defined Table Functions (UDTF) do obliczania wszystkich drobnych i ukrytych kosztów jazdy taksówką (dla każdego kursu)
@udtf(returnType="fare_amount: float, tip:float, sales_tax:float, climate_tax: float, final_total: float")
class TaxiFareUDTF:
    def eval(self, row: Row, discount_percentage: float):
        return_row = Row(
            # Oblicz napiwek od kwoty netto, wymagany napiwek to 20%, witamy w stanie WA
            tip=row["fare_amount"] * 0.20,
            # Oblicz podatki
            sales_tax=row["fare_amount"] * 0.08, # 8% podatku od sprzedaży
            climate_tax=row["fare_amount"] * 0.03, # 3% podatku klimatycznego
            # Oblicz końcową kwotę łączną
            final_total=row["fare_amount"] + (row["fare_amount"] * 0.20) + (row["fare_amount"] * 0.08) + (row["fare_amount"] * 0.03) - (discount_percentage/100 * row["fare_amount"])
            )
        yield row["fare_amount"], return_row["tip"], return_row["sales_tax"], return_row["climate_tax"], return_row["final_total"]


# Python UDTFs można też zarejestrować i używać ich w zapytaniach SQL.
spark.udtf.register("calculate_individual_costs", TaxiFareUDTF)

# Python UDTFs mogą też przyjmować TABLE jako argument wejściowy, także razem ze skalarnymi argumentami wejściowymi. Domyślnie dozwolony jest tylko jeden argument wejściowy TABLE, głównie ze względu na wydajność. Jeśli potrzebujesz więcej niż jednego argumentu wejściowego TABLE, ustaw konfigurację spark.sql.tvf.allowMultipleTableArguments.enabled na true.
spark.sql("SELECT * FROM calculate_individual_costs(TABLE(SELECT fare_amount FROM bronzerawdata.green_202201_202301 LIMIT 20), 5)").show()
```

</details>

Każda nowa wersja Runtime rozszerza API i dodaje nowe metody oraz transformacje, dzięki czemu przetwarzanie danych jest wydajniejsze i daje więcej możliwości. Najnowsze wersje runtime ze statusem GA są też zwykle szybsze od poprzednich, bo stale ulepszają je społeczność open source i zespoły produktowe Microsoft.

Teraz wykorzystaj tę wiedzę i oblicz pełne koszty w szerszym zakresie niż w przykładzie. 

---

# Managed Private Endpoints

Managed virtual networks to sieci wirtualne, które Microsoft Fabric tworzy i którymi zarządza osobno dla każdego workspace w Fabric. Zapewniają izolację sieciową obciążeń Fabric Spark: klastry obliczeniowe są wdrażane w dedykowanej sieci i nie należą już do współdzielonej sieci wirtualnej. Managed virtual networks umożliwiają też korzystanie z funkcji bezpieczeństwa sieci, takich jak Managed Private Endpoints i Private Link, dla elementów Data Engineering i Data Science w Microsoft Fabric, które używają Apache Spark.

> [!IMPORTANT]
> Managed Private Endpoints działają na każdej Fabric capacity z SKU F oraz na Fabric trial capacity. Nie działają na capacity z SKU P.

![MPE-OVERVIEW](https://learn.microsoft.com/en-us/fabric/security/media/security-managed-vnets-fabric-overview/managed-vnets-overview.gif)

Managed Private Endpoints dodaje się do workspace. Administratorzy workspace mogą tworzyć i usuwać połączenia Managed Private Endpoints w ustawieniach workspace w Fabric.

![demo-mpe](https://learn.microsoft.com/en-us/fabric/security/media/security-managed-vnets-fabric-overview/creating-private-endpoint-animation.gif)

Managed Private Endpoints to połączenia, które administratorzy workspace tworzą, żeby uzyskać dostęp do źródeł danych ukrytych za zaporą albo niedostępnych z publicznego internetu. Dzięki nim obciążenia Fabric Spark bezpiecznie korzystają ze źródeł danych bez wystawiania ich do sieci publicznej i bez skomplikowanej konfiguracji sieci. Private endpoints pozwalają bezpiecznie połączyć się z tymi źródłami danych i odczytać z nich dane za pomocą takich elementów jak Notebook i Spark Job Definition.

Microsoft Fabric tworzy Managed Private Endpoints i zarządza nimi na podstawie danych podanych przez administratora workspace. Administrator konfiguruje je w ustawieniach workspace: podaje identyfikator zasobu źródła danych, wskazuje docelowy zasób podrzędny i uzasadnia żądanie private endpoint. Managed Private Endpoints obsługują różne źródła danych, m.in. Azure Storage i Azure SQL Database.

Obejrzyj GIF, który pokazuje pełne demo tworzenia Managed Private Endpoint.

> [!WARNING]
> To jest tylko demo. Nie twórz Managed Private Endpoint w swoim workspace warsztatowym. Gdy workspace dostaje managed virtual network, Fabric wyłącza w nim Starter pool. Każda Spark session startuje wtedy od 3 do 5 minut, do końca warsztatu.

![mpe](../screenshots/5/managed_private_endpoint_velocity.gif)


> [!NOTE]
> MPE trzeba zatwierdzić po stronie zasobu docelowego. 

Weźmy jako przykład SQL Server. Użytkownik przechodzi do Azure portal i wyszukuje zasób "SQL Server".

1. Na stronie zasobu wybierz **Networking** w menu nawigacji, a następnie kartę **Private Access**.

   ![Zrzut ekranu z kartą Private access na stronie Networking zasobu w Azure portal](https://learn.microsoft.com/en-us/fabric/security/media/security-managed-private-endpoints-create/networking-private-access-tab.png)

1. Administratorzy źródła danych powinni widzieć aktywne połączenia private endpoint i nowe żądania połączenia.

    ![Zrzut ekranu z oczekującymi żądaniami na karcie Private access](https://learn.microsoft.com/en-us/fabric/security/media/security-managed-private-endpoints-create/new-connection-requests.png)

1. Administratorzy mogą wybrać *Approve* albo *Reject* i podać uzasadnienie biznesowe.

    ![Zrzut ekranu z formularzem zatwierdzania.](https://learn.microsoft.com/en-us/fabric/security/media/security-managed-private-endpoints-create/approve-reject-request.png)

1. Gdy administrator źródła danych zatwierdzi albo odrzuci żądanie, status zaktualizuje się na stronie ustawień workspace w Fabric po jej odświeżeniu.

    ![Zrzut ekranu z Managed Private Endpoint w stanie approved.](https://learn.microsoft.com/en-us/fabric/security/media/security-managed-private-endpoints-create/endpoint-request-approved-state.png)

1. Gdy status zmieni się na *approved*, możesz używać tego private endpoint w Notebooku albo Spark Job Definition, żeby z workspace w Fabric sięgać do danych zapisanych w źródle danych.

Kliknij [tutaj](https://learn.microsoft.com/en-us/fabric/security/security-managed-private-endpoints-create#supported-data-sources), żeby zobaczyć listę obsługiwanych źródeł danych.


---

# Autotune Query Tuning
Gdy mówimy o wersjach runtime Spark, zawsze dochodzimy do wydajności, czyli tematu ważnego dla nas wszystkich. Dlatego opracowaliśmy Autotune. Ta funkcja optymalizuje ustawienia Spark dla twoich Spark job, żeby działały wydajniej i skuteczniej.

> [!WARNING]
> Stan na wrzesień 2026 roku: Autotune działa tylko z Runtime 1.2, a ta wersja straciła wsparcie 31 marca 2026 roku. W Runtime 1.3 i 2.0 nie da się go włączyć. Autotune nie działa też z High concurrency mode ani z private endpoints. Traktuj tę sekcję jako opis mechanizmu, a nie ćwiczenie do wykonania.

Autotune włączało się w konfiguracji Spark w Environment, właściwością Spark 'spark.ms.autotune.enabled = true'.

* [Obejrzyj ekskluzywne demo](https://1drv.ms/v/s!ApCaji7rcQaQ3rNv8g7pBnLdrwQBfQ?e=R7GiEq)

* Więcej informacji o Autotune znajdziesz w dokumentacji: [Autotune w Fabric Data Engineering](https://learn.microsoft.com/en-us/fabric/data-engineering/autotune?tabs=sparksql).

> [!TIP]
> Autotune query tuning analizuje pojedyncze zapytania i dla każdego z nich buduje osobny model ML. Skupia się na:
> - zapytaniach powtarzalnych
> - zapytaniach długotrwałych (wykonywanych dłużej niż 15 sekund)
> - zapytaniach Spark SQL (z wyjątkiem pisanych w RDD API, które są bardzo rzadkie)
>
> Ta funkcja działa z Notebook, Spark Job Definition i Pipeline.

---

# Spark czy Pandas
W tym zadaniu twoją misją jest przeprowadzić nowych członków zespołu przez labirynt przetwarzania big data. Pokaż im przede wszystkim, kiedy przy dużych zbiorach danych wybrać Apache Spark zamiast Pandas. Ta rada jest kluczowa w ekosystemie Fabric i w całym świecie big data.

## Jak działa Pandas
Pandas wyróżnia się prostotą i intuicyjną konstrukcją, dlatego lubią go inżynierzy danych, badacze danych i analitycy. Ma jednak jedno główne ograniczenie: nie potrafi natywnie korzystać z architektur i obliczeń równoległych. Pandas wykonuje obliczenia w pamięci jednego węzła. To ogranicza skalowalność i wydajność przy ogromnych zbiorach danych, typowych dla big data.

## Przejście na Spark i jego podstawowe pojęcia
Apache Spark pokonuje te ograniczenia dzięki obliczeniom rozproszonym. Najważniejsze różnice:
- **Spark DataFrames**: są rozproszone w klastrze, więc dane przetwarzasz równolegle, daleko poza możliwościami jednej maszyny.
- **Lazy Evaluation**: Spark stosuje lazy evaluation dla DataFrame. Buduje Directed Acyclic Graph (DAG) transformacji, optymalizuje go i wykonuje dopiero wtedy, gdy potrzebna jest akcja. To poprawia ogólną wydajność wykonania.
- **Zaawansowane optymalizacje**: Adaptive Query Execution (AQE) automatycznie optymalizuje plany zapytań, a Dynamic Partition Pruning (DPP) robi to samo z podziałem danych na partition. Pandas tego nie potrafi.

## Ogólna zasada
- Używaj Pandas do zbiorów danych, które swobodnie mieszczą się w pamięci jednej maszyny, i wtedy, gdy przetwarzanie nie wymaga intensywnej równoległości.
- Wybierz Spark, gdy pracujesz z ogromnymi zbiorami danych, które przekraczają możliwości jednej maszyny, albo gdy przetwarzanie wyraźnie zyskuje na równoległości. Zrób tak nawet wtedy, gdy dobrze znasz Pandas, bo Spark daje skalowalność i optymalizacje.

## Koalas łączy oba światy
Koalas, wprowadzony w Spark 3.2, łączy prostotę API Pandas z mocą obliczeń rozproszonych Spark. Wystarczy zaimportować API `pandas` przez PySpark:

```python
from pyspark import pandas as pd
```

Dzięki tej integracji możesz stosować znane operacje w stylu Pandas i jednocześnie korzystać z rozproszonej architektury Spark. Masz to, co najlepsze z obu światów.

## Praktyczne zastosowanie w Fabric:
W Fabric dane ładuje się inaczej w Pandas, a inaczej w Spark. Poniżej znajdziesz przykład, który pokazuje, jak załadować plik CSV w obu frameworkach. To porównanie pokazuje różnice w składni i podpowiada, kiedy wybrać który framework, zależnie od rozmiaru zbioru danych i potrzeb obliczeniowych.

Sprawdź [Jak odczytywać i zapisywać dane za pomocą Pandas w Microsoft Fabric](https://learn.microsoft.com/en-us/fabric/data-science/read-write-pandas).

---

# Zaprzyjaźnij się z Data Wrangler
Poznaj wydajną analizę danych z Data Wrangler w Fabric. To zadanie pomoże ci użyć Data Wrangler do skutecznej eksploracji i transformacji Pandas DataFrame. Data Wrangler łączy przyjazny interfejs w formie siatki z dynamicznymi narzędziami analizy danych, dzięki czemu eksploracyjna analiza danych jest intuicyjna i solidna.

Poznaj dokładnie funkcje Data Wrangler w Fabric, ze szczególnym naciskiem na Pandas DataFrame. Zadanie jest podzielone na konkretne kroki, które przeprowadzą cię przez eksplorację, wizualizację i transformację danych w tym narzędziu.


## Konfiguracja początkowa
Otwórz `notebook-2` (ma już podpięty Lakehouse) i uruchom komórkę, która utworzy Pandas DataFrame:

```python
import pandas as pd
wrangler_sample_df = pd.read_csv("https://aka.ms/wrangler/titanic.csv")
display(wrangler_sample_df)
```

Następnie na karcie `Home` wstążki Notebooka rozwiń `Data Wrangler` i wybierz `wrangler_sample_df`. Data Wrangler nie otworzy się, dopóki trwa wykonanie komórki, poczekaj na `Session ready`.

> [!TIP]
> Chcesz popracować na danych z warsztatu? Użyj małej próbki, nie całej tabeli: `df = spark.read.table("bronzerawdata.green_202201_202301").limit(20000).toPandas()`. Pandas liczy w pamięci jednego węzła.

![Krok](../screenshots/5/new/dw1.jpg)
![Krok](../screenshots/5/new/dw2.jpg)
![Krok](../screenshots/5/new/dw3.jpg)

## Eksploracyjna analiza danych

Przejrzyj zbiór danych w widoku siatki. Zwróć uwagę na rozkład danych, brakujące wartości i typy danych.
Wygeneruj dynamiczne statystyki podsumowujące, żeby szybko poznać średnią, medianę, dominantę, minimum i maksimum w kolumnach.
Użyj wbudowanych wizualizacji, żeby zrozumieć rozkłady danych, korelacje i wartości odstające. Wypróbuj różne typy wykresów i wybierz ten, który najlepiej pokazuje twoje dane.

![Krok](../screenshots/5/new/dw4.jpg)
![Krok](../screenshots/5/new/dw5.jpg)
![Krok](../screenshots/5/new/dw6.jpg)

## Operacje czyszczenia danych

Znajdź w zbiorze danych niespójności, brakujące wartości i wartości odstające.
Zastosuj typowe operacje czyszczenia danych dostępne w Data Wrangler, np. uzupełnianie brakujących wartości, filtrowanie wierszy albo poprawianie typów danych. Obserwuj, jak każda operacja na bieżąco aktualizuje widok danych.
Oceń, jak twoje transformacje wpłynęły na statystyki podsumowujące i wizualizacje, i upewnij się, że są zgodne z celami analizy.

## Generowanie kodu i ponowne użycie

Gdy stosujesz transformacje w Data Wrangler, obserwuj, jak automatycznie powstaje odpowiadający im kod w Pandas albo PySpark.
Zapisz wygenerowany kod w Notebooku jako funkcję do ponownego użycia. W ten sposób lepiej zrozumiesz transformacje danych i zbudujesz bibliotekę własnych funkcji do przyszłych analiz.

![Krok](../screenshots/5/new/dw7.jpg)

## Chcesz dowiedzieć się więcej? Zachęcamy do obejrzenia odcinka Fabric Espresso o Data Wrangler.
[![FabricEspresso](https://img.youtube.com/vi/-g6KveKQXu4/0.jpg)](https://www.youtube.com/watch?v=-g6KveKQXu4)


---

# VSCode (WEB)

Visual Studio Code for the Web to darmowy Microsoft Visual Studio Code, który nie wymaga instalacji i działa w całości w przeglądarce. Pozwala szybko i bezpiecznie przeglądać repozytoria kodu źródłowego i wprowadzać drobne zmiany w kodzie. 

## Otwórz Notebook (np. notebook-2) za pomocą rozszerzenia Fabric Data Engineering - Remote VS Code for the Web

Notebook otworzysz w VS Code for the Web przyciskiem **Open in VS Code(Web)** na stronie edycji Notebooka w portalu Fabric. Po kliknięciu przycisku otworzy się osobna karta przeglądarki z VS Code for the Web. Jeśli nie masz jeszcze rozszerzenia, zainstaluje się ono i aktywuje automatycznie, a Notebook zostanie otwarty.
![VSCODE](../screenshots/5/new/vs1.jpg)
![VSCODE](../screenshots/5/new/vs2.jpg)

## Zainstaluj rozszerzenie Jupyter
Żeby wybrać kernel Python, zainstaluj rozszerzenie Jupyter. Wykonaj kroki pokazane na zrzucie ekranu. Po instalacji rozszerzenia odśwież stronę.

![VSCODE](../screenshots/5/new/vs3.jpg)


## Uruchom Notebook w VS Code for the Web

Notebook uruchomisz w VS Code for the Web przyciskiem **Run** w edytorze Notebooka. Zanim uruchomisz Notebook, wybierz **Microsoft Fabric Runtime** jako kernel. Kernel wybierasz w prawym górnym rogu edytora Notebooka.

![VSCODE](../screenshots/5/new/vs4.jpg)
![VSCODE](../screenshots/5/new/vs5.jpg)
![VSCODE](../screenshots/5/new/vs6.jpg)


## Chcesz dowiedzieć się więcej? Zachęcamy do obejrzenia odcinka Fabric Espresso o VSCode.

[![FabricEspresso](https://img.youtube.com/vi/A9SjAyZ_JSc/0.jpg)](https://www.youtube.com/watch?v=A9SjAyZ_JSc)



---
> [!IMPORTANT]
> Po zakończeniu przejdź do [agendy](./../README.md#agenda). Jeśli przed kolejnym ćwiczeniem zostanie czas, wykonaj [dodatkowe kroki](../exercise-extra/extra.md).

---

> [!TIP]
> Kończysz na dziś? Wypełnij krótką [ankietę o warsztacie](https://forms.cloud.microsoft/e/hXHYaB8pDb). Kod QR znajdziesz na końcu [strony głównej](./../README.md#twoja-opinia).
