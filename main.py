from datetime import datetime

from pawpal_system import Owner, Pet, Scheduler, Task


def build_demo_data() -> Scheduler:
    owner = Owner(name="Jordan Smith")

    luna = Pet(name="Luna", species="Dog")
    milo = Pet(name="Milo", species="Cat")

    owner.add_pet(luna)
    owner.add_pet(milo)

    morning_walk = Task(type="Walking", description="30-minute neighborhood walk", frequency="Daily")
    breakfast = Task(type="Feeding", description="Dry food and water refill", frequency="Daily")
    grooming = Task(type="Grooming", description="Brush coat for 10 minutes", frequency="Weekly")
    litter = Task(type="Cleaning", description="Scoop litter box", frequency="Daily")

    luna.add_task(morning_walk)
    luna.add_task(grooming)
    milo.add_task(breakfast)
    milo.add_task(litter)

    grooming.mark_complete()

    scheduler = Scheduler(owner=owner)

    today = datetime.now().replace(second=0, microsecond=0)
    # Insert intentionally out of time order to verify Scheduler.sort_by_time.
    scheduler.add_entry(luna, grooming, today.replace(hour=18, minute=0))
    scheduler.add_entry(milo, litter, today.replace(hour=7, minute=45))
    scheduler.add_entry(luna, morning_walk, today.replace(hour=8, minute=0))

    # Create a same-time conflict and print a warning instead of raising.
    _, conflict_warning = scheduler.add_entry_with_warning(
        milo,
        breakfast,
        today.replace(hour=8, minute=0),
    )
    if conflict_warning:
        print(conflict_warning)

    return scheduler


def print_todays_schedule(scheduler: Scheduler) -> None:
    print("Today's Schedule")
    print("-" * 40)

    today_date = datetime.now().date()
    todays_entries = [entry for entry in scheduler.entries if entry[2].date() == today_date]
    todays_entries = scheduler.sort_by_time(todays_entries)

    if not todays_entries:
        print("No tasks scheduled for today.")
        return

    for pet, task, date_time in todays_entries:
        time_label = date_time.strftime("%I:%M %p")
        print(f"{time_label} | {pet.name} ({pet.species}) | {task.get_details()}")


def print_filtered_tasks(scheduler: Scheduler) -> None:
    print("\nFiltered Tasks")
    print("-" * 40)

    pending_tasks = scheduler.filter_tasks(completed=False)
    print("Pending tasks:")
    for task in pending_tasks:
        pet_name = task.pet.name if task.pet is not None else "Unknown"
        print(f"- {pet_name}: {task.get_details()}")

    luna_tasks = scheduler.filter_tasks(pet_name="Luna")
    print("\nTasks for Luna:")
    for task in luna_tasks:
        print(f"- {task.get_details()}")


if __name__ == "__main__":
    demo_scheduler = build_demo_data()
    print_todays_schedule(demo_scheduler)
    print_filtered_tasks(demo_scheduler)
