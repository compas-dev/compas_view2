from compas_view2.values import IntValue
from compas_view2.values import FloatValue
from compas_view2.values import StrValue
from compas_view2.values import ListValue
from compas_view2.values import DictValue
from compas_view2.values import BoolValue
from compas_view2.values import Settings


settings = Settings({
    "a": IntValue(1),
    "a2": IntValue(1, min=0, max=10),
    "a3": IntValue(1, options=[0, 1, 2, 3]),
    "b": FloatValue(0.005),
    "c": StrValue("some texts"),
    "d": ListValue([1, 2, 3], int),
    "e": DictValue({"a": 1}, int),
    "f": BoolValue(True),
})

print(settings)

print("Assigning new values to settings:")
print(settings["a"])
settings["a"] = 2
print(settings["a"])

print("\nAssigning wrong type:")
try:
    settings["b"] = "some_text"
except AssertionError as e:
    print(e)

print("\nAssigning value out of bounds")
try:
    settings["a2"] = 11
except AssertionError as e:
    print(e)

print("\nAssigning value out of options")
try:
    settings["a3"] = 4
except AssertionError as e:
    print(e)