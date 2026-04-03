# Wymagania funkcjonalne / Functional Requirements

## Wczytywanie i zarządzanie danymi

**WF-01.** System umożliwia wczytanie danych z pliku CSV zawierającego kolumny z datą/czasem (timestamp) oraz wartościami zużycia energii (kWh).

**WF-02.** System waliduje poprawność formatu pliku CSV przy wczytywaniu — sprawdza obecność wymaganych kolumn, typy danych i raportuje błędy.

**WF-03.** System automatycznie wykrywa i obsługuje brakujące wartości w danych (NaN) — umożliwia ich usunięcie lub interpolację.

**WF-04.** System umożliwia filtrowanie danych po zakresie dat (od–do) wybranym przez użytkownika.

## Wizualizacja danych

**WF-05.** System wyświetla wykres zużycia energii w agregacji dziennej — prezentuje łączne/średnie zużycie dla każdego dnia.

**WF-06.** System wyświetla wykres zużycia energii w agregacji tygodniowej — prezentuje łączne/średnie zużycie dla każdego tygodnia.

**WF-07.** System wyświetla wykres zużycia energii w agregacji miesięcznej — prezentuje łączne/średnie zużycie dla każdego miesiąca.

**WF-08.** System umożliwia porównanie zużycia energii między wybranymi dniami tygodnia (np. poniedziałek vs. sobota) na jednym wykresie.

**WF-09.** System wyświetla wykres profilu dobowego zużycia (średnie zużycie wg godzin w ciągu doby) z podziałem na dzień roboczy i weekend.

## Statystyki i analiza

**WF-10.** System oblicza i wyświetla podstawowe statystyki zużycia energii: średnią, medianę, minimum, maksimum, odchylenie standardowe oraz sumę w wybranym okresie.

**WF-11.** System identyfikuje godziny szczytowego zużycia energii (peak hours) oraz godziny najniższego zużycia (off-peak) i prezentuje je użytkownikowi.

**WF-12.** System porównuje zużycie energii w wybranym okresie z analogicznym okresem wcześniejszym i wyświetla procentową zmianę.

## Wykrywanie anomalii

**WF-13.** System automatycznie wykrywa anomalie w zużyciu energii — punkty danych znacząco odbiegające od normy (np. >2 odchylenia standardowe od średniej kroczącej).

**WF-14.** System wizualizuje wykryte anomalie na wykresie, oznaczając je wyróżnionym kolorem lub markerem.

**WF-15.** System umożliwia konfigurację progu czułości wykrywania anomalii przez użytkownika (np. suwak z zakresem 1.5–3.0 odchylenia standardowego).

## Prognoza zużycia

**WF-16.** System generuje prognozę przyszłego zużycia energii na wybrany horyzont czasowy (np. 7, 14 lub 30 dni) z wykorzystaniem modelu regresji liniowej lub średniej kroczącej.

**WF-17.** System wyświetla wykres prognozowanego zużycia wraz z danymi historycznymi, umożliwiając wizualne porównanie.

## Interfejs użytkownika

**WF-18.** System udostępnia interfejs webowy (Streamlit) z panelem bocznym umożliwiającym wybór zakresu dat, typu agregacji i parametrów analizy.

**WF-19.** System umożliwia eksport wyników analizy (statystyki, wykryte anomalie) do pliku CSV.

**WF-20.** System wyświetla podgląd wczytanych danych w formie tabeli z możliwością sortowania i paginacji.
