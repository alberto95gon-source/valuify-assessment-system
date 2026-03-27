# 📓 SOP: Real Estate Valuation Engine (Spain)

## 📋 Objective
Provide a deterministic mathematical valuation for residential properties in Spain using market benchmarks and adjustment factors.

## 🛠️ Inputs (Data Schema)
- `location`: String (City/Province)
- `square_meters`: Number
- `rooms`: Number
- `bathrooms`: Number
- `age`: Number (Years)
- `has_terrace`: Boolean
- `property_images`: Array (File Analysis Simulation)

## ⚙️ Core Logic (Mathematical Model)
1. **Base Price Search**:
   - If city match (Madrid, Barcelona, San Sebastián): Use specific €/m².
   - If province match: Use provincial average.
   - Default: National average (~2500 €/m²).

2. **Market Price Benchmarks (2024/2025 Ref)**:
   - Madrid: 5222 €/m²
   - Barcelona: 4604 €/m²
   - San Sebastián: 6278 €/m²
   - Valencia: 2300 €/m²
   - Málaga: 3400 €/m²
   - National Avg: 2500 €/m²

3. **Adjustment Coefficients ($C$):**
   - **Rooms**: $C_{rooms} = 1 + (rooms * 0.02)$
   - **Bathrooms**: $C_{baths} = 1 + (bathrooms * 0.03)$
   - **Terrace**: $C_{terrace} = 1.05$ (if true)
   - **Age**: $C_{age} = 1 - (age * 0.005)$ (capped at 0.70)
   - **Image Factor**: $C_{img} = 1 + (images\_provided * 0.01)$ (capped at 1.05 for positive visual health).

4. **Installment Plans (Payment Strategy):**
   - **Scenario**: 80% of value financed over 4 years.
   - **Monthly**: $V \times 0.8 \div 48$
   - **Quarterly**: $V \times 0.8 \div 16$
   - **Semi-Annual**: $V \times 0.8 \div 8$
   - **Annual**: $V \times 0.8 \div 4$

5. **Entidades Hipotecarias Autorizadas (Marcas de Lujo):**
   - **Summit Capital - Peak Rate (Fija)**: 2.35% TIN (Estabilidad absoluta para propiedades premium).
   - **Nexus Finance - Dynamic Flow (Variable)**: Euribor (2.22%) + 0.52% Diferencial (Agilidad y potencia financiera).
   - **Apex Mortgage - Hybrid Guard (Mixta)**: 1.8% durante los primeros 10 años, luego variable (La opción más versátil).
   - **Zenith Real - Eco-Shield (Green)**: 2.10% TIN bonificado para construcciones con certificado A++.

6. **OmniGuard - Seguros & Protección Patrimonial:**
   - **Total Shield (Hogar)**: Protección total contra daños, robo e imprevistos lógicos.
   - **Veridian Asset (Vida)**: Seguro de vida vinculado que reduce el TIN hipotecario en 0.10%.
   - **Continuum Safe (Protección)**: Garantía de pagos ante situaciones de desempleo o incapacidad.

7. **Final Formula:**
   $V = (Area \times BasePrice) \times (C_{rooms} \times C_{baths} \times C_{terrace} \times C_{age} \times C_{img})$

## ⚠️ Edge Cases
- Area < 10m²: Return "Información insuficiente".
- Age > 100 years: Use 0.70 factor (historic value cap).
- Unknown location: Use National Avg and flag as "Baja precisión".

## 📤 Output Requirements
1. JSON with computed value.
2. Formatted Markdown for the UI.
3. Plain text (.txt) log for local saving.
