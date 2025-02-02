import unittest

import numpy as np
import pandas as pd

from gradeit import grade


class GradeTest(unittest.TestCase):
    def setUp(self):
        self.lat1 = 39.702730
        self.lat2 = 39.695368
        self.lon1 = -105.245678
        self.lon2 = -105.209049

        self.expected_dist_km = 3.665130
        self.expected_bearing_deg = 104.63

        self.data = pd.DataFrame()
        self.data["lat"] = np.linspace(39.702730, 39.695368, 10)
        self.data["lon"] = np.linspace(-105.245678, -105.209049, 10)

        self.data["elev_ft"] = np.array(
            [
                7048.15,
                7015.69,
                7157.89,
                7004.84,
                6921.27,
                6840.03,
                6696.7,
                6735.26,
                6554.42,
                6445.5,
            ]
        )

        self.data["dist_ft"] = [
            0,
            1336.0892816,
            1336.0892816,
            1336.0892816,
            1336.0892816,
            1336.12209,
            1336.12209,
            1336.12209,
            1336.12209,
            1336.1548984,
        ]

        self.data["grade_dec"] = [
            0.0,
            -0.0243,
            0.1064,
            -0.1146,
            -0.0625,
            -0.0608,
            -0.1073,
            0.0289,
            -0.1353,
            -0.0815,
        ]

    def test_haversine_no_bearing(self):
        dist = grade.haversine(
            self.lat1, self.lon1, self.lat2, self.lon2, get_bearing=False
        )

        self.assertEqual(dist, self.expected_dist_km)

    def test_haversine_with_bearing(self):
        dist, bearing = grade.haversine(
            self.lat1, self.lon1, self.lat2, self.lon2, get_bearing=True
        )

        self.assertEqual(bearing, self.expected_bearing_deg)

    def test_get_distances(self):
        coordinates = list(zip(self.data.lat, self.data.lon))
        dist_arr = grade.get_distances(coordinates)

        np.testing.assert_array_equal(
            dist_arr, np.array(self.data.dist_ft[1:])
        )

    def test_get_grade_from_coords(self):
        coordinates = list(zip(self.data.lat, self.data.lon))
        dist_arr, grade_arr = grade.get_grade(
            self.data.elev_ft, coordinates=coordinates
        )

        np.testing.assert_array_equal(dist_arr, self.data.dist_ft[1:])
        np.testing.assert_array_equal(grade_arr, self.data.grade_dec)

    def test_get_grade_from_dist(self):
        dist_arr, grade_arr = grade.get_grade(
            self.data.elev_ft, distances=np.array(self.data.dist_ft[1:])
        )

        np.testing.assert_array_equal(dist_arr, self.data.dist_ft[1:])
        np.testing.assert_array_equal(grade_arr, self.data.grade_dec)


if __name__ == "__main__":
    unittest.main(warnings="ignore")
