# Źródła danych / Data Sources

## 1. UCI — Individual Household Electric Power Consumption (REKOMENDOWANE)

- **URL:** https://archive.ics.uci.edu/dataset/235/individual+household+electric+power+consumption
- **Kaggle mirror:** https://www.kaggle.com/datasets/uciml/electric-power-consumption-data-set
- **Opis:** Pomiary zużycia energii elektrycznej w jednym gospodarstwie domowym z minutowym interwałem próbkowania, przez okres ~4 lat (grudzień 2006 – listopad 2010).
- **Rozmiar:** 2 075 259 pomiarów, ~133 MB
- **Format:** TXT/CSV, separator: `;`
- **Kolumny:**
  - `Date` — data (dd/mm/yyyy)
  - `Time` — czas (hh:mm:ss)
  - `Global_active_power` — minutowa średnia mocy czynnej (kW)
  - `Global_reactive_power` — minutowa średnia mocy biernej (kW)
  - `Voltage` — minutowe średnie napięcie (V)
  - `Global_intensity` — minutowe średnie natężenie prądu (A)
  - `Sub_metering_1` — kuchnia (Wh)
  - `Sub_metering_2` — pralnia (Wh)
  - `Sub_metering_3` — bojler + klimatyzacja (Wh)
- **Brakujące dane:** ~1.25% wierszy
- **Licencja:** CC BY 4.0
- **Dlaczego pasuje:** Dane czasowe (time series), format timestamp + zużycie energii, idealne do analizy dziennej/tygodniowej/miesięcznej, wykrywania anomalii i prognozy.

---

## 2. Kaggle — Smart Meters in London

- **URL:** https://www.kaggle.com/datasets/jeanmidev/smart-meters-in-london
- **Opis:** Dane z inteligentnych liczników energii z 5 567 gospodarstw domowych w Londynie (listopad 2011 – luty 2014). Zawiera dane półgodzinne i dzienne + dane pogodowe.
- **Rozmiar:** ~10 GB (pełny zestaw)
- **Pliki:**
  - `halfhourly_dataset.zip` — pomiary co 30 minut
  - `daily_dataset.zip` — agregacje dzienne (min, max, mean, median, sum, std)
  - `weather_daily_darksky.csv` — dane pogodowe dzienne
  - `weather_hourly_darksky.csv` — dane pogodowe godzinne
  - `informations_households.csv` — informacje o gospodarstwach (grupa ACORN, taryfa)
- **Licencja:** Open Database License (ODbL)
- **Dlaczego pasuje:** Dane smart meter, wielu użytkowników (profile zużycia), dane pogodowe umożliwiają korelację temperatura ↔ zużycie.

---

## 3. Kaggle — Household Electricity Consumption (240 000 records)

- **URL:** https://www.kaggle.com/datasets/thedevastator/240000-household-electricity-consumption-records
- **Opis:** 240 000 rekordów zużycia energii elektrycznej w gospodarstwach domowych.
- **Rozmiar:** ~3 MB (lekki dataset, łatwy do przetwarzania)
- **Licencja:** Kaggle — sprawdź stronę datasetu
- **Dlaczego pasuje:** Mniejszy zestaw idealny do szybkiego prototypowania i testowania aplikacji.

---

## Rekomendacja

Dla tego projektu najlepiej użyć **datasetu nr 1 (UCI Household Electric Power Consumption)**, ponieważ:
- Ma format timestamp + zużycie energii (zgodnie z wymaganiami projektu)
- Dane minutowe umożliwiają agregację do dzień/tydzień/miesiąc
- Dane z ~4 lat pozwalają na analizę sezonowości
- Sub-metering pozwala analizować zużycie wg urządzeń
- CC BY 4.0 — wolna licencja
