from datetime import datetime

from pawpal_system import Owner, Pet, Scheduler, Task


def test_mark_complete_changes_task_status() -> None:
    task = Task(type="Feeding", description="Morning food", frequency="Daily")

    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_add_task_increases_pet_task_count() -> None:
    pet = Pet(name="Luna", species="Dog")
    initial_count = len(pet.get_tasks())

    task = Task(type="Walking", description="Evening walk", frequency="Daily")
    pet.add_task(task)

    assert len(pet.get_tasks()) == initial_count + 1


def test_mark_task_complete_creates_next_daily_task_with_plus_one_day() -> None:
    owner = Owner(name="Jordan")
    pet = Pet(name="Luna", species="Dog")
    owner.add_pet(pet)
    scheduler = Scheduler(owner=owner)

    task = Task(type="Feeding", description="Morning meal", frequency="Daily")
    pet.add_task(task)
    scheduled_at = datetime(2026, 3, 27, 8, 0)
    entry = scheduler.add_entry(pet, task, scheduled_at)

    next_entry = scheduler.mark_task_complete(entry)

    assert task.completed is True
    assert next_entry is not None
    assert next_entry[2] == datetime(2026, 3, 28, 8, 0)
    assert len(pet.get_tasks()) == 2

    next_task = next_entry[1]
    assert next_task.completed is False
    assert next_task.type == task.type
    assert next_task.description == task.description
    assert next_task.frequency == task.frequency


def test_mark_task_complete_does_not_create_next_for_non_recurring_task() -> None:
    owner = Owner(name="Jordan")
    pet = Pet(name="Milo", species="Cat")
    owner.add_pet(pet)
    scheduler = Scheduler(owner=owner)

    task = Task(type="Training", description="Practice recall command", frequency="Once")
    pet.add_task(task)
    entry = scheduler.add_entry(pet, task, datetime(2026, 3, 27, 10, 0))

    next_entry = scheduler.mark_task_complete(entry)

    assert task.completed is True
    assert next_entry is None
    assert len(pet.get_tasks()) == 1


def test_detect_time_conflicts_for_different_pets() -> None:
    owner = Owner(name="Jordan")
    luna = Pet(name="Luna", species="Dog")
    milo = Pet(name="Milo", species="Cat")
    owner.add_pet(luna)
    owner.add_pet(milo)
    scheduler = Scheduler(owner=owner)

    walk = Task(type="Walking", description="Morning walk", frequency="Daily")
    feed = Task(type="Feeding", description="Breakfast", frequency="Daily")
    luna.add_task(walk)
    milo.add_task(feed)

    same_time = datetime(2026, 3, 27, 9, 0)
    scheduler.add_entry(luna, walk, same_time)
    scheduler.add_entry(milo, feed, same_time)

    conflicts = scheduler.detect_time_conflicts()

    assert scheduler.has_time_conflict(same_time) is True
    assert len(conflicts) == 1
    assert conflicts[0][0][0] is not conflicts[0][1][0]


def test_detect_time_conflicts_for_same_pet() -> None:
    owner = Owner(name="Jordan")
    luna = Pet(name="Luna", species="Dog")
    owner.add_pet(luna)
    scheduler = Scheduler(owner=owner)

    walk = Task(type="Walking", description="Morning walk", frequency="Daily")
    groom = Task(type="Grooming", description="Brush coat", frequency="Weekly")
    luna.add_task(walk)
    luna.add_task(groom)

    same_time = datetime(2026, 3, 27, 17, 30)
    scheduler.add_entry(luna, walk, same_time)
    scheduler.add_entry(luna, groom, same_time)

    conflicts = scheduler.detect_time_conflicts()

    assert scheduler.has_time_conflict(same_time) is True
    assert len(conflicts) == 1
    assert conflicts[0][0][0] is conflicts[0][1][0]


def test_add_entry_with_warning_returns_message_on_conflict() -> None:
    owner = Owner(name="Jordan")
    luna = Pet(name="Luna", species="Dog")
    milo = Pet(name="Milo", species="Cat")
    owner.add_pet(luna)
    owner.add_pet(milo)
    scheduler = Scheduler(owner=owner)

    walk = Task(type="Walking", description="Morning walk", frequency="Daily")
    feed = Task(type="Feeding", description="Breakfast", frequency="Daily")
    luna.add_task(walk)
    milo.add_task(feed)

    same_time = datetime(2026, 3, 28, 9, 0)
    scheduler.add_entry(luna, walk, same_time)

    added_entry, warning = scheduler.add_entry_with_warning(milo, feed, same_time)

    assert added_entry in scheduler.entries
    assert warning is not None
    assert "Scheduling warning" in warning
    assert "Luna:Walking" in warning


def test_add_entry_with_warning_returns_none_when_no_conflict() -> None:
    owner = Owner(name="Jordan")
    luna = Pet(name="Luna", species="Dog")
    owner.add_pet(luna)
    scheduler = Scheduler(owner=owner)

    walk = Task(type="Walking", description="Morning walk", frequency="Daily")
    luna.add_task(walk)

    added_entry, warning = scheduler.add_entry_with_warning(
        luna,
        walk,
        datetime(2026, 3, 28, 9, 0),
    )

    assert added_entry in scheduler.entries
    assert warning is None


def test_view_scheduler_returns_entries_in_chronological_order() -> None:
    owner = Owner(name="Jordan")
    luna = Pet(name="Luna", species="Dog")
    owner.add_pet(luna)
    scheduler = Scheduler(owner=owner)

    walk = Task(type="Walking", description="Morning walk", frequency="Daily")
    feed = Task(type="Feeding", description="Breakfast", frequency="Daily")
    meds = Task(type="Medication", description="Evening medicine", frequency="Daily")
    luna.add_task(walk)
    luna.add_task(feed)
    luna.add_task(meds)

    t1 = datetime(2026, 3, 28, 8, 0)
    t2 = datetime(2026, 3, 28, 12, 0)
    t3 = datetime(2026, 3, 28, 18, 0)

    scheduler.add_entry(luna, meds, t3)
    scheduler.add_entry(luna, walk, t1)
    scheduler.add_entry(luna, feed, t2)

    scheduled_times = [entry[2] for entry in scheduler.view_scheduler()]

    assert scheduled_times == [t1, t2, t3]


def test_has_time_conflict_flags_duplicate_times() -> None:
    owner = Owner(name="Jordan")
    luna = Pet(name="Luna", species="Dog")
    owner.add_pet(luna)
    scheduler = Scheduler(owner=owner)

    walk = Task(type="Walking", description="Morning walk", frequency="Daily")
    feed = Task(type="Feeding", description="Breakfast", frequency="Daily")
    luna.add_task(walk)
    luna.add_task(feed)

    same_time = datetime(2026, 3, 29, 9, 0)
    scheduler.add_entry(luna, walk, same_time)
    assert scheduler.has_time_conflict(same_time) is False

    scheduler.add_entry(luna, feed, same_time)
    assert scheduler.has_time_conflict(same_time) is True


def test_pet_with_no_tasks_returns_empty_lists() -> None:
    owner = Owner(name="Jordan")
    luna = Pet(name="Luna", species="Dog")
    owner.add_pet(luna)
    scheduler = Scheduler(owner=owner)

    assert luna.get_tasks() == []
    assert luna.get_pending_tasks() == []
    assert scheduler.get_tasks_for_pet(luna) == []
    assert scheduler.get_pending_tasks_for_pet(luna) == []