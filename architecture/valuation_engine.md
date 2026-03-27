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

5. **Advanced Mortgage Variants (March 2026 Benchmarks):**
   - **Plan Joven (Youth First):** 95% Financing, Mixed Rate (1.5% fixed for 7 years, then Euribor + 0.45%).
   - **Hipoteca Sostenible (Green):** 80% Financing, Fixed Rate (2.1% fixed), specifically for efficient properties.
   - **Plan Pro (Hybrid):** 80% Financing, Mixed Rate (1.75% fixed for 5 years, then Euribor + 0.55%).
   - **Security Factor**: Life/Home insurance linked reduces TIN by 0.10%.

6. **Insurance Options (Annual Estimates):**
   - **Hogar (Home):** Base price $0.0005 \times V$ (Min 200€).
   - **Vida (Life):** Base price $0.0003 \times V$ per owner.
   - **Protección Pagos:** $0.0001 \times V$ (Job loss/disability).

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
