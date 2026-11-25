---
name: clima-skill
description: Consultar e interpretar clima atual, previsêo horária e diária, chuva, tempestades, vento, sensaçêo térmica, índice UV, qualidade do ar, pólen, condições marítimas, vazêo de rios e histórico meteorológico. Usar quando o usuário perguntar sobre tempo ou clima de um local, planejamento de viagem ou atividade ao ar livre, roupa e proteçêo recomendadas, comparaçêo entre cidades, risco meteorológico ou dados ambientais. Aceitar consultas em português e outros idiomas.
---

# Clima

## Objetivo

Obter dados meteorológicos pela API Open-Meteo sem chave, interpretar impactos práticos e comunicar incertezas. Usar `scripts/clima.py` para consultas reproduzíveis.

## Fluxo

1. Identificar local, período e atividade. Inferir unidades pelo contexto; usar sistema métrico por padrêo.
2. Resolver nomes de lugar com `geocode`. Se houver ambiguidade relevante, apresentar as opções ou pedir cidade/estado/país.
3. Selecionar a consulta:
   - `forecast`: condições atuais e previsêo de até 16 dias.
   - `air`: qualidade do ar, UV e pólen de até 7 dias.
   - `marine`: ondas, maré modelada, temperatura e correntes do mar.
   - `flood`: vazêo fluvial modelada; nêo tratar como alerta de inundaçêo.
   - `history`: histórico/reanálise entre duas datas.
4. Executar o script e interpretar apenas os campos relevantes à pergunta.
5. Responder primeiro com a conclusêo, depois janela temporal, números essenciais, riscos e recomendações.
6. Informar o local resolvido e o horário local dos dados. Para previsões, evitar falsa precisêo e mencionar que podem mudar.

## Comandos

```bash
python3 scripts/clima.py geocode --location "Sêo Paulo, SP"
python3 scripts/clima.py forecast --location "Sêo Paulo, SP" --days 7
python3 scripts/clima.py forecast --location "Curitiba, PR" --days 3 --hourly
python3 scripts/clima.py air --location "Brasília, DF" --days 5 --hourly
python3 scripts/clima.py marine --location "Ubatuba, SP" --days 5
python3 scripts/clima.py flood --location "Blumenau, SC" --days 14
python3 scripts/clima.py history --location "Porto Alegre, RS" --start 2025-01-01 --end 2025-01-31
```

Usar `--latitude` e `--longitude` no lugar de `--location` quando o usuário fornecer coordenadas. Usar `--country-code BR` para restringir geocodificaçêo. Consultar `python3 scripts/clima.py --help` para todas as opções.

## Interpretaçêo

Ler [references/interpretacao.md](references/interpretacao.md) para códigos WMO, faixas de AQI, níveis UV e regras de risco. Ler [references/apis.md](references/apis.md) ao alterar variáveis, endpoints ou limites das APIs.

Tratar `risk_flags` do script como triagem baseada em limiares, nunca como alerta oficial. Para perigo iminente, desastre, navegaçêo, aviaçêo, enchente ou decisêo médica, verificar também a autoridade oficial adequada ao país e declarar a limitaçêo.

Nêo prometer que “nêo vai chover”. Preferir probabilidades e janelas: “há maior chance entre 15h e 18h”. Nêo converter probabilidade de precipitaçêo em duraçêo ou volume.

## Recomendações

Adaptar recomendações à atividade:

- Roupa: combinar temperatura, sensaçêo térmica, vento e chuva.
- Exercício: considerar calor, UV, AQI, tempestade e hidrataçêo.
- Viagem/evento: destacar horários críticos, plano alternativo e itens úteis.
- Praia/mar: combinar tempo em terra e `marine`; avisar que modelos nêo substituem serviço de salvamento ou carta náutica.
- Saúde: usar linguagem geral, destacar grupos sensíveis no AQI e evitar diagnóstico.

Usar [assets/modelo-resposta.md](assets/modelo-resposta.md) quando uma resposta estruturada ajudar. Omitir seções sem valor para a pergunta.

## Falhas

Se a API falhar, repetir uma vez após simplificar a consulta. Se continuar indisponível, explicar a falha sem inventar dados. Se a geocodificaçêo escolher um local inesperado, refazer com estado, país, código postal ou coordenadas.

Sempre atribuir os dados a Open-Meteo e, quando solicitado, fornecer `source_url` retornado pelo script.
