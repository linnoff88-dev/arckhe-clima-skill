# ðŸŒ¦ï¸ Clima

<div align="center">
  <img src="capa/logo.svg" alt="Arckhé AI" height="48" />
  <p><strong>Arckhé AI</strong></p>
</div>


Skill do Claude para consultar e interpretar clima atual, previsÃ£o horÃ¡ria e diÃ¡ria,
qualidade do ar, Ã­ndice UV, pÃ³len, condiÃ§Ãµes marÃ­timas, vazÃ£o de rios e histÃ³rico
meteorolÃ³gico pela API **Open-Meteo** â€” sem chave de API.

## ðŸ“– Guia de uso

Guia completo (landing + passo a passo): **https://inematds.github.io/clima-skill/guia/**

## InstalaÃ§Ã£o

```bash
git clone https://github.com/inematds/clima-skill ~/.claude/skills/clima
```

## Uso rÃ¡pido

```bash
python3 scripts/clima.py geocode  --location "SÃ£o Paulo, SP"
python3 scripts/clima.py forecast --location "SÃ£o Paulo, SP" --days 7
python3 scripts/clima.py air      --location "BrasÃ­lia, DF" --days 5 --hourly
python3 scripts/clima.py marine   --location "Ubatuba, SP" --days 5
python3 scripts/clima.py flood    --location "Blumenau, SC" --days 14
python3 scripts/clima.py history  --location "Porto Alegre, RS" --start 2025-01-01 --end 2025-01-31
```

Veja `SKILL.md` para o fluxo completo e `references/` para interpretaÃ§Ã£o
(cÃ³digos WMO, faixas de AQI, nÃ­veis UV) e detalhes das APIs.

Dados por [Open-Meteo](https://open-meteo.com).

---

<div align="center">
  <img src="capa/logo.svg" alt="Arckhé AI" height="32" />
  <p><strong>Arckhé AI</strong></p>
</div>