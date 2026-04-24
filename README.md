# Clock App - Analog Clock with Circular Doubly Linked Lists

## Overview

This project implements an analog clock simulation using advanced data structures in Python.
The core structure is a circular doubly linked list, used to represent the cyclic behavior of hours, minutes, and seconds.

The architecture follows layered design and Object-Oriented Programming principles:

- High cohesion per class
- Single responsibility per layer
- Decoupled UI and business logic

---

## Folder Structure

- `domain/`
  - Contains core business abstractions and pure domain objects.
  - No external dependencies to frameworks or UI.

- `application/`
  - Contains application orchestration logic.
  - Coordinates domain entities and services through use-case style operations.

- `services/`
  - Contains adapters to external systems, such as system time.
  - Keeps infrastructure concerns out of domain logic.

- `presentation/`
  - Contains Streamlit UI logic.
  - Only consumes application services and displays results.

- `config/`
  - Reserved for environment/configuration files.
  - Useful for future scalability (settings, constants, app config).

---

## File-by-File Explanation

### domain/entities/time_node.py
- Purpose:
  - Defines `TimeNode`, the atomic unit for linked-list storage.
- Responsibilities:
  - Encapsulates node value.
  - Stores next and previous references.
- Relations:
  - Used by `CircularDoublyLinkedList`.

### domain/structures/circular_doubly_linked_list.py
- Purpose:
  - Implements a circular doubly linked list.
- Responsibilities:
  - Append nodes while preserving circular links.
  - Traverse forward and backward.
  - Find a node by value.
- Relations:
  - Uses `TimeNode`.
  - Serves `ClockHand` with cyclic value navigation.

### domain/entities/clock_hand.py
- Purpose:
  - Models a clock hand over a circular doubly linked list.
- Responsibilities:
  - Move forward and backward one position.
  - Expose current value.
- Relations:
  - Consumes `CircularDoublyLinkedList` and its nodes.
  - Used by `ClockEngine` for hour/minute/second state.

### domain/value_objects/clock_time.py
- Purpose:
  - Immutable representation of a time snapshot.
- Responsibilities:
  - Store hour, minute, second.
  - Format output in 12h and 24h forms.
- Relations:
  - Exchanged between `TimeService`, `ClockEngine`, and UI.

### services/time_service.py
- Purpose:
  - Obtain current real system time.
- Responsibilities:
  - Map `datetime.now()` into `ClockTime`.
- Relations:
  - Injected into `ClockEngine` to avoid direct infrastructure coupling.

### application/clock_engine.py
- Purpose:
  - Coordinate the full clock behavior.
- Responsibilities:
  - Build circular ranges for hours/minutes/seconds.
  - Synchronize initial or real time.
  - Advance one second (`tick`) and propagate carry to minute/hour.
  - Move backward one second.
  - Return current simulated time.
- Relations:
  - Uses `ClockHand`, `CircularDoublyLinkedList`, and `TimeService`.

### presentation/clock_ui.py
- Purpose:
  - Provide Streamlit interface for live simulation.
- Responsibilities:
  - Render controls (start, pause, sync, step back).
  - Show simulated time in 24h and 12h.
  - Trigger periodic updates while running.
- Relations:
  - Uses `ClockEngine` as backend boundary.

### presentation/streamlit_app.py
- Purpose:
  - Main Streamlit execution entrypoint.
- Responsibilities:
  - Delegate startup to `ClockUI`.
- Relations:
  - Imports and runs `main()` from `presentation/clock_ui.py`.

### tests/test_circular_doubly_linked_list.py
- Purpose:
  - Validate the linked-list implementation behavior.
- Responsibilities:
  - Verify forward traversal, backward traversal, and strict circular linkage integrity.
- Relations:
  - Tests `CircularDoublyLinkedList` directly.

### tests/test_clock_engine.py
- Purpose:
  - Validate clock transitions and edge cases.
- Responsibilities:
  - Verify second rollover, minute rollover, full-day rollover, and full backward rollover.
- Relations:
  - Tests `ClockEngine` using a fake time service.

---

## Conceptual Explanation

### Why Circular Doubly Linked List?

A clock is inherently cyclic:

- Seconds: 59 -> 00
- Minutes: 59 -> 00
- Hours: 23 -> 00

A circular list models this naturally because the last node points to the first, removing edge-case resets. The doubly linked variant also allows backward movement efficiently.

### How the Clock Is Modeled

- Three circular doubly linked lists represent possible values:
  - Hours: 0..23
  - Minutes: 0..59
  - Seconds: 0..59
- Each hand (`ClockHand`) points to one current node.
- `tick()` moves second hand one node ahead.
  - If second rolls over (59 -> 00), minute moves.
  - If minute also rolls over, hour moves.

### Advantages of This Design

- Natural representation of cyclic time progression.
- O(1) step movement for each hand.
- Clear separation of concerns for maintainability.
- Easy extension (alarms, timezone offsets, chronometer modes).

---

## Run Instructions

1. Install dependencies:

```bash
pip install streamlit matplotlib
```

2. Run UI from project root:

```bash
streamlit run presentation/streamlit_app.py
```

3. Run unit tests:

```bash
python -m unittest discover -s tests -p "test_*.py"
```

---

## Notes

- Code is in English.
- Comments are in Spanish, as requested.
- UI is implemented only with Python + Streamlit.


# execution
./run_clock_app.bat