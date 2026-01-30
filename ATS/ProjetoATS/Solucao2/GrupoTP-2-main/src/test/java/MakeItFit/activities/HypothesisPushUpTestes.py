from hypothesis import given, strategies as st
import uuid

class PushUp:
    def __init__(self, user_code=None, date="01/01/2024", duration=0, designation="", name="", reps=0, series=0):
        self.user_code = user_code or uuid.uuid4()
        self.date = date
        self.duration = duration
        self.designation = designation
        self.name = name
        self.reps = reps
        self.series = series
        self.specialization = "PushUp"
        self.caloric_waste = 0

    def caloricWaste(self, index: float) -> int:
        return int(self.reps * self.series * index * 0.1)

    def calculateCaloricWaste(self, index: float):
        self.caloric_waste = self.caloricWaste(index)

    def __eq__(self, other):
        if not isinstance(other, PushUp):
            return False
        return (self.reps == other.reps and
                self.series == other.series and
                self.name == other.name and
                self.designation == other.designation)

    def clone(self):
        return PushUp(
            self.user_code,
            self.date,
            self.duration,
            self.designation,
            self.name,
            self.reps,
            self.series
        )

    def __str__(self):
        return f"{self.name} - {self.reps}x{self.series}"


# Cobertura completa

def test_default_constructor():
    p = PushUp()
    assert p.specialization == "PushUp"

def test_equals_with_different_object():
    p1 = PushUp(name="Push", reps=10, series=2)
    assert p1 != "string"
    assert p1 != PushUp(name="Diff", reps=10, series=2)
    assert p1 != PushUp(name="Push", reps=99, series=2)

@given(reps=st.integers(0, 500), series=st.integers(0, 50), index=st.floats(min_value=0.0, max_value=10.0))
def test_caloric_waste_positive(reps, series, index):
    p = PushUp(reps=reps, series=series)
    waste = p.caloricWaste(index)
    assert waste >= 0

@given(index=st.floats(min_value=0.0, max_value=10.0))
def test_calculate_and_store_waste(index):
    p = PushUp(reps=10, series=5)
    p.calculateCaloricWaste(index)
    assert p.caloric_waste == p.caloricWaste(index)

@given(name=st.text(), designation=st.text(), reps=st.integers(0, 100), series=st.integers(0, 100))
def test_clone_equality(name, designation, reps, series):
    p1 = PushUp(name=name, designation=designation, reps=reps, series=series)
    p2 = p1.clone()
    assert p1 == p2
    assert p1 is not p2

@given(name=st.text(), reps=st.integers(0, 100), series=st.integers(0, 100))
def test_str_representation(name, reps, series):
    p = PushUp(name=name, reps=reps, series=series)
    s = str(p)
    assert name in s
