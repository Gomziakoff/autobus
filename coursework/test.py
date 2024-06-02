from haversine import haversine, Unit

cords = (52.09556749,23.75711132)
bus_stop = (52.094,23.756)

dist = haversine(cords,bus_stop, unit=Unit.METERS)
print(dist)