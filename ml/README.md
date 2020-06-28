# Założenia i cel projektu
Model który opracowaliśmy bazuje na rzeczywistej bazie nieruchomości z całej Polski z kilku popularnych stron internetowych dotyczących tej tematyki w okresie ................. . Zgromadzone dane dotyczą danych z rynku wtórnego i pierwotnego.
Celem jest opracowanie modelu, który ma szerokie zastosowanie w celu przewidywania cen sprzedaży mieszkań. Przy określeniu kilku parametrów np. liczba pokoi, piętro czy wielkość miejscowości jesteśmy w stanie określić cenę sprzedaży danego lokalu mieszkalnego.
Jako metryki sukcesu modelu zastosowano MSE i statystykę R2.
W pierwszym etapie pracy nad bazą przeprowadzono zaawansowany data cleaning polegający na czyszczeniu danych NaN, usystematyzowaniu nazw poszczególnych danych kategorycznych w celu lepszej czytelności danych oraz usunięciu outlajerów. Ostatecznie połączono tak oczyszczoną bazę z bazą dotyczącą populacji, w celu określenia przedziałów populacji w poszczególnych miejscowościach.
Jako modele zastosowano regresję liniową, drzewa i lasy decyzyjne, KNN oraz XG boost.
W każdym z zastosowanych modeli dobrano najbardziej optymalne hiperparametry.
Na podstawie wymienionych modeli przeprowadzono badania i przedstawiono wyniki poszczególnych metod.
Wynikiem pracy jest porównanie modeli i wybranie najbardziej skutecznego i satysfakcjonującego.
