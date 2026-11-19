---
name: clima-skill
description: Consultar e interpretar clima atual, previsão horária e diária, chuva, tempestades, vento, sensação térmica, índice UV, qualidade do ar, pólen, condições marítimas, vazão de rios e histórico meteorológico. Usar quando o usuário perguntar sobre tempo ou clima de um local, planejamento de viagem ou atividade ao ar livre, roupa e proteção recomendadas, comparação entre cidades, risco meteorológico ou dados ambientais. Aceitar consultas em português e outros idiomas.
---

# Clima

## Objetivo

Obter dados meteorológicos pela API Open-Meteo sem chave, interpretar impactos práticos e comunicar incertezas. Usar `scripts/clima.py` para consultas reproduzíveis.

## Fluxo

1. Identificar local, período e atividade. Inferir unidades pelo contexto; usar sistema métrico por padrão.
2. Resolver nomes de lugar com `geocode`. Se houver ambiguidade relevante, apresentar as opções ou pedir cidade/estado/país.
3. Selecionar a consulta:
   - `forecast`: condições atuais e previsão de até 16 dias.
   - `air`: qualidade do ar, UV e pólen de até 7 dias.
   - `marine`: ondas, maré modelada, temperatura e correntes do mar.
   - `flood`: vazão fluvial modelada; não tratar como alerta de inundação.
   - `history`: histórico/reanálise entre duas datas.
4. Executar o script e interpretar apenas os campos relevantes à pergunta.
5. Responder primeiro com a conclusão, depois janela temporal, números essenciais, riscos e recomendações.
6. Informar o local resolvido e o horário local dos dados. Para previsões, evitar falsa precisão e mencionar que podem mudar.

## Comandos

```bash
python3 scripts/clima.py geocode --location "São Paulo, SP"
python3 scripts/clima.py forecast --location "São Paulo, SP" --days 7
python3 scripts/clima.py forecast --location "Curitiba, PR" --days 3 --hourly
python3 scripts/clima.py air --location "Brasília, DF" --days 5 --hourly
python3 scripts/clima.py marine --location "Ubatuba, SP" --days 5
python3 scripts/clima.py flood --location "Blumenau, SC" --days 14
python3 scripts/clima.py history --location "Porto Alegre, RS" --start 2025-01-01 --end 2025-01-31
```

Usar `--latitude` e `--longitude` no lugar de `--location` quando o usuário fornecer coordenadas. Usar `--country-code BR` para restringir geocodificação. Consultar `python3 scripts/clima.py --help` para todas as opções.

## Interpretação

Ler [references/interpretacao.md](references/interpretacao.md) para códigos WMO, faixas de AQI, níveis UV e regras de risco. Ler [references/apis.md](references/apis.md) ao alterar variáveis, endpoints ou limites das APIs.

Tratar `risk_flags` do script como triagem baseada em limiares, nunca como alerta oficial. Para perigo iminente, desastre, navegação, aviação, enchente ou decisão médica, verificar também a autoridade oficial adequada ao país e declarar a limitação.

Não prometer que “não vai chover”. Preferir probabilidades e janelas: “há maior chance entre 15h e 18h”. Não converter probabilidade de precipitação em duração ou volume.

## Recomendações

Adaptar recomendações à atividade:

- Roupa: combinar temperatura, sensação térmica, vento e chuva.
- Exercício: considerar calor, UV, AQI, tempestade e hidratação.
- Viagem/evento: destacar horários críticos, plano alternativo e itens úteis.
- Praia/mar: combinar tempo em terra e `marine`; avisar que modelos não substituem serviço de salvamento ou carta náutica.
- Saúde: usar linguagem geral, destacar grupos sensíveis no AQI e evitar diagnóstico.

Usar [assets/modelo-resposta.md](assets/modelo-resposta.md) quando uma resposta estruturada ajudar. Omitir seções sem valor para a pergunta.

## Falhas

Se a API falhar, repetir uma vez após simplificar a consulta. Se continuar indisponível, explicar a falha sem inventar dados. Se a geocodificação escolher um local inesperado, refazer com estado, país, código postal ou coordenadas.

Sempre atribuir os dados a Open-Meteo e, quando solicitado, fornecer `source_url` retornado pelo script.
