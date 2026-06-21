"""
AstraCare — API REST Flask
Expõe a lógica de cálculo de risco clínico do projeto Python para o frontend Estelar.

Endpoints:
  POST /calcular-risco  -> Calcula nível de risco (EMERGENCIA/URGENTE/ATENCAO/BAIXO)
  GET  /health          -> Health check
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import risco

app = Flask(__name__)
CORS(app)


@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "UP", "service": "AstraCare Risco API", "versao": "1.0.0"}), 200


@app.route('/calcular-risco', methods=['POST'])
def calcular_risco_endpoint():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"erro": "Body JSON obrigatório"}), 400

        sinais_campos = ['temperatura', 'saturacao', 'frequencia_cardiaca', 'pressao_sistolica', 'pressao_diastolica']
        for campo in sinais_campos:
            if campo not in data.get('sinais', {}):
                return jsonify({"erro": f"Campo obrigatório ausente em sinais: {campo}"}), 400

        sinais = {
            "temperatura":          float(data['sinais']['temperatura']),
            "saturacao":            float(data['sinais']['saturacao']),
            "frequencia_cardiaca":  float(data['sinais']['frequencia_cardiaca']),
            "pressao_sistolica":    float(data['sinais']['pressao_sistolica']),
            "pressao_diastolica":   float(data['sinais']['pressao_diastolica']),
        }

        sintomas = {
            "dor_peito":         bool(data.get('sintomas', {}).get('dor_peito', False)),
            "falta_ar":          bool(data.get('sintomas', {}).get('falta_ar', False)),
            "confusao":          bool(data.get('sintomas', {}).get('confusao', False)),
            "desmaio":           bool(data.get('sintomas', {}).get('desmaio', False)),
            "sangramento":       bool(data.get('sintomas', {}).get('sangramento', False)),
            "febre_persistente": bool(data.get('sintomas', {}).get('febre_persistente', False)),
            "vomitos":           bool(data.get('sintomas', {}).get('vomitos', False)),
            "dor_forte":         bool(data.get('sintomas', {}).get('dor_forte', False)),
        }

        contexto = {
            "distancia_hospital_km": float(data.get('contexto', {}).get('distancia_hospital_km', 0)),
            "internet_disponivel":   bool(data.get('contexto', {}).get('internet_disponivel', True)),
            "medicamentos_basicos":  bool(data.get('contexto', {}).get('medicamentos_basicos', True)),
        }

        resultado = risco.calcular_risco(sinais, sintomas, contexto)
        return jsonify(resultado), 200

    except (ValueError, KeyError) as e:
        return jsonify({"erro": f"Dado inválido: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"erro": f"Erro interno: {str(e)}"}), 500


if __name__ == '__main__':
    print("🩺  AstraCare Risco API iniciando...")
    print("❤️  Health check: http://localhost:5001/health")
    app.run(debug=True, host='0.0.0.0', port=5001)
