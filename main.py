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

    luna.add_task(morning_walk)
    luna.add_task(grooming)
    milo.add_task(breakfast)

    scheduler = Scheduler(owner=owner)

    today = datetime.now().replace(second=0, microsecond=0)
    scheduler.add_entry(luna, morning_walk, today.replace(hour=8, minute=0))
    scheduler.add_entry(milo, breakfast, today.replace(hour=12, minute=30))
    scheduler.add_entry(luna, grooming, today.replace(hour=18, minute=0))

    return scheduler


def print_todays_schedule(scheduler: Scheduler) -> None:
    print("Today's Schedule")
    print("-" * 40)

    today_date = datetime.now().date()
    todays_entries = [entry for entry in scheduler.view_scheduler() if entry[2].date() == today_date]

    if not todays_entries:
        print("No tasks scheduled for today.")
        return

    for pet, task, date_time in todays_entries:
        time_label = date_time.strftime("%I:%M %p")
        print(f"{time_label} | {pet.name} ({pet.species}) | {task.get_details()}")


if __name__ == "__main__":
    demo_scheduler = build_demo_data()
    print_todays_schedule(demo_scheduler)
