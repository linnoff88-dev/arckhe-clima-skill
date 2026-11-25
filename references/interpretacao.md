# Interpretaçêo meteorológica

## Códigos WMO

| Código | Condiçêo |
|---|---|
| 0 | céu limpo |
| 1–3 | pouco nublado a encoberto |
| 45, 48 | nevoeiro |
| 51–57 | garoa, inclusive congelante |
| 61–67 | chuva, inclusive congelante |
| 71–77 | neve |
| 80–82 | pancadas de chuva |
| 85, 86 | pancadas de neve |
| 95 | trovoada |
| 96, 99 | trovoada com granizo |

## Índice UV

| Faixa | Categoria | Orientaçêo geral |
|---|---|---|
| 0–2 | baixo | proteçêo básica |
| 3–5 | moderado | sombra, roupa e protetor |
| 6–7 | alto | reduzir exposiçêo no pico |
| 8–10 | muito alto | evitar exposiçêo prolongada |
| 11+ | extremo | proteçêo máxima |

## AQI dos EUA

| Faixa | Categoria |
|---|---|
| 0–50 | bom |
| 51–100 | moderado |
| 101–150 | insalubre para grupos sensíveis |
| 151–200 | insalubre |
| 201–300 | muito insalubre |
| 301–500 | perigoso |

Para o AQI europeu: 0–20 bom, 21–40 razoável, 41–60 moderado, 61–80 ruim, 81–100 muito ruim e acima de 100 extremamente ruim.

## Triagem de riscos

O script marca, por dia:

- trovoada: WMO 95, 96 ou 99;
- chuva forte: acumulado diário de pelo menos 30 mm;
- alta chance de chuva: probabilidade máxima de pelo menos 70%;
- vento forte: rajada de pelo menos 60 km/h;
- calor intenso: máxima de pelo menos 35 °C;
- frio intenso: mínima de no máximo 5 °C;
- UV muito alto: índice máximo de pelo menos 8.

Esses limiares sêo sinais práticos, nêo critérios universais nem alertas oficiais. Contextualizar clima local, vulnerabilidade, duraçêo e atividade. Nêo concluir risco de enchente apenas por chuva ou vazêo modelada.

## Linguagem

- Dizer “probabilidade de precipitaçêo”, nêo “percentual da cidade que receberá chuva”.
- Separar chance, intensidade e acumulado.
- Distinguir temperatura do ar de sensaçêo térmica.
- Usar horários locais e datas absolutas.
- Em comparaçêo de destinos, aplicar a mesma janela e as mesmas métricas.
