"""Test weather icon mapping"""

def get_weather_icon(weather_code):
    """Map weather code to unicode icon
    Weather codes from Open-Meteo API:
    0: Clear sky
    1-3: Mainly clear, partly cloudy, and overcast
    45, 48: Fog
    51-67: Rain (drizzle, rain, freezing rain)
    71-77, 85-86: Snow
    80-82: Rain showers
    95-99: Thunderstorm
    """
    if weather_code is None:
        return ""

    # Thunderstorm
    if weather_code >= 95:
        return "⛈"
    # Rainy (including showers, drizzle, freezing rain)
    elif weather_code >= 51 and weather_code <= 67:
        return "⛆"
    elif weather_code >= 80 and weather_code <= 82:
        return "⛆"
    # Snow
    elif weather_code >= 71 and weather_code <= 77:
        return "❄"
    elif weather_code >= 85 and weather_code <= 86:
        return "❄"
    # Cloudy (overcast, fog)
    elif weather_code >= 2 or weather_code >= 45:
        return "☁"
    # Clear/Sunny
    else:
        return "☀"


if __name__ == "__main__":
    # Test cases
    test_cases = [
        (0, "☀", "Clear sky"),
        (1, "☀", "Mainly clear"),
        (2, "☁", "Partly cloudy"),
        (3, "☁", "Overcast"),
        (45, "☁", "Fog"),
        (51, "⛆", "Drizzle"),
        (61, "⛆", "Rain"),
        (71, "❄", "Snow"),
        (80, "⛆", "Rain showers"),
        (95, "⛈", "Thunderstorm"),
        (99, "⛈", "Severe thunderstorm"),
    ]

    print("Weather Icon Mapping Tests:")
    print("-" * 50)
    for code, expected, description in test_cases:
        result = get_weather_icon(code)
        status = "✓" if result == expected else "✗"
        print(f"{status} Code {code:2d}: {result} (expected {expected}) - {description}")

    # Test with temperature
    outdoor_temp = 15.7
    weather_code = 61
    icon = get_weather_icon(weather_code)
    print("\n" + "-" * 50)
    print(f"Example output: {icon}{outdoor_temp:.0f}°C")

