# Data Visualization and Preprocessing Toolkit

This Flask application streamlines data visualization and preprocessing, enabling efficient exploration and preparation of datasets. Users can upload a dataset, and the app automatically generates:

## Features

- **Statistical Summary:** Provides key insights, including mean, median, mode, standard deviation, and more for numerical columns.
- **Single-Variable Plots:** Creates all possible plots for individual variables using libraries like Matplotlib, Plotly, and Pyplot.
- **Label Encoding:** Allows users to encode categorical data directly within the app for further analysis.
- **Multi-Variable Plots:** Users can interactively select variables to create scatter plots, heatmaps, and other advanced visualizations, including network graphs with Graphviz.
- **Customization Options:** Provides dynamic and detailed data exploration tools.

## Tech Stack

- **Backend:** Flask
- **Frontend:** HTML, CSS, JavaScript
- **Libraries:** Matplotlib, Plotly, Pyplot, Graphviz, Pandas, NumPy

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/data-viz-preprocessing-toolkit.git
   cd data-viz-preprocessing-toolkit
   ```

2. Create a virtual environment (optional but recommended):

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows use: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the Flask application:

   ```bash
   python app.py
   ```

5. Open your browser and visit:

   ```
   http://127.0.0.1:5000/
   ```

## Usage

1. Upload a CSV file from the landing page.
2. Select the analysis type:
   - Statistical summary
   - Label encoding
   - Graph generation
3. View the generated visualizations.

---

## Visualizations

### 1. Statistical Summary
_Example output will be shown here._

### 2. Single-Variable Plots
_Insert Histogram, Boxplots, or Bar Charts here._

### 3. Multi-Variable Plots
- **Scatter Plots**  
  ![Scatter Plot](graphs/scatter_plot.png)

- **Heatmaps**  
  ![Heatmap](graphs/heatmap.png)

- **Network Graphs (Graphviz)**  
  ![Network Graph](graphs/network_graph.png)

---

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

---

## License

This project is licensed under the MIT License.

---

## Contact

For any questions or suggestions, feel free to reach out:

- **Email:** your-email@example.com
- **GitHub:** [yourusername](https://github.com/yourusername)
