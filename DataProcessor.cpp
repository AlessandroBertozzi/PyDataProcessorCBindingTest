// DataProcessor.cpp - Implementazione della libreria C++
#include <vector>
#include <algorithm>
#include <numeric>
#include <cmath>
#include <functional>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/functional.h>

namespace py = pybind11;

class DataProcessor {
public:
    // Calcola statistiche di base su un vettore di dati
    std::vector<double> calculateStats(const std::vector<double>& data) {
        if (data.empty()) {
            return {0.0, 0.0, 0.0}; // Media, mediana, deviazione standard
        }

        // Calcolo della media
        double sum = std::accumulate(data.begin(), data.end(), 0.0);
        double mean = sum / data.size();

        // Calcolo della mediana
        std::vector<double> sorted_data = data;
        std::sort(sorted_data.begin(), sorted_data.end());
        double median;
        if (sorted_data.size() % 2 == 0) {
            median = (sorted_data[sorted_data.size()/2 - 1] + sorted_data[sorted_data.size()/2]) / 2.0;
        } else {
            median = sorted_data[sorted_data.size()/2];
        }

        // Calcolo della deviazione standard
        double sq_sum = std::inner_product(data.begin(), data.end(), data.begin(), 0.0);
        double stdev = std::sqrt(sq_sum / data.size() - mean * mean);

        return {mean, median, stdev};
    }

    // Implementa una semplice trasformazione dei dati
    std::vector<double> transform(const std::vector<double>& data, double factor) {
        std::vector<double> result(data.size());
        for (size_t i = 0; i < data.size(); ++i) {
            result[i] = data[i] * factor;
        }
        return result;
    }

    // Filtra i valori in base a una soglia
    std::vector<double> filter(const std::vector<double>& data, double threshold) {
        std::vector<double> result;
        for (const auto& value : data) {
            if (value > threshold) {
                result.push_back(value);
            }
        }
        return result;
    }
    
    // Ordina i dati (operazione intensiva)
    std::vector<double> sort_data(const std::vector<double>& data) {
        std::vector<double> sorted_data = data;
        std::sort(sorted_data.begin(), sorted_data.end());
        return sorted_data;
    }
    
    // Calcola percentili (operazione intensiva)
    std::vector<double> calculate_percentiles(const std::vector<double>& data) {
        if (data.empty()) {
            return {};
        }
        
        std::vector<double> sorted_data = data;
        std::sort(sorted_data.begin(), sorted_data.end());
        
        std::vector<double> percentiles;
        for (int p = 0; p <= 100; p += 5) {
            size_t idx = static_cast<size_t>(p / 100.0 * (sorted_data.size() - 1));
            percentiles.push_back(sorted_data[idx]);
        }
        
        return percentiles;
    }
    
    // Calcola media mobile (operazione intensiva)
    std::vector<double> calculate_rolling_mean(const std::vector<double>& data, size_t window) {
        if (data.empty()) {
            return {};
        }
        
        std::vector<double> result(data.size());
        for (size_t i = 0; i < data.size(); ++i) {
            size_t start = (i >= window) ? i - window : 0;
            double sum = 0.0;
            for (size_t j = start; j <= i; ++j) {
                sum += data[j];
            }
            result[i] = sum / (i - start + 1);
        }
        
        return result;
    }
    
    // Integrazione numerica usando il metodo del rettangolo
    double integrate_rectangle(const std::function<double(double)>& f, double a, double b, int n) {
        double width = (b - a) / n;
        double sum = 0.0;
        
        for (int i = 0; i < n; ++i) {
            double x = a + (i + 0.5) * width;
            sum += f(x);
        }
        
        return sum * width;
    }
    
    // Integrazione numerica usando il metodo del trapezio
    double integrate_trapezoid(const std::function<double(double)>& f, double a, double b, int n) {
        double width = (b - a) / n;
        double sum = 0.5 * (f(a) + f(b));
        
        for (int i = 1; i < n; ++i) {
            double x = a + i * width;
            sum += f(x);
        }
        
        return sum * width;
    }
    
    // Integrazione numerica usando il metodo di Simpson
    double integrate_simpson(const std::function<double(double)>& f, double a, double b, int n) {
        if (n % 2 != 0) n++; // Assicuriamo che n sia pari
        
        double width = (b - a) / n;
        double sum = f(a) + f(b);
        
        for (int i = 1; i < n; ++i) {
            double x = a + i * width;
            sum += f(x) * (i % 2 == 0 ? 2 : 4);
        }
        
        return sum * width / 3.0;
    }
    
    // Calcolo di serie numeriche
    double sum_series(const std::function<double(int)>& term, int n) {
        double sum = 0.0;
        for (int i = 1; i <= n; ++i) {
            sum += term(i);
        }
        return sum;
    }
    
    // Calcolo di prodotti numerici
    double product_series(const std::function<double(int)>& term, int n) {
        double product = 1.0;
        for (int i = 1; i <= n; ++i) {
            product *= term(i);
        }
        return product;
    }
};

// Crea il modulo Python
PYBIND11_MODULE(data_processor, m) {
    m.doc() = "Data processing library implemented in C++";
    
    py::class_<DataProcessor>(m, "DataProcessor")
        .def(py::init<>())
        .def("calculate_stats", &DataProcessor::calculateStats, 
             "Calculate basic statistics (mean, median, standard deviation)")
        .def("transform", &DataProcessor::transform, 
             "Transform data by multiplying with a factor")
        .def("filter", &DataProcessor::filter, 
             "Filter data by keeping only values above a threshold")
        .def("sort_data", &DataProcessor::sort_data, 
             "Sort data in ascending order")
        .def("calculate_percentiles", &DataProcessor::calculate_percentiles, 
             "Calculate percentiles at 5% intervals")
        .def("calculate_rolling_mean", &DataProcessor::calculate_rolling_mean, 
             "Calculate rolling mean with given window size")
        .def("integrate_rectangle", &DataProcessor::integrate_rectangle, 
             "Numerical integration using rectangle method",
             py::arg("f"), py::arg("a"), py::arg("b"), py::arg("n") = 1000)
        .def("integrate_trapezoid", &DataProcessor::integrate_trapezoid, 
             "Numerical integration using trapezoid method",
             py::arg("f"), py::arg("a"), py::arg("b"), py::arg("n") = 1000)
        .def("integrate_simpson", &DataProcessor::integrate_simpson, 
             "Numerical integration using Simpson's method",
             py::arg("f"), py::arg("a"), py::arg("b"), py::arg("n") = 1000)
        .def("sum_series", &DataProcessor::sum_series, 
             "Calculate sum of numerical series",
             py::arg("term"), py::arg("n"))
        .def("product_series", &DataProcessor::product_series, 
             "Calculate product of numerical series",
             py::arg("term"), py::arg("n"));
}
