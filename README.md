# AI: Integrating Robust Error Handling in OOP

## Objective

Apply AI-driven scaffolding to enhance a refactored `Product` class by
integrating robust exception handling and data validation using
Python's `@property` decorators and a custom exception, improving the
code's resilience and data integrity.

## Files

| File | Description |
|---|---|
| `initial_code.py` | The starting-point `Product` / `InventoryManager` classes, with unvalidated `price` and `quantity` attributes. |
| `refactored_code.py` | The AI-scaffolded version: `price` and `quantity` are now validated `@property` attributes, backed by a custom `InvalidProductDataError` exception, plus the invalid-input test case appended at the end. |

## Points of Failure Identified

In `initial_code.py`, `Product.price` and `Product.quantity` are plain
public attributes assigned directly in `__init__` with no validation.
Any code path — including `InventoryManager.update_quantity` — can set
either attribute to a nonsensical value (a negative price, a negative
quantity, a string, `None`, etc.) without the object ever raising an
error. That bad state then silently propagates into
`calculate_total_value()` and `display_inventory()`, producing
incorrect totals or crashing later with a confusing, unrelated
`TypeError` far from the actual point where the bad data was
introduced.

## AI Prompt Used

The following single prompt was submitted to Gemini Code Assist in
VS Code to scaffold the fix:

> Refactor the `Product` class below to add robust data validation for
> its `price` and `quantity` attributes using Python's `@property`
> decorators and associated setter methods. Use a custom exception
> called `InvalidProductDataError` to handle validation failures (for
> example, a negative price, a negative quantity, or a non-numeric
> value), so the application never crashes with an unrelated error but
> instead raises this clear, meaningful exception at the point the bad
> value is assigned. Keep the rest of the `InventoryManager` class
> working exactly as before. Then explain your design choices,
> specifically how using `@property` setters together with a custom
> exception enforces Data Integrity and Encapsulation.
>
> ```python
> class Product:
>     """Represents a product with a name, price, and quantity."""
>     def __init__(self, name, price, quantity):
>         self.name = name
>         self.price = price
>         self.quantity = quantity
> ```

## Testing

The following test case was appended to `refactored_code.py` to
confirm the validation works:

```python
print("\n--- Testing Invalid Input ---")
try:
    manager.inventory[0].quantity = -5
except Exception as e:
    print(f"Test result: {e}")
```

Output:

```
--- Testing Invalid Input ---
Test result: Invalid quantity for 'Laptop': -5 cannot be negative.
```

## Analysis

Assigning `manager.inventory[0].quantity = -5` triggers the
`quantity.setter` on `Product`, which checks the incoming value before
ever storing it in the private `_quantity` attribute. Because `-5` is
negative, the setter raises `InvalidProductDataError` with a message
naming the product and the invalid value, instead of letting the
assignment succeed and corrupting the object's state.

This is superior to direct attribute assignment without validation in
three ways:

1. **Data integrity is enforced at the single point of entry.** Every
   assignment to `product.quantity` — whether from `__init__`,
   `InventoryManager.update_quantity`, or any future code — passes
   through the same setter, so there is exactly one place that can
   ever let bad data through, and exactly one place to fix if the
   validation rules change.
2. **Encapsulation is preserved.** Callers still write
   `product.quantity = -5`, the same syntax as a plain attribute; they
   don't need to know a validated setter exists underneath. The
   internal representation (`self._quantity`) is hidden, so the class
   is free to change how it stores or checks the value later without
   breaking any external code that uses the public `quantity`
   interface.
3. **Failures are explicit and specific.** A custom exception
   (`InvalidProductDataError`) with a descriptive message pinpoints
   exactly what went wrong and on which product, right at the moment
   the bad value was introduced — rather than the program continuing
   silently with corrupted state and failing later with a generic,
   hard-to-trace error (or no error at all, just wrong numbers in
   `calculate_total_value()`).
- [x] `initial_code.py` and `refactored_code.py` uploaded to this
  folder.
- [x] This `README.md`.
