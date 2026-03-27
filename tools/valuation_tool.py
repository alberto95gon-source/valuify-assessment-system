import json
import os
from datetime import datetime

# Benchmarks 2024-2025 (Spain) - Layer 1 Architecture (valuation_engine.md)
BENCHMARKS = {
    "madrid": 5222,
    "barcelona": 4604,
    "san sebastian": 6278,
    "valencia": 2300,
    "malaga": 3400,
    "nacional": 2500
}

def calculate_valuation(data):
    """
    Core Deterministic Valuation Engine (A.N.T Layer 3: Tools)
    Following the SOP in architecture/valuation_engine.md
    """
    try:
        location = data.get("location", "nacional").lower()
        area = float(data.get("square_meters", 0))
        rooms = int(data.get("rooms", 0))
        baths = int(data.get("bathrooms", 0))
        age = int(data.get("age", 0))
        has_terrace = data.get("has_terrace", False)

        if area < 10:
            return {"error": "Área insuficiente para tasación (mínimo 10m2)."}

        # 1. Base Price Selection
        base_price = BENCHMARKS.get(location, BENCHMARKS["nacional"])
        precision = "Alta" if location in BENCHMARKS else "Baja (Media Nacional)"

        # 2. Adjustments
        c_rooms = 1 + (rooms * 0.02)
        c_baths = 1 + (baths * 0.03)
        c_terrace = 1.05 if has_terrace else 1.0
        
        # Age Factor (max 30% reduction)
        age_reduction = age * 0.005
        c_age = max(0.70, 1 - age_reduction)

        # 3. Final Calculation
        estimated_value = (area * base_price) * (c_rooms * c_baths * c_terrace * c_age)
        price_per_m2 = estimated_value / area

        # 4. Payload Refinement
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        result = {
            "estimated_value": round(estimated_value, 2),
            "price_per_m2": round(price_per_m2, 2),
            "benchmark_used": location.capitalize(),
            "precision_score": precision,
            "valuation_date": timestamp,
            "inputs_echo": data
        }

        # 5. Generate TXT Report for delivery (Phase 5 Requirement)
        report_txt = generate_txt_report(result)
        result["txt_report_content"] = report_txt
        
        return result

    except Exception as e:
        return {"error": f"Fallo en el motor de cálculo: {str(e)}"}

def generate_txt_report(result):
    """Genera el contenido para el Bloc de Notas (.txt)"""
    report = f"""
=========================================
      REPORTE DE TASACIÓN INMOBILIARIA
=========================================
Fecha: {result['valuation_date']}
Ubicación: {result['benchmark_used']} (Precisión: {result['precision_score']})
-----------------------------------------
VALOR ESTIMADO: {result['estimated_value']:,.2f} EUR
Precio/m2: {result['price_per_m2']:,.2f} EUR
-----------------------------------------
DETALLES DE LA PROPIEDAD:
- Superficie: {result['inputs_echo']['square_meters']} m2
- Habitaciones: {result['inputs_echo']['rooms']}
- Baños: {result['inputs_echo']['bathrooms']}
- Antigüedad: {result['inputs_echo']['age']} años
- Terraza: {'Sí' if result['inputs_echo']['has_terrace'] else 'No'}
-----------------------------------------
Generado por: System Pilot (Antigravity)
Protocolo BLAST v1.0
=========================================
"""
    return report.strip()

if __name__ == "__main__":
    # Handshake Verification (Phase 2: Link)
    test_data = {
        "location": "Madrid",
        "square_meters": 100,
        "rooms": 3,
        "bathrooms": 2,
        "age": 10,
        "has_terrace": True
    }
    print(json.dumps(calculate_valuation(test_data), indent=2))
