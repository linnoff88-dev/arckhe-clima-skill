# APIs usadas

## Endpoints

| Recurso | Endpoint | Janela |
|---|---|---|
| Geocodificação | `https://geocoding-api.open-meteo.com/v1/search` | atual |
| Previsão | `https://api.open-meteo.com/v1/forecast` | até 16 dias |
| Qualidade do ar | `https://air-quality-api.open-meteo.com/v1/air-quality` | até 7 dias |
| Mar | `https://marine-api.open-meteo.com/v1/marine` | até 16 dias, conforme modelo |
| Vazão de rios | `https://flood-api.open-meteo.com/v1/flood` | até 210 dias |
| Histórico | `https://archive-api.open-meteo.com/v1/archive` | desde 1940, conforme modelo |

Usar `timezone=auto` para alinhar horas e dias ao fuso do local. Campos `daily` exigem fuso. A geocodificação aceita nome, código postal, idioma e filtro de país.

## Limitações

- Open-Meteo combina modelos numéricos; valores são estimativas de grade, não leitura da estação mais próxima.
- Previsões distantes têm mais incerteza. Resumir tendências depois de 7 dias.
- AQI e pólen têm resolução e cobertura variáveis; pólen é principalmente europeu e sazonal.
- Dados marítimos costeiros, correntes e maré modelada não servem para navegação.
- Vazão usa grade de aproximadamente 5 km e pode selecionar o curso d'água errado.
- Histórico é reanálise. Para tendências longas, preferir séries consistentes como ERA5/ERA5-Land.
- A API não fornece avisos oficiais de defesa civil. Verificar a autoridade nacional/local em situações perigosas.

## Documentação oficial

- Previsão: https://open-meteo.com/en/docs
- Geocodificação: https://open-meteo.com/en/docs/geocoding-api
- Qualidade do ar: https://open-meteo.com/en/docs/air-quality-api
- Mar: https://open-meteo.com/en/docs/marine-weather-api
- Vazão: https://open-meteo.com/en/docs/flood-api
- Histórico: https://open-meteo.com/en/docs/historical-weather-api

Ao adicionar campos, confirmar o nome e a unidade na documentação oficial e testar o comando.
