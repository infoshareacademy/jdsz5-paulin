Opis ogólny

Aplikacja pozwala na wizualizację danych dotyczących terroryzmu na świecie w latach 1970-2017 (w bazie danych brak roku 1993). Funkcjonalne widgety pozwalają na filtowanie zbioru danych w poszukiwaniu ilości zabitych w zalezności od interesującego użytkownika regionu, roku oraz rodzaju wykorzystanej broni. 

Opis funkcjonalności aplikacj

##wykresy słupkowe ilości zabitych w zależności od regionów
##box-plot rozkładu ilości zabitych w zalezności od regionu (wizualizacja funckji descibe())
##wyznaczenie prawdopodobieństwa wystąpienia aktu terroru przy użyciu danej broni do wszystkich aktów w zbiorze danych
## testy statystyczne: 
			dla małej ilości danych n<=30 't-student' 
			dla dużej ilości danych n>30 "model 3"

## sprawdzanie hipotezy : # W ROKU X DOSZŁO DO WIEKSZEJ ILOŚCI PRZESTĘPSTW Z UZYCIEM BRONI PALNEJ NIŻ POBIĆ W REGIONIE Y
Użycie

Właściwą aplikacją jest notebook app.ipnb

Pakiety
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp 
import scipy.stats as st

Baza danych
link do bazy: 
https://www.kaggle.com/START-UMD/gtd

