from flask import Flask, render_template, request
import numpy as np
import pandas as pd

app = Flask(__name__)

# Fungsi untuk simulasi Monte Carlo
def monte_carlo_simulation(num_simulations, current_rate, economic_growth_mean, economic_growth_std):
    """
    Simulasi Monte Carlo untuk prediksi angka kemiskinan.

    Parameters:
    - num_simulations: Jumlah simulasi
    - current_rate: Angka kemiskinan saat ini (dalam persen)
    - economic_growth_mean: Rata-rata pertumbuhan ekonomi tahunan
    - economic_growth_std: Standar deviasi pertumbuhan ekonomi

    Returns:
    - results: Array hasil simulasi
    """
    results = []
    for _ in range(num_simulations):
        # Sampling acak untuk pertumbuhan ekonomi
        economic_growth = np.random.normal(economic_growth_mean, economic_growth_std)

        # Prediksi angka kemiskinan
        # Asumsi: Kemiskinan berkurang dengan faktor pertumbuhan ekonomi negatif
        predicted_rate = current_rate - (economic_growth * 0.5)
        
        # Tidak boleh kurang dari 0
        predicted_rate = max(predicted_rate, 0)
        results.append(predicted_rate)

    return np.array(results)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/simulate', methods=['POST'])
def simulate():
    region = request.form['region']
    current_rate = float(request.form['current_rate'])
    economic_growth_mean = float(request.form['economic_growth_mean'])
    economic_growth_std = float(request.form['economic_growth_std'])
    
    num_simulations = 10000
    simulation_results = monte_carlo_simulation(
        num_simulations, 
        current_rate, 
        economic_growth_mean, 
        economic_growth_std
    )

    mean_prediction = np.mean(simulation_results)
    std_prediction = np.std(simulation_results)

    results_df = pd.DataFrame({
        'Simulasi': range(1, num_simulations + 1),
        'Prediksi Kemiskinan (%)': simulation_results
    })

    return render_template('result.html', 
                           region=region, 
                           current_rate=current_rate, 
                           mean_prediction=mean_prediction,
                           std_prediction=std_prediction,
                           results=results_df)

if __name__ == '__main__':
    app.run(debug=True)
