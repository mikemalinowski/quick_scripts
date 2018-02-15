"""
By Mike Malinowski
www.twisted.space
"""
import pymel.core as pm


def worldspaceShapeReparent(shape, transform, cleanup=False):
    """
    Moves the given shape to the given transform node
    ensuring that the shape retains its worldspace point
    positions regardless of transform differences.
    
    :param shape: The shape (or transform containing a shape node)
    :type shape: pm.nt.NurbsCurve (or pm.nt.Transform)
    
    :param transform: The node you want the shape to be parented under
    :type transform: pm.nt.Transform
    
    :param cleanup: If true, the transform hosting the shape prior to the
        reparenting will be removed
    :type cleanup: bool
    
    return None
    """
    
    # -- If the shape is a transform, pull out
    # -- the first shape from it
    if isinstance(shape, pm.nt.Transform):
        shape = shape.getShape()
    
    # -- If we have no valid shape, raise an error
    if not shape:
        raise Exception(
            'You must pass a NurbsCurve or a transform which contains a NurbsCurve'
        )
    
    # -- Store the shapes original transform
    former_host = shape.getParent()
    
    # -- Store the worldspace positions of the curve
    worldspace_positions = list()

    for idx in range(shape.numCVs()):
        worldspace_positions.append(
            shape.getCV(idx, space='world'),
        )
    
    # -- Now we have stored the positions, we can reparent the
    # -- shape node
    shape.setParent(
        transform, 
        shape=True, 
        relative=True,
    )
    
    # -- If we need to perform any cleanup, we do that now
    if cleanup:
        pm.delete(former_host)
    
    # -- Re-apply the worldspace positions of the cvs
    for idx in range(shape.numCVs()):
        shape.setCV(
            idx,
            worldspace_positions[idx],
            space='world',
        )


# -- Get the user selection and call the function
if __name__ == '__main__':
    worldspaceShapeReparent(
        pm.selected()[0],
        pm.selected()[1],
        cleanup=True,
    )
    