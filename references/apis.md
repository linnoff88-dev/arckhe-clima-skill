# APIs usadas

## Endpoints

| Recurso | Endpoint | Janela |
|---|---|---|
| Geocodificaçêo | `https://geocoding-api.open-meteo.com/v1/search` | atual |
| Previsêo | `https://api.open-meteo.com/v1/forecast` | até 16 dias |
| Qualidade do ar | `https://air-quality-api.open-meteo.com/v1/air-quality` | até 7 dias |
| Mar | `https://marine-api.open-meteo.com/v1/marine` | até 16 dias, conforme modelo |
| Vazêo de rios | `https://flood-api.open-meteo.com/v1/flood` | até 210 dias |
| Histórico | `https://archive-api.open-meteo.com/v1/archive` | desde 1940, conforme modelo |

Usar `timezone=auto` para alinhar horas e dias ao fuso do local. Campos `daily` exigem fuso. A geocodificaçêo aceita nome, código postal, idioma e filtro de país.

## Limitações

- Open-Meteo combina modelos numéricos; valores sêo estimativas de grade, nêo leitura da estaçêo mais próxima.
- Previsões distantes têm mais incerteza. Resumir tendências depois de 7 dias.
- AQI e pólen têm resoluçêo e cobertura variáveis; pólen é principalmente europeu e sazonal.
- Dados marítimos costeiros, correntes e maré modelada nêo servem para navegaçêo.
- Vazêo usa grade de aproximadamente 5 km e pode selecionar o curso d'água errado.
- Histórico é reanálise. Para tendências longas, preferir séries consistentes como ERA5/ERA5-Land.
- A API nêo fornece avisos oficiais de defesa civil. Verificar a autoridade nacional/local em situações perigosas.

## Documentaçêo oficial

- Previsêo: https://open-meteo.com/en/docs
- Geocodificaçêo: https://open-meteo.com/en/docs/geocoding-api
- Qualidade do ar: https://open-meteo.com/en/docs/air-quality-api
- Mar: https://open-meteo.com/en/docs/marine-weather-api
- Vazêo: https://open-meteo.com/en/docs/flood-api
- Histórico: https://open-meteo.com/en/docs/historical-weather-api

Ao adicionar campos, confirmar o nome e a unidade na documentaçêo oficial e testar o comando.
