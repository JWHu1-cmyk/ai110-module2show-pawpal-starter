from pawpal_system import CareTask, Pet, Owner, Planner

# Create an owner with 60 minutes available per day
owner = Owner(name="Alex", available_minutes_per_day=60)

# Create two pets
dog = Pet(name="Buddy", species="Dog", notes="Golden retriever, high energy")
cat = Pet(name="Whiskers", species="Cat", notes="Indoor cat, senior")

owner.add_pet(dog)
owner.add_pet(cat)

# Add tasks to Buddy
dog.add_care_task(CareTask(title="Morning walk", category="Exercise", duration_minutes=30, priority=5))
dog.add_care_task(CareTask(title="Feed breakfast", category="Feeding", duration_minutes=10, priority=4))
dog.add_care_task(CareTask(title="Brush coat", category="Grooming", duration_minutes=15, priority=2))

# Add tasks to Whiskers
cat.add_care_task(CareTask(title="Feed wet food", category="Feeding", duration_minutes=5, priority=5))
cat.add_care_task(CareTask(title="Litter box cleanup", category="Hygiene", duration_minutes=10, priority=4))
cat.add_care_task(CareTask(title="Play with feather toy", category="Enrichment", duration_minutes=15, priority=3))

# Build and display plans
planner = Planner()

print("=" * 50)
print(f"  Today's Schedule for {owner.name}")
print(f"  Available time: {owner.available_minutes_per_day} minutes")
print("=" * 50)

for pet in owner.pets:
    print(f"\n--- {pet.name} ({pet.species}) ---")
    plan = planner.build_daily_plan(owner, pet)
    print(planner.explain_plan(plan))

print("\n" + "=" * 50)
print("  All tasks across all pets:")
for task in owner.get_all_tasks():
    print(f"  - {task.title} ({task.category})")
