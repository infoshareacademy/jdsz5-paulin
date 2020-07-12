### 1) Założenia i cel projektu

Celem jest opracowanie aplikacji, który ma szerokie zastosowanie dla przewidywania cen sprzedaży mieszkań. Przy określeniu kilku parametrów np. liczby pokoi, piętra czy wielkości miejscowości jesteśmy w stanie określić cenę sprzedaży danego lokalu mieszkalnego.

Model, który opracowaliśmy bazuje na rzeczywistej bazie nieruchomości z całej Polski, z kilku popularnych stron internetowych dotyczących tej tematyki. Zgromadzone dane dotyczą danych z rynku wtórnego i pierwotnego.

Jako metryki sukcesu modelu zastosowano MSE i statystykę R2.

### 2) Analiza danych

Zmienne zawarte w bazie są typu liczbowego i kategorycznego. Na potrzeby pracy nad modelem zostały poddane funkcji get.dummies w celu przekształceniu ich na liczbowe.
Podstawowymy zmiennymi objaśniającymi są:

współrzędne geograficzne,
powierzchnia,
liczba pokoi,
piętro,
rok budowy.
Zmienną objaśnianą jest cena.

### 3, 4) Data Cleaning i Feature Engineering
W pierwszym etapie pracy nad bazą przeprowadzono zaawansowany data cleaning polegający na uzupełnieniu części brakujących danych metodą najbliższych sąsiadów, usunięciu danych NaN, usystematyzowaniu nazw poszczególnych danych kategorycznych, w celu lepszej czytelności danych, zmiany typów danych oraz usunięciu outlajerów. Ostatecznie połączono, tak oczyszczoną bazę danych z bazą dotyczącą populacji, by określić przedziały populacji w poszczególnych miejscowościach (duże miasto, średniej, małe). Dokonano tego, ażeby otrzymać bardziej precyzyjną predykcję ceny. Narzędzie, które poslużyło do dostania się do bazy danych populacji był scrapping, dla bardziej komfortowego użytkowania wytrenowanego modelu na rzeczywistych danych bez względu na miejsce użytkownika.

### 5) Modelowanie

Jako modele zastosowano regresję liniową wieloraką, drzewa i lasy decyzyjne, KNN, SVM oraz XG boost. W każdym z zastosowanych modeli dobrano najbardziej optymalne hiperparametry do określenia ceny lokalu mieszkalnego. Dodatkowo, zastosowano klasyfikację metodą KNN, w celu wyszukania zbliżonych ogłoszeń nieruchomości ze względu na ich atrybuty.
Na podstawie wymienionych modeli przeprowadzono badania i przedstawiono wyniki poszczególnych metod.

### 6) Model ostateczny

Wynikiem pracy jest porównanie modeli i wybranie najbardziej skutecznego i satysfakcjonującego, na którym została przeprowadzona cross validation, w celu ocenienia jak wybrany model będzie się zachowywał w praktyce.