from hypothesis import given, strategies as st
import uuid

class MakeItFitDate:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    def __eq__(self, other):
        return (self.year, self.month, self.day) == (other.year, other.month, other.day)


class Activity:
    def __init__(self, code, realization_date):
        self.code = code
        self.realization_date = realization_date
        self.updated = False

    def getRealizationDate(self):
        return self.realization_date

    def updateActivity(self, index):
        self.updated = True

    def clone(self):
        return self

    def getCode(self):
        return self.code


class TrainingPlan:
    def __init__(self, user_code, start_date):
        self.user_code = user_code
        self.code = uuid.uuid4()
        self.start_date = start_date
        self.activities = []

    def setStartDate(self, date):
        self.start_date = date

    def getStartDate(self):
        return self.start_date

    def addActivity(self, repetitions, activity):
        self.activities.append((repetitions, activity))

    def extractActivities(self, current_date):
        return [act for _, act in self.activities if current_date.year >= act.getRealizationDate().year]

    def updateActivities(self, current_date, index):
        for _, act in self.activities:
            if current_date.year >= act.getRealizationDate().year:
                act.updateActivity(index)

    def getUserCode(self):
        return self.user_code

    def getActivities(self):
        return self.activities

    def getCode(self):
        return self.code


# === TESTES AQUI ===

@given(
    year=st.integers(min_value=2000, max_value=2030),
    month=st.integers(min_value=1, max_value=12),
    day=st.integers(min_value=1, max_value=28)
)
def test_set_start_date(year, month, day):
    user_code = uuid.uuid4()
    plan = TrainingPlan(user_code, MakeItFitDate(2020, 1, 1))
    new_date = MakeItFitDate(year, month, day)
    plan.setStartDate(new_date)
    assert plan.getStartDate() == new_date


@given(
    repetitions=st.integers(min_value=1, max_value=10),
    day_offset=st.integers(min_value=1, max_value=30),
    index=st.floats(min_value=0.1, max_value=5.0)
)
def test_training_plan_add_and_extract(repetitions, day_offset, index):
    user_code = uuid.uuid4()
    today = MakeItFitDate(2025, 5, 31)
    past_date = MakeItFitDate(2025, 5, max(1, 31 - day_offset))
    plan = TrainingPlan(user_code, today)
    activity = Activity(uuid.uuid4(), past_date)
    plan.addActivity(repetitions, activity)
    plan.updateActivities(today, index)
    extracted = plan.extractActivities(today)
    assert activity in extracted
    assert activity.updated is True


@given(
    year=st.integers(min_value=2000, max_value=2030),
    month=st.integers(min_value=1, max_value=12),
    day=st.integers(min_value=1, max_value=28)
)
def test_set_and_get_start_date(year, month, day):
    plan = TrainingPlan(uuid.uuid4(), MakeItFitDate(2020, 1, 1))
    new_date = MakeItFitDate(year, month, day)
    plan.setStartDate(new_date)
    assert plan.getStartDate() == new_date


@given(reps=st.integers(min_value=1, max_value=10))
def test_add_activity_and_get(reps):
    plan = TrainingPlan(uuid.uuid4(), MakeItFitDate(2025, 5, 31))
    act = Activity(uuid.uuid4(), MakeItFitDate(2025, 5, 15))
    plan.addActivity(reps, act)
    activities = plan.getActivities()
    assert (reps, act) in activities
