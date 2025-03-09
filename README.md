# PyC-DataProcessorBindingTest

Una libreria per l'elaborazione dati ad alte prestazioni che combina la facilità d'uso di Python con l'efficienza del C++.

## Panoramica

PyDataProcessor è un progetto che dimostra come utilizzare pybind11 per creare estensioni C++ per Python. La libreria implementa diverse operazioni comuni di elaborazione dati e calcolo numerico, mostrando il notevole vantaggio prestazionale del C++ rispetto al Python puro per operazioni computazionalmente intensive.

## Caratteristiche

- Operazioni statistiche di base (media, mediana, deviazione standard)
- Trasformazione e filtraggio dei dati
- Calcolo di percentili e medie mobili
- Integrazione numerica con diversi metodi (rettangolo, trapezio, Simpson)
- Calcolo di serie e prodotti numerici
- Visualizzazione grafica dei risultati
- Benchmark prestazionali Python vs C++

## Installazione

```bash
# Clona il repository
git clone https://github.com/username/PyDataProcessor.git
cd PyDataProcessor

# Crea e attiva un ambiente virtuale
python -m venv venv
source venv/bin/activate  # Su Windows: venv\Scripts\activate

# Installa le dipendenze e compila la libreria C++
pip install -e .
```

## Utilizzo Base

```python
import numpy as np
import data_processor as dp

# Crea un'istanza del processor
processor = dp.DataProcessor()

# Genera dati casuali
data = np.random.normal(0, 1, 1000).tolist()

# Calcola statistiche
stats = processor.calculate_stats(data)
print(f"Media: {stats[0]}, Mediana: {stats[1]}, DevStd: {stats[2]}")

# Trasforma i dati
transformed = processor.transform(data, 2.5)

# Filtra i dati
filtered = processor.filter(data, 0.5)
```

## Guida alle Operazioni Matematiche

### 1. Statistica Descrittiva

La libreria offre funzioni per calcolare statistiche di base su insiemi di dati:

```python
# Calcolo di media, mediana e deviazione standard
stats = processor.calculate_stats(data)
```

L'implementazione C++ è particolarmente efficiente per grandi dataset, utilizzando algoritmi ottimizzati:
- Media: Somma di tutti i valori divisa per il numero di elementi
- Mediana: Valore centrale in un dataset ordinato
- Deviazione standard: Misura della dispersione dei dati calcolata con la formula √(Σ(x_i - μ)²/n)

### 2. Percentili e Media Mobile

```python
# Calcola percentili a intervalli del 5%
percentiles = processor.calculate_percentiles(data)

# Calcola media mobile con finestra di 100 elementi
rolling_mean = processor.calculate_rolling_mean(data, 100)
```

La media mobile è calcolata per ogni punto i come la media dei valori in una finestra [i-window, i].

### 3. Integrazione Numerica

La libreria implementa tre metodi classici di integrazione numerica:

```python
# Definisci una funzione da integrare
def f(x):
    return x * x

# Integra da a=0 a b=10 con n=1000 punti
result_rect = processor.integrate_rectangle(f, 0, 10, 1000)
result_trap = processor.integrate_trapezoid(f, 0, 10, 1000)
result_simp = processor.integrate_simpson(f, 0, 10, 1000)
```

#### Metodo del Rettangolo
Approssima l'integrale dividendo l'intervallo in n sotto-intervalli e sommando i rettangoli:
- Formula: ∫[a,b] f(x)dx ≈ Σ(i=0 to n-1) f(a + (i+0.5)·h)·h, dove h = (b-a)/n

#### Metodo del Trapezio
Approssima l'integrale usando i trapezi invece dei rettangoli:
- Formula: ∫[a,b] f(x)dx ≈ h/2·[f(a) + 2·Σ(i=1 to n-1) f(a+i·h) + f(b)], dove h = (b-a)/n

#### Metodo di Simpson
Un metodo di ordine superiore che approssima la funzione con parabole:
- Formula: ∫[a,b] f(x)dx ≈ h/3·[f(a) + 4·Σ(i dispari) f(a+i·h) + 2·Σ(i pari) f(a+i·h) + f(b)]

### 4. Serie Numeriche

La libreria consente di calcolare serie e prodotti numerici:

```python
# Calcola la serie per approssimare π/4 = 1 - 1/3 + 1/5 - 1/7 + ...
def pi_term(k):
    return ((-1)**(k+1)) / (2*k - 1)

result = processor.sum_series(pi_term, 1000000)  # Un milione di termini
print(f"π/4 ≈ {result}")

# Calcola un prodotto numerico
def factorial_term(k):
    return k

result = processor.product_series(factorial_term, 5)  # 5! = 5×4×3×2×1 = 120
```

## Benchmark e Confronto Prestazionale

Lo script `analyze_data.py` include un benchmark completo che confronta le prestazioni di Python e C++ per tutte le operazioni implementate:

```bash
python analyze_data.py
```

I risultati tipici mostrano che l'implementazione C++ è significativamente più veloce di Python puro, specialmente per operazioni intensive come l'integrazione numerica e la manipolazione di grandi dataset.

## Nota sull'Implementazione

La libreria utilizza pybind11 per esporre le funzioni C++ a Python. Questo approccio permette di ottenere il meglio da entrambi i mondi: la facilità d'uso e la flessibilità di Python con le prestazioni del C++.

Un aspetto particolarmente interessante è la possibilità di passare funzioni Python a C++ (grazie a `pybind11/functional.h`), permettendo di personalizzare facilmente calcoli come l'integrazione numerica.

## Estensione del Progetto

Il design modulare rende facile aggiungere nuove funzionalità:

1. Implementa una nuova funzione nella classe `DataProcessor` in C++
2. Esponi la funzione in `PYBIND11_MODULE`
3. Utilizza la nuova funzionalità da Python

## Licenza

Questo progetto è rilasciato sotto licenza MIT.
