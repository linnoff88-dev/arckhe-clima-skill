ï»¿# ê°Å¸ÅÂ¦ê¯Â¸Â Clima

<div align="center">
  <img src="capa/logo.svg" alt="Arckhé AI" height="48" />
  <p><strong>Arckhé AI</strong></p>
</div>


Skill do Claude para consultar e interpretar clima atual, previsêÂ£o horêÂ¡ria e diêÂ¡ria,
qualidade do ar, êÂ­ndice UV, pêÂ³len, condiêÂ§êÂµes marêÂ­timas, vazêÂ£o de rios e histêÂ³rico
meteorolêÂ³gico pela API **Open-Meteo** ê¢â¬â sem chave de API.

## ê°Å¸ââ Guia de uso

Guia completo (landing + passo a passo): **https://linnoff88-dev.github.io/

## InstalaêÂ§êÂ£o

```bash
git clone https://github.com/linnoff88-dev/clima-skill ~/.claude/skills/clima
```

## Uso rêÂ¡pido

```bash
python3 scripts/clima.py geocode  --location "SêÂ£o Paulo, SP"
python3 scripts/clima.py forecast --location "SêÂ£o Paulo, SP" --days 7
python3 scripts/clima.py air      --location "BrasêÂ­lia, DF" --days 5 --hourly
python3 scripts/clima.py marine   --location "Ubatuba, SP" --days 5
python3 scripts/clima.py flood    --location "Blumenau, SC" --days 14
python3 scripts/clima.py history  --location "Porto Alegre, RS" --start 2025-01-01 --end 2025-01-31
```

Veja `SKILL.md` para o fluxo completo e `references/` para interpretaêÂ§êÂ£o
(cêÂ³digos WMO, faixas de AQI, nêÂ­veis UV) e detalhes das APIs.

Dados por [Open-Meteo](https://open-meteo.com).

---

<div align="center">
  <img src="capa/logo.svg" alt="Arckhé AI" height="32" />
  <p><strong>Arckhé AI</strong></p>
</div>