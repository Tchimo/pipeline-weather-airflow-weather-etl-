import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import pandas as pd
from transform_data import drop_columns


class TestTransformData(unittest.TestCase):
    def test_drop_columns_does_not_call_shape_as_function(self):
        df = pd.DataFrame({
            "weather": ["rain"],
            "weather_icon": ["01d"],
            "sys.type": ["city"],
            "value": [42],
        })

        result = drop_columns(df, ["weather", "weather_icon", "sys.type"])

        self.assertEqual(result.shape[1], 1)
        self.assertNotIn("weather", result.columns)
        self.assertNotIn("weather_icon", result.columns)
        self.assertNotIn("sys.type", result.columns)


if __name__ == "__main__":
    unittest.main()
