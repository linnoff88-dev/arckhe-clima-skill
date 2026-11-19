#!/usr/bin/env python3
"""Cliente sem dependências para APIs públicas do Open-Meteo."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
AIR_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"
MARINE_URL = "https://marine-api.open-meteo.com/v1/marine"
FLOOD_URL = "https://flood-api.open-meteo.com/v1/flood"
HISTORY_URL = "https://archive-api.open-meteo.com/v1/archive"

CURRENT_VARS = (
    "temperature_2m,relative_humidity_2m,apparent_temperature,is_day,"
    "precipitation,rain,weather_code,cloud_cover,surface_pressure,"
    "wind_speed_10m,wind_direction_10m,wind_gusts_10m"
)
HOURLY_VARS = (
    "temperature_2m,relative_humidity_2m,apparent_temperature,"
    "precipitation_probability,precipitation,rain,showers,snowfall,"
    "weather_code,cloud_cover,visibility,wind_speed_10m,wind_gusts_10m,"
    "uv_index"
)
DAILY_VARS = (
    "weather_code,temperature_2m_max,temperature_2m_min,"
    "apparent_temperature_max,apparent_temperature_min,sunrise,sunset,"
    "daylight_duration,sunshine_duration,uv_index_max,"
    "precipitation_sum,rain_sum,showers_sum,snowfall_sum,"
    "precipitation_hours,precipitation_probability_max,"
    "wind_speed_10m_max,wind_gusts_10m_max,wind_direction_10m_dominant,"
    "shortwave_radiation_sum,et0_fao_evapotranspiration"
)
AIR_CURRENT = (
    "european_aqi,us_aqi,pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,"
    "sulphur_dioxide,ozone,dust,uv_index,alder_pollen,birch_pollen,"
    "grass_pollen,mugwort_pollen,olive_pollen,ragweed_pollen"
)
MARINE_HOURLY = (
    "wave_height,wave_direction,wave_period,wind_wave_height,"
    "swell_wave_height,swell_wave_direction,swell_wave_period,"
    "sea_level_height_msl,sea_surface_temperature,"
    "ocean_current_velocity,ocean_current_direction"
)
MARINE_DAILY = (
    "wave_height_max,wave_direction_dominant,wave_period_max,"
    "wind_wave_height_max,swell_wave_height_max,"
    "swell_wave_direction_dominant,swell_wave_period_max"
)
HISTORY_DAILY = (
    "weather_code,temperature_2m_max,temperature_2m_min,"
    "temperature_2m_mean,apparent_temperature_max,"
    "apparent_temperature_min,precipitation_sum,rain_sum,"
    "snowfall_sum,precipitation_hours,wind_speed_10m_max,"
    "wind_gusts_10m_max,shortwave_radiation_sum,"
    "et0_fao_evapotranspiration"
)


class CliError(RuntimeError):
    pass


def fetch_json(base_url: str, params: dict[str, Any]) -> tuple[dict[str, Any], str]:
    clean = {key: value for key, value in params.items() if value is not None}
    url = f"{base_url}?{urlencode(clean)}"
    request = Request(url, headers={"User-Agent": "clima-skill/1.0"})
    try:
        with urlopen(request, timeout=30) as response:
            payload = json.load(response)
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")
        raise CliError(f"API HTTP {exc.code}: {detail}") from exc
    except (URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise CliError(f"Falha ao consultar API: {exc}") from exc
    if isinstance(payload, dict) and payload.get("error"):
        raise CliError(str(payload.get("reason", "Erro desconhecido da API")))
    if not isinstance(payload, dict):
        raise CliError("Resposta inesperada da API")
    return payload, url


def geocode(name: str, language: str, country_code: str | None, count: int = 5) -> dict[str, Any]:
    payload, source_url = fetch_json(
        GEOCODE_URL,
        {
            "name": name,
            "count": count,
            "language": language,
            "format": "json",
            "countryCode": country_code,
        },
    )
    results = payload.get("results") or []
    if not results:
        raise CliError(f"Local não encontrado: {name}")
    return {"results": results, "source_url": source_url}


def resolve_location(args: argparse.Namespace) -> tuple[float, float, dict[str, Any]]:
    if args.latitude is not None or args.longitude is not None:
        if args.latitude is None or args.longitude is None:
            raise CliError("Informe latitude e longitude juntas")
        return args.latitude, args.longitude, {
            "name": "Coordenadas fornecidas",
            "latitude": args.latitude,
            "longitude": args.longitude,
        }
    if not args.location:
        raise CliError("Informe --location ou --latitude e --longitude")
    result = geocode(args.location, args.language, args.country_code, count=1)["results"][0]
    return float(result["latitude"]), float(result["longitude"]), result


def location_label(item: dict[str, Any]) -> dict[str, Any]:
    return {
        key: item[key]
        for key in ("name", "admin1", "admin2", "country", "country_code", "latitude", "longitude", "timezone")
        if key in item
    }


def daily_rows(payload: dict[str, Any]) -> list[dict[str, Any]]:
    block = payload.get("daily") or {}
    times = block.get("time") or []
    return [
        {key: values[index] for key, values in block.items() if key != "time" and index < len(values)}
        | {"time": timestamp}
        for index, timestamp in enumerate(times)
    ]


def detect_forecast_risks(payload: dict[str, Any]) -> list[dict[str, str]]:
    flags: list[dict[str, str]] = []
    for row in daily_rows(payload):
        day = row["time"]
        checks = (
            ("tempestade", row.get("weather_code") in (95, 96, 99), "código WMO indica trovoada"),
            ("chuva forte", (row.get("precipitation_sum") or 0) >= 30, "precipitação diária ≥ 30 mm"),
            ("alta chance de chuva", (row.get("precipitation_probability_max") or 0) >= 70, "probabilidade máxima ≥ 70%"),
            ("vento forte", (row.get("wind_gusts_10m_max") or 0) >= 60, "rajadas ≥ 60 km/h"),
            ("calor intenso", (row.get("temperature_2m_max") or -999) >= 35, "máxima ≥ 35 °C"),
            ("frio intenso", (row.get("temperature_2m_min") or 999) <= 5, "mínima ≤ 5 °C"),
            ("UV muito alto", (row.get("uv_index_max") or 0) >= 8, "UV máximo ≥ 8"),
        )
        for kind, matched, reason in checks:
            if matched:
                flags.append({"date": day, "type": kind, "reason": reason})
    return flags


def emit(kind: str, location: dict[str, Any], payload: dict[str, Any], source_url: str) -> None:
    output = {
        "query_type": kind,
        "resolved_location": location_label(location),
        "retrieved_date": date.today().isoformat(),
        "data": payload,
        "source": "Open-Meteo",
        "source_url": source_url,
    }
    if kind == "forecast":
        output["risk_flags"] = detect_forecast_risks(payload)
    print(json.dumps(output, ensure_ascii=False, indent=2))


def base_parser(subparsers: Any, name: str, help_text: str) -> argparse.ArgumentParser:
    parser = subparsers.add_parser(name, help=help_text)
    parser.add_argument("--location", help="Cidade, estado, país ou código postal")
    parser.add_argument("--latitude", type=float)
    parser.add_argument("--longitude", type=float)
    parser.add_argument("--country-code", help="Filtro ISO alpha-2, por exemplo BR")
    parser.add_argument("--language", default="pt", help="Idioma da geocodificação")
    return parser


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Consulta dados do Open-Meteo sem chave de API")
    sub = parser.add_subparsers(dest="command", required=True)

    geo = sub.add_parser("geocode", help="Buscar locais")
    geo.add_argument("--location", required=True)
    geo.add_argument("--country-code")
    geo.add_argument("--language", default="pt")
    geo.add_argument("--count", type=int, default=5, choices=range(1, 101), metavar="1..100")

    forecast = base_parser(sub, "forecast", "Clima atual e previsão")
    forecast.add_argument("--days", type=int, default=7, choices=range(1, 17), metavar="1..16")
    forecast.add_argument("--hourly", action="store_true", help="Incluir série horária")

    air = base_parser(sub, "air", "Qualidade do ar, UV e pólen")
    air.add_argument("--days", type=int, default=5, choices=range(1, 8), metavar="1..7")
    air.add_argument("--hourly", action="store_true")

    marine = base_parser(sub, "marine", "Ondas e condições oceânicas")
    marine.add_argument("--days", type=int, default=7, choices=range(1, 17), metavar="1..16")
    marine.add_argument("--hourly", action="store_true")

    flood = base_parser(sub, "flood", "Vazão fluvial modelada")
    flood.add_argument("--days", type=int, default=14, choices=range(1, 211), metavar="1..210")

    history = base_parser(sub, "history", "Histórico meteorológico")
    history.add_argument("--start", required=True, help="Data YYYY-MM-DD")
    history.add_argument("--end", required=True, help="Data YYYY-MM-DD")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        if args.command == "geocode":
            print(json.dumps(geocode(args.location, args.language, args.country_code, args.count), ensure_ascii=False, indent=2))
            return 0

        lat, lon, resolved = resolve_location(args)
        common = {"latitude": lat, "longitude": lon, "timezone": "auto"}

        if args.command == "forecast":
            params = common | {
                "current": CURRENT_VARS,
                "daily": DAILY_VARS,
                "hourly": HOURLY_VARS if args.hourly else None,
                "forecast_days": args.days,
            }
            payload, url = fetch_json(FORECAST_URL, params)
        elif args.command == "air":
            params = common | {
                "current": AIR_CURRENT,
                "hourly": AIR_CURRENT if args.hourly else None,
                "forecast_days": args.days,
            }
            payload, url = fetch_json(AIR_URL, params)
        elif args.command == "marine":
            params = common | {
                "current": MARINE_HOURLY,
                "daily": MARINE_DAILY,
                "hourly": MARINE_HOURLY if args.hourly else None,
                "forecast_days": args.days,
            }
            payload, url = fetch_json(MARINE_URL, params)
        elif args.command == "flood":
            params = {
                "latitude": lat,
                "longitude": lon,
                "daily": "river_discharge,river_discharge_mean,river_discharge_median,"
                "river_discharge_max,river_discharge_min,river_discharge_p25,river_discharge_p75",
                "forecast_days": args.days,
            }
            payload, url = fetch_json(FLOOD_URL, params)
        else:
            params = common | {
                "start_date": args.start,
                "end_date": args.end,
                "daily": HISTORY_DAILY,
            }
            payload, url = fetch_json(HISTORY_URL, params)

        emit(args.command, resolved, payload, url)
        return 0
    except CliError as exc:
        print(f"erro: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
