# Open-Meteo API Test Automation Framework

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Pytest](https://img.shields.io/badge/pytest-7.0+-green.svg)
![API](https://img.shields.io/badge/API-Open--Meteo-orange.svg)

A scalable API test automation framework for the Open-Meteo Weather API, built with Python and Pytest.

## 🎯 Project Overview

This repository contains automated API tests for the [Open-Meteo Weather API](https://open-meteo.com/), demonstrating comprehensive test coverage including positive scenarios, parametrized tests, and negative testing [web:11][web:12].

## 📋 Test Cases

| Test Case | Description                                                           | Endpoint        | Validations                                                                                                                         | Expected Result                                                                               |
| --------- | --------------------------------------------------------------------- | --------------- | ----------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| **TC001** | Verify current weather for multiple cities (Nürnberg, Patras, Berlin) | `GET /forecast` | • Status code 200<br>• Response time ≤3s<br>• Valid JSON format<br>• Temperature range (-50°C to 50°C)<br>• Non-negative wind speed | Successfully returns current weather data with valid temperature and wind speed for each city |
| **TC002** | Verify hourly forecast data                                           | `GET /forecast` | • Status code 200<br>• Response time ≤3s<br>• Valid JSON format<br>• Contains hourly array<br>• Time array populated                | Successfully returns hourly forecast with temperature and precipitation arrays                |
| **TC003** | Verify daily forecast data                                            | `GET /forecast` | • Status code 200<br>• Response time ≤3s<br>• Valid JSON format<br>• Contains daily max/min temperatures<br>• Time array populated  | Successfully returns 7-day forecast with daily temperature ranges                             |
| **TC004** | Invalid coordinates handling (Negative Test)                          | `GET /forecast` | • Status code 400<br>• API rejects invalid latitude (999)<br>• API rejects invalid longitude (999)                                  | API returns 400 Bad Request and handles invalid input gracefully                              |

## 🔍 Validation Strategy & Rationale

### Status Code Validation

**Why:** Ensures API contract compliance and proper HTTP response behavior [web:16][web:20]. Status codes indicate whether requests succeeded (200), had client errors (400), or experienced server issues (500).

**Implementation:** Every test validates the expected status code matches the actual response.

### Response Time Validation

**Why:** Performance is critical for weather APIs used in real-time applications [web:12]. A 3-second threshold ensures acceptable user experience.

**Implementation:** `validate_response_time()` measures elapsed time using `response.elapsed.total_seconds()`.

### JSON Schema Validation

**Why:** Ensures the API returns properly formatted data that can be parsed by clients [web:18]. Invalid JSON breaks integrations.

**Implementation:** `validate_json_response()` attempts to parse response body as JSON and fails gracefully with clear error messages.

### Business Logic Validation

**Why:** Data must be realistic and within acceptable bounds [web:20]. Weather data outside physical limits (-50°C to 50°C) indicates API errors.

**Implementation:**

- Temperature range assertions prevent unrealistic values
- Non-negative wind speed checks catch calculation errors
- Array length validation ensures data completeness

### Negative Testing

**Why:** APIs must handle invalid inputs gracefully without crashes [web:16]. Error handling quality impacts reliability.

**Implementation:** TC004 sends coordinates outside valid ranges (lat: -90 to 90, lon: -180 to 180) and expects proper 400 responses.

## 🏗️ Repository Structure
