#!/usr/bin/env python3
# analyze_data.py - Script Python che utilizza la libreria C++

import numpy as np
import matplotlib.pyplot as plt
import time
import data_processor as dp
from tqdm import tqdm

def generate_test_data(size=10000000000):
    """Genera dati di test con distribuzione normale"""
    print(f"Generazione di {size:,} punti dati...")
    with tqdm(total=1) as pbar:
        data = np.random.normal(0, 1, size).tolist()
        pbar.update(1)
    return data

def benchmark_comparison(data):
    """Confronta le prestazioni di Python e C++"""
    print("Esecuzione calcoli in Python...")
    # Python/NumPy implementation
    start_time = time.time()
    numpy_mean = np.mean(data)
    numpy_median = np.median(data)
    numpy_std = np.std(data)
    
    # Computazione intensiva aggiuntiva in Python
    print("  Ordinamento dati...")
    sorted_data = sorted(data)
    
    print("  Calcolo percentili...")
    percentiles = [np.percentile(data, p) for p in tqdm(range(0, 101, 5))]
    
    print("  Calcolo media mobile...")
    rolling_mean = []
    for i in tqdm(range(len(data))):
        rolling_mean.append(np.mean(data[max(0, i-1000):i+1]))
    
    python_time = time.time() - start_time
    
    print("\nEsecuzione calcoli in C++...")
    # C++ implementation
    processor = dp.DataProcessor()
    start_time = time.time()
    
    with tqdm(total=4, desc="Operazioni C++") as pbar:
        cpp_stats = processor.calculate_stats(data)
        pbar.update(1)
        
        cpp_sorted = processor.sort_data(data)
        pbar.update(1)
        
        cpp_percentiles = processor.calculate_percentiles(data)
        pbar.update(1)
        
        cpp_rolling_mean = processor.calculate_rolling_mean(data, 1000)
        pbar.update(1)
    
    cpp_time = time.time() - start_time
    
    print(f"\nPython/NumPy: Media={numpy_mean:.4f}, Mediana={numpy_median:.4f}, DevStd={numpy_std:.4f}")
    print(f"C++: Media={cpp_stats[0]:.4f}, Mediana={cpp_stats[1]:.4f}, DevStd={cpp_stats[2]:.4f}")
    print(f"Tempo Python: {python_time:.6f} s, Tempo C++: {cpp_time:.6f} s")
    print(f"C++ è {python_time/cpp_time:.2f}x più veloce di Python")

def visualize_transformed_data(data, factor=2.0):
    """Visualizza i dati originali e trasformati"""
    processor = dp.DataProcessor()
    transformed_data = processor.transform(data, factor)
    
    plt.figure(figsize=(12, 6))
    
    plt.subplot(1, 2, 1)
    plt.hist(data, bins=50, alpha=0.7, color='blue')
    plt.title('Dati Originali')
    plt.xlabel('Valore')
    plt.ylabel('Frequenza')
    
    plt.subplot(1, 2, 2)
    plt.hist(transformed_data, bins=50, alpha=0.7, color='red')
    plt.title(f'Dati Trasformati (fattore={factor})')
    plt.xlabel('Valore')
    
    plt.tight_layout()
    plt.savefig('data_transformation.png')
    plt.close()
    
    print(f"Grafico salvato come 'data_transformation.png'")

def filter_and_analyze(data, threshold=0.0):
    """Filtra e analizza i dati usando la libreria C++"""
    print(f"Filtraggio dati con soglia > {threshold}...")
    processor = dp.DataProcessor()
    
    with tqdm(total=2) as pbar:
        filtered_data = processor.filter(data, threshold)
        pbar.update(1)
        
        print(f"Calcolo statistiche su {len(filtered_data):,} elementi filtrati...")
        if filtered_data:
            stats = processor.calculate_stats(filtered_data)
        pbar.update(1)
    
    print(f"Dati originali: {len(data):,} elementi")
    print(f"Dati filtrati (>{threshold}): {len(filtered_data):,} elementi")
    
    if filtered_data:
        print(f"Statistiche dei dati filtrati: Media={stats[0]:.4f}, Mediana={stats[1]:.4f}, DevStd={stats[2]:.4f}")

