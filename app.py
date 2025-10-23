from flask import Flask, jsonify
from LoginSecopSinGUI import generar_cookies_secop
from Search_Secop import procesar_datos_func

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ API Flask funcionando"

@app.route("/generar-cookies", methods=["GET"])
def generar_cookies():
    cookies = generar_cookies_secop()
    if cookies:
        return jsonify({"status": "ok", "cookies": cookies})
    else:
        return jsonify({"status": "error", "message": "No se pudieron generar las cookies"}), 500
    
@app.route('/procesar_datos', methods=['GET'])
def procesar_datos_route():
    print("📩 Petición recibida desde n8n...")
    try:
        resultados = procesar_datos_func()
        return jsonify(resultados)
    except Exception as e:
        print("❌ Error interno:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
