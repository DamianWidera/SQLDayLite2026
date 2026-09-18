# Konwencja nazw

> [!TIP]
> Zapoznaj się z konwencją nazw, bo od niej zależy, czy wszystkie ćwiczenia przebiegną bez problemów. **Nie musisz nic robić, wystarczy, że przeczytasz konwencję nazw i przyjmiesz ją do wiadomości**.

## Nazwa workspace
Nadaj nazwę: `urban-innovation-deNNN`, gdzie NNN to przydzielony ci numer. Na przykład `urban-innovation-de001` (workspace Estery).

## Nazwy tabel
* Zadanie 1.1.18 - `green_202201_202301`
* Zadanie 1.3.7 - `green202301`


              "green_202201_202301",
                    "green_from_202302"

## Warstwa bronze (zarządzanie danymi surowymi)
Nazwa Lakehouse: `bronzerawdata`

To warstwa podstawowa. Trafiają do niej dane surowe prosto z różnych źródeł: dane o przejazdach żółtych i zielonych taksówek, dane o przejazdach FHV, a potencjalnie także inne zbiory danych o mobilności miejskiej. Dane są przechowywane w oryginalnej, niezmienionej postaci. Na tym warsztacie ładujesz do tej warstwy surowe dane TLC Trip Record Data. Wszystkie dane surowe pozostają niezmienne i możliwe do prześledzenia na potrzeby lineage.

## Warstwa silver (zarządzanie danymi oczyszczonymi)
Nazwa Lakehouse: `silvercleansed`

W tej warstwie pośredniej dane są czyszczone, standaryzowane i wzbogacane. Usuwa to niespójności i przygotowuje dane do bardziej szczegółowej analizy. Obejmuje to rozwiązywanie problemów z jakością danych, ujednolicanie formatów oraz wzbogacanie danych o taksówkach i FHV o dodatkowy kontekst, na przykład warunki pogodowe lub dane o ruchu drogowym. Celem jest wiarygodny zbiór danych zoptymalizowany pod kątem zapytań, który usprawnia analizę i raportowanie.

## Warstwa gold (zarządzanie danymi gotowymi do raportowania)
Nazwa Lakehouse: `goldcurated`

To najwyższa warstwa Lakehouse. Dane są tu dalej transformowane, modelowane i podsumowywane, aby wspierać zaawansowaną analitykę i business intelligence. Ta warstwa ma dostarczać wnioski, na podstawie których można działać, i wspierać decyzje na wysokim szczeblu. Może to oznaczać agregowanie danych w użyteczne metryki, opracowanie KPI efektywności transportu miejskiego albo budowanie modeli uczenia maszynowego, które na podstawie wzorców historycznych przewidują przyszłe trendy.
