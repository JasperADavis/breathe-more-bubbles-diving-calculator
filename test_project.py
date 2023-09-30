# CS50P

from project import check_dangers, ft_to_m, absolute_pressure_to_depth, min_depth


def main():
    ft_to_m()
    test_ft_to_m()
    test_absolute_pressure_to_depth()
    test_min_depth()


def test_ft_to_m():
    assert ft_to_m(num=10, unit="m") == 10
    assert float(f"{(ft_to_m(99, unit='ft')):,.2f}") == 30.18


def test_check_dangers():
    gases_dict = {
        "oxygen": 0.0,
        "nitrogen": 8.0,
    }
    assert check_dangers(gases_dict) == [("oxygen: apoxia"), ("nitrogen: severe narcosis: hallucinations & unconsciousness")]


def test_absolute_pressure_to_depth():
    assert absolute_pressure_to_depth(1) == 0
    assert absolute_pressure_to_depth(3.5) == 25


def test_min_depth():
    assert min_depth(.18) == 0
    assert min_depth(.09) == 10

if __name__ == "__main__":
    main()