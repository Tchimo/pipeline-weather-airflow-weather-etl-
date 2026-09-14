import importlib.util
from pathlib import Path


def test_package_extract_data_module_imports_without_missing_env_error():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "src"
        / "pipeline_weather"
        / "extract_data.py"
    )

    spec = importlib.util.spec_from_file_location(
        "pipeline_weather_extract_data",
        module_path,
    )
    module = importlib.util.module_from_spec(spec)

    try:
        spec.loader.exec_module(module)
    except ValueError as exc:
        raise AssertionError(f"Import should not raise ValueError for API_KEY: {exc}") from exc
