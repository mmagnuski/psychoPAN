# przydatne kodu skrawki

## Sprawdzamy folder, w którym znajduje się eksperyment
W każdym pliku pythonowym jest dostępna zmienna `__file__`, która mówi o pełnej
ścieżce do danego pliku.
```python
import os.path as op

# wyrzucamy z pełnej ścieżki nazwę pliku
root_dir = op.dirname(__file__)
data_dir = op.join(root_dir, 'data')

# możemy na wszelki wypdaek sprawdzić czy folder istnieje:
if not op.exists(data_dir):
    # jeżeli folderu nie ma, tworzymy go:
    os.mkdir(data_dir) # os powinno być domyślnie zaimportowane
```

## Tworzymy listę plików, które znajdują się w danym folderze
Zakładam, że wcześniej wykonaliśmy to, co znajduje się powyżej.
```python
from glob import glob

img_files = glob(op.join(data_dir, 'img', '*.jpg'))
```

Teraz `img_files` to lista nazw plików, możemy ją adresować aby dostawać się do
poszczególnych nazw plików.
Jeżeli chcemy mieć losową kolejność plików możemy zrobić to na dwa sposoby.

1. przetasować listę nazw plików:

  ```python
  img_files = np.array(img_files)
  np.random.shuffle(img_files)
  ```

2. przetasować adresy do listy:

  ```python
  img_idx = np.arange(len(img_files))
  np.random.shuffle(img_idx)
  ```
  
  Gdy już mamy `img_idx`, aby otrzymać obrazy w przetasowanej kolejności robilibyśmy:
  ```python
  # kroczymy pętlą przez indeksowniki:
  for idx in img_idx:
      this_img = img_files[idx]
      # i coś robimy z plikiem
  ```

  Moglibyśmy też od razu utowrzyć listę obiektów `visual.ImageStim`:
  ```python
  # (w przetasowanej kolejności tzn korzystając z img_idx)
  images = [visual.ImageStim(window, image=img_files[idx]) for idx in img_idx]
  ```

## Wczytujemy pliki z dysku i sprawdzamy ich rozdzielczość i proporcje
Gdy używamy obrazków różnej wielkości i chcemy wyświetlać je w porównywalnym rozmiarze (np. zawsze wysokość == 400 pix), zachowując proporcje boków. Poniżej wczytujemy obrazy z dysku i zachowujemy proporcje (szerokość / wysokość) w słowniku `size_prop`. Klucze tego słownika to nazwy obrazków, wartości to proporcja szerokości do wysokości.
```python
from PIL import Image

img_dir = r'E:\proj\psychopy wrszt\stim'
img_files = os.listdir(img_dir)
img_files = [f for f in img_files if f.endswith('.jpg')]

# wczytujemy
size_prop = dict()
for img in img_files:
    image = Image.open(os.path.join(img_dir, img))
    size_prop[img] = image.width / image.height
```
W kolejnych etapach eksperymentu możemy korzystać ze słownika `size_prop` aby ustawiać adekwatny rozmiar w pikselach, centymetrach czy stopniach kątowych, zachowując proporcje obrazka.

## Tworzymy i uzupełniamy DataFrame
Na początku procedury:
```python
import pandas as pd

columns = ['A', 'B', 'C']
data = pd.DataFrame(columns=columns)
```

Jeżeli z góry wiemy ile będzie triali możemy od razu podać też index
(tzn. oznaczenia wierszy):
```python
import pandas as pd

num_trials = 450
columns = list('ABCD')
index = np.arange(1, num_trials + 1) # + 1 aby mieć z 450 włącznie
data = pd.DataFrame(columns=columns, index=index)
```

Dajmy na to, że później w procedurze mamy obiekt `resp` - klawiaturę zbierającą
odpowiedzi, przy czym nie czeka ona na odpowiedź wiecznie. Chcemy ustawić w
kolumnie `A` rodzaj bodźca kodowany zmienną `condition`, w kolumnie `B` 
udzieloną odpowiedź (`np.nan` - jeżeli nie było odpowiedzi), w kolumnie `C`
wpiszemy czy odpowiedź była poprawna, natomiast w `D` umieścimy czas reakcji.
Zakładam, że mamy już wcześniej utworzoną zmienną `current_trial`, która 
informuje o tym w którym jesteśmy trialu.
```python
data.loc[current_trial, 'A'] = condition
data.loc[current_trial, 'B'] = resp.keys if resp.keys else np.nan
data.loc[current_trial, 'C'] = resp.corr
data.loc[current_trial, 'D'] = resp.rt if resp.keys else np.nan

current_trial += 1

# możemy też na wszelki wypadek zapisywać za każdym razem dane:
data.to_excel(os.path.join(data_dir, expInfo['participant'] + '.xlsx'))
```
