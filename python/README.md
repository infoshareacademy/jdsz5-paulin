Opis ogólny

Aplikacja pozwala na wizualizację danych dotyczących terroryzmu na świecie w latach 1970-2017 (w bazie danych brak roku 1993). Funkcjonalne widgety pozwalają na filtowanie zbioru danych w poszukiwaniu ilości zabitych w zalezności od interesującego użytkownika roku oraz rodzaju wykorzystanej broni w ataku. 

źródło danych:  
https://www.kaggle.com/START-UMD/gtd
w celu użytkowania aplikacji proszę ściągnąć bazę do tej samej lokalizacji co aplikacja.

Dane ogólne  

1. zestawienie wszystkich zmiennych wystepujących w datasecie, wraz z typem zmiennej oraz ilości argumentów.
2. wykresy słupkowe ilości zabitych w zależności od użytej broni w danym roku na kontynentach. Wyszukiwanie przy użyciu widgetów
3. wykresy słupkowe ilości ataków w zależności od regionu świata.
4. box-plot (wizualizacja danych statystycznych: mediana,kwartyle,wielkości podejżane o anormlaność, wielkości odstające/błędy)

Statystyka

1. sprawdzenie czy rozkład jest normalny poprzez sprawdzenie wartości p_value (p_val<0 to hipoteza 0 odrzucona. Hipoteza 0 brzmi: badane dane podlegają rozkłądowi normalnemu (rozkład badanych danych =rozkładowi normalnemu) oraz poprzez sprawdzenie czy dane podlegają rozkładowi Poissona (True=rozkład graniczny dwubiegunowy, FALSE= rozkład normalny) Dodatkowo ze względu na charakter danych (zmienne niezależne od siebie/losowe) dokonano wykreślenia gęstości zmiennych dysktertnych  

2. test welcha. Sprawdzenie hipotezy zerowej:
	"średnia(parametr rozkładu) jest identyczna w porównywanych próbkach". Jeżeli p_val>0.05 to brak możliwości odrzucenia hipotezy O. Jeżeli p<0 to przyjęcie hiporezy alternatywnej o nierówności średniej w porównywanych próbkach.
3. test bootstrapowy: metoda służaca weryfikacji hipotez statystycznych. Do przeprowadzenia tego testu, nie jest ważne jakiemu rozkładowi podlegają dane. 

Wytłumaczenienie wyników testu bootstrapowego:
Na przykład gdy hipotezą zerową jest wartość oczekiwana w populacji {\displaystyle \mu =10,}{\displaystyle \mu =10,} a w próbie uzyskaliśmy średnią {\displaystyle {\overline {\mathbf {X} }}=9{,}23,}{\displaystyle {\overline {\mathbf {X} }}=9{,}23,} wówczas wartość {\displaystyle p}p jest prawdopodobieństwem, że średnia z próby będzie się różniła od średniej w populacji o co najmniej {\displaystyle 10-9{,}23=0{,}77.}{\displaystyle 10-9{,}23=0{,}77.} Prawdopodobieństwo to można oszacować, losując próby bootstrap z {\displaystyle \mathbf {X} }\mathbf {X}  i sprawdzając w jakim odsetku losowań średnia wykracza poza przedział {\displaystyle (9{,}23-0{,}77,\ 9{,}23+0{,}77).}{\displaystyle (9{,}23-0{,}77,\ 9{,}23+0{,}77).}"

źródło: https://pl.wikipedia.org/wiki/Bootstrap_(statystyka)

Właściwą aplikacją jest notebook app.ipnb

Pakiety

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import scipy.stats as st
from pandas import Series, DataFrame
from pandas.core.groupby import GroupBy
from scipy.stats import ttest_ind
from scipy.stats import norm
from ipywidgets import widgets
from ipywidgets import interact, interactive, fixed, interact_manual

