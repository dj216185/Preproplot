from flask import Flask, render_template, request, redirect, url_for, send_file
import pandas as pd
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder,OneHotEncoder

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['STATIC_FOLDER'] = 'static'
app.config['GRAPHS_FOLDER'] = os.path.join(app.config['STATIC_FOLDER'], 'graphs')

# Ensure the upload, static, and graphs folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['STATIC_FOLDER'], exist_ok=True)
os.makedirs(app.config['GRAPHS_FOLDER'], exist_ok=True)

# Function to clear old data
def clear_old_data():
    for folder in [app.config['UPLOAD_FOLDER'], app.config['GRAPHS_FOLDER']]:
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    os.rmdir(file_path)
            except Exception as e:
                print(e)

# Route for file upload (home page)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        clear_old_data()  # Clear old data before processing new file
        
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            return redirect(url_for('dashboard', filename=file.filename))
    return render_template('index.html')

# Dashboard route to display graphs and statistics
@app.route('/dashboard/<filename>', methods=['GET', 'POST'])
def dashboard(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    df = pd.read_csv(filepath)

    # Select numeric columns and object columns
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    object_columns = df.select_dtypes(include=['object']).columns.tolist()
    plots = []

    # Generate basic statistics
    stats_basic = df[numeric_columns].describe()
    stats_skew = df[numeric_columns].apply(pd.Series.skew)
    stats_kurtosis = df[numeric_columns].apply(pd.Series.kurtosis)

    # Combine statistics into a single DataFrame
    stats_combined = pd.DataFrame({
        'Count': stats_basic.loc['count'],
        'Mean': stats_basic.loc['mean'],
        'Std Dev': stats_basic.loc['std'],
        'Min': stats_basic.loc['min'],
        '25%': stats_basic.loc['25%'],
        'Median': stats_basic.loc['50%'],
        '75%': stats_basic.loc['75%'],
        'Max': stats_basic.loc['max'],
        'Skewness': stats_skew,
        'Kurtosis': stats_kurtosis
    })

    # Convert combined statistics to HTML
    stats = stats_combined.to_html(classes='table table-striped table-hover')

    # Automatically generate single-attribute graphs
    for feature in numeric_columns:
        # Histogram
        hist_path = os.path.join(app.config['GRAPHS_FOLDER'], f'{feature}_hist.png')
        plt.figure()
        sns.histplot(df[feature], kde=True, color='purple')
        plt.title(f'Distribution of {feature}')
        plt.savefig(hist_path, bbox_inches='tight')
        plt.close('all')
        plots.append(f'graphs/{feature}_hist.png')

        # Boxplot
        boxplot_path = os.path.join(app.config['GRAPHS_FOLDER'], f'{feature}_box.png')
        plt.figure()
        sns.boxplot(data=df, y=feature)
        plt.title(f'Boxplot of {feature}')
        plt.savefig(boxplot_path, bbox_inches='tight')
        plt.close('all')
        plots.append(f'graphs/{feature}_box.png')

        # Violin Plot
        violin_path = os.path.join(app.config['GRAPHS_FOLDER'], f'{feature}_violin.png')
        plt.figure()
        sns.violinplot(data=df, y=feature)
        plt.title(f'Violin Plot of {feature}')
        plt.savefig(violin_path, bbox_inches='tight')
        plt.close('all')
        plots.append(f'graphs/{feature}_violin.png')

        # Density Plot
        density_path = os.path.join(app.config['GRAPHS_FOLDER'], f'{feature}_density.png')
        plt.figure()
        sns.kdeplot(df[feature], fill=True, color='orange')
        plt.title(f'Density Plot of {feature}')
        plt.savefig(density_path, bbox_inches='tight')
        plt.close('all')
        plots.append(f'graphs/{feature}_density.png')

        # Cumulative Distribution Function (CDF)
        cdf_path = os.path.join(app.config['GRAPHS_FOLDER'], f'{feature}_cdf.png')
        plt.figure()
        sns.ecdfplot(df[feature], color='blue')
        plt.title(f'Cumulative Distribution Function of {feature}')
        plt.xlabel(feature)
        plt.ylabel('CDF')
        plt.savefig(cdf_path, bbox_inches='tight')
        plt.close('all')
        plots.append(f'graphs/{feature}_cdf.png')

    # Automatically generate count plots for categorical variables
    for feature in object_columns:
        count_path = os.path.join(app.config['GRAPHS_FOLDER'], f'{feature}_count.png')
        plt.figure()
        sns.countplot(data=df, y=feature, palette='viridis')
        plt.title(f'Count Plot of {feature}')
        plt.savefig(count_path, bbox_inches='tight')
        plt.close('all')
        plots.append(f'graphs/{feature}_count.png')

    pre_processing_report = ""

    if request.method == 'POST':
        if 'encode_columns' in request.form:
            selected_encode_cols = request.form.getlist('encode_cols')
            pre_processing_report += f"Columns selected for encoding: {', '.join(selected_encode_cols)}<br>"

            # Encoding process
            for col in selected_encode_cols:
                le = OneHotEncoder()
                df[col] = le.fit_transform(df[col])
                pre_processing_report += f"Encoded {col} successfully.<br>"

        # Pre-processing report
        null_counts = df.isnull().sum()
        duplicate_count = df.duplicated().sum()
        pre_processing_report += f"Found {duplicate_count} duplicate rows.<br>"

        if duplicate_count > 0:
            df = df.drop_duplicates()
            pre_processing_report += "Removed duplicate rows.<br>"
        else:
            pre_processing_report += "No duplicate rows found.<br>"

        if null_counts.any():
            pre_processing_report += "Found null values:<br>"
            for col, count in null_counts.items():
                if count > 0:
                    pre_processing_report += f"{col}: {count} null values<br>"
            df = df.dropna()
            pre_processing_report += "Removed null values.<br>"
        else:
            pre_processing_report += "No null values found.<br>"

        # Save the updated CSV
        updated_filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'updated_data.csv')
        df.to_csv(updated_filepath, index=False)

        return render_template('dashboard.html', stats=stats, plots=plots, columns=numeric_columns, object_columns=object_columns, pre_processing_report=pre_processing_report, updated_file='updated_data.csv')

    return render_template('dashboard.html', stats=stats, columns=numeric_columns, object_columns=object_columns, plots=plots)

# Add Export Functionality (for graphs)
@app.route('/download_plot/<filename>', methods=['GET'])
def download_plot(filename):
    plot_path = os.path.join(app.config['STATIC_FOLDER'], filename)
    return send_file(plot_path, as_attachment=True)

# Route to download the updated CSV
@app.route('/download_csv', methods=['GET'])
def download_csv():
    updated_csv_path = os.path.join(app.config['UPLOAD_FOLDER'], 'updated_data.csv')
    return send_file(updated_csv_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
