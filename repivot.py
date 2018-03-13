"""
This is a simple re-pivoting tool which allows you to select an
object you want to animate, and an object you want to animate it
from.

It will map all the motion of the object onto the new pivot object
and allow you to manipulate the object from that pivot. You can then
keep running this to change the pivot as and hwen you need.

By Mike Malinowski
www.twisted.space
"""
import pymel.core as pm

# -- Assume a selection order. The first object is the object
# -- we want to drive, the second object is the object we want
# -- to use as a new pivot point
driven = pm.selected()[0]
driver = pm.selected()[1]

# -- We need to map the motion of the soon-to-be driven
# -- object onto our driver
cns = pm.parentConstraint(
    driven,
    driver,
    maintainOffset=True,
)
pm.bakeResults(
    driver,
    time=[
        pm.playbackOptions(q=True, min=True),
        pm.playbackOptions(q=True, max=True),
    ],
    simulation=True,
)

# -- Now remove the constraint, and ensure there are no
# -- constraints on the soon-to-be driven object
pm.delete(cns)

constraints = list()
for child in driven.getChildren():
    if isinstance(child, pm.nt.Constraint):
        constraints.append(child)

pm.delete(constraints)

# -- Now we can constrain the driven to our new driver and
# -- we should get the same result, but we can manipulate
# -- it from our new space
pm.parentConstraint(
    driver,
    driven,
    maintainOffset=True,
)
