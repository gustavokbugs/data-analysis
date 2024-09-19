from flask import Flask, jsonify, request, send_file
import pandas as pd
import matplotlib.pyplot as plt
import io
# import os

app = Flask(__name__)

def create_bar_chart(df, x_column, y_column):
    plt.figure(figsize=(10, 6))
    df.plot(kind='bar', x=x_column, y=y_column, color='orange')
    image = io.BytesIO()
    plt.savefig(image, format='png')
    image.seek(0)
    plt.close()
    return image

@app.route('/upload-data', methods=['POST'])
def upload_data():
    file = request.files.get('file')
    if not file:
        return jsonify({"error": "Nenhum arquivo foi enviado"}), 400
    
    try:
        df = pd.read_csv(file)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    summary = df.describe().to_dict()

    return jsonify(summary)

@app.route('/generate-graph', methods=['POST'])
def generate_graph():
    data = request.json
    x_column = data.get("x_column")
    y_column = data.get("y_column")

    if not x_column or not y_column:
        return jsonify({"error": "As colunas nao foram enviadas corretamente"}), 400
    
    df = pd.DataFrame(data.get('table'))

    report_file = 'report.csv'
    df.to_csv(report_file, index=False)

    return send_file(report_file, mimetype='text/csv', as_attachment=True, download_name='report.csv')

if __name__ == '__main__':
    app.run(debug=True)