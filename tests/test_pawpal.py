from pawpal_system import Pet, Task


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