def benchmark_numerical_methods():
    """Confronta le prestazioni dei metodi numerici tra Python e C++"""
    print("\n=== Confronto Metodi Numerici Python vs C++ ===")
    
    # Definiamo una funzione da integrare (x^2)
    def func(x):
        return x * x
    
    # Parametri di integrazione
    a, b = 0.0, 10.0
    n = 1000000  # Numero elevato di punti per un test intensivo
    
    # Implementazione Python dell'integrazione con rettangoli
    print("Esecuzione integrazione numerica in Python...")
    start_time = time.time()
    
    with tqdm(total=3) as pbar:
        # Metodo del rettangolo in Python
        width = (b - a) / n
        py_sum_rect = 0.0
        for i in range(n):
            x = a + (i + 0.5) * width
            py_sum_rect += func(x)
        py_rect = py_sum_rect * width
        pbar.update(1)
        
        # Metodo del trapezio in Python
        width = (b - a) / n
        py_sum_trap = 0.5 * (func(a) + func(b))
        for i in range(1, n):
            x = a + i * width
            py_sum_trap += func(x)
        py_trap = py_sum_trap * width
        pbar.update(1)
        
        # Metodo di Simpson in Python
        width = (b - a) / n
        py_sum_simp = func(a) + func(b)
        for i in range(1, n):
            x = a + i * width
            py_sum_simp += func(x) * (4 if i % 2 == 1 else 2)
        py_simp = py_sum_simp * width / 3.0
        pbar.update(1)
    
    python_time = time.time() - start_time
    
    # Implementazione C++ dell'integrazione
    print("Esecuzione integrazione numerica in C++...")
    processor = dp.DataProcessor()
    start_time = time.time()
    
    with tqdm(total=3) as pbar:
        cpp_rect = processor.integrate_rectangle(func, a, b, n)
        pbar.update(1)
        
        cpp_trap = processor.integrate_trapezoid(func, a, b, n)
        pbar.update(1)
        
        cpp_simp = processor.integrate_simpson(func, a, b, n)
        pbar.update(1)
    
    cpp_time = time.time() - start_time
    
    # Risultati
    print("\nRisultati dell'integrazione di x^2 da 0 a 10:")
    print(f"Valore analitico esatto: {(b**3 - a**3)/3:.6f}")
    print(f"Python: Rettangolo={py_rect:.6f}, Trapezio={py_trap:.6f}, Simpson={py_simp:.6f}")
    print(f"C++: Rettangolo={cpp_rect:.6f}, Trapezio={cpp_trap:.6f}, Simpson={cpp_simp:.6f}")
    print(f"Tempo Python: {python_time:.6f} s, Tempo C++: {cpp_time:.6f} s")
    print(f"C++ è {python_time/cpp_time:.2f}x più veloce di Python")
    
    # Serie infinita: calcolo di pi/4 = 1 - 1/3 + 1/5 - 1/7 + ...
    print("\n=== Calcolo di pi mediante serie ===")
    
    def pi_term(k):
        return ((-1)**(k+1)) / (2*k - 1)
    
    n_terms = 1000000  # Un milione di termini
    
    print("Calcolo serie in Python...")
    start_time = time.time()
    py_sum = 0.0
    for i in tqdm(range(1, n_terms + 1)):
        py_sum += pi_term(i)
    python_time = time.time() - start_time
    
    print("Calcolo serie in C++...")
    start_time = time.time()
    cpp_sum = processor.sum_series(pi_term, n_terms)
    cpp_time = time.time() - start_time
    
    print(f"\nCalcolo di pi/4 mediante serie:")
    print(f"Valore di riferimento pi/4: {np.pi/4:.10f}")
    print(f"Python (somma di {n_terms} termini): {py_sum:.10f}")
    print(f"C++ (somma di {n_terms} termini): {cpp_sum:.10f}")
    print(f"Tempo Python: {python_time:.6f} s, Tempo C++: {cpp_time:.6f} s")
    print(f"C++ è {python_time/cpp_time:.2f}x più veloce di Python")

def main():
    print("Generazione dati di test...")
    # Usa 2 milioni di punti per un test più rapido ma comunque significativo
    data = generate_test_data(2000000)
    
    print("\n=== Confronto Prestazioni Python vs C++ (operazioni complesse) ===")
    benchmark_comparison(data)
    
    print("\n=== Test Metodi Numerici ===")
    benchmark_numerical_methods()
    
    print("\n=== Trasformazione Dati ===")
    # Usa un campione più piccolo per la visualizzazione
    sample_data = data[:10000]
    visualize_transformed_data(sample_data, factor=2.5)
    
    print("\n=== Filtraggio e Analisi ===")
    filter_and_analyze(data, threshold=0.5)

if __name__ == "__main__":
    main()
