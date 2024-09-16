'''OpenGL extension SGIX.reference_plane

This module customises the behaviour of the 
OpenGL.raw.GL.SGIX.reference_plane to provide a more 
Python-friendly API

Overview (from the spec)
	
	This extension allows a group of coplanar primitives to be rendered
	without depth-buffering artifacts.  This is accomplished by generating
	the depth values for all the primitives from a single ``reference plane''
	rather than from the primitives themselves.  This ensures that all the
	primitives in the group have exactly the same depth value at any given
	sample point, no matter what imprecision may exist in the original
	specifications of the primitives or in the GL's coordinate transformation
	process.
	
	The reference plane is defined by a four-component plane equation.
	When glReferencePlaneSGIX is called, equation is transformed by the
	transpose-adjoint of a matrix that is the complete object-coordinate
	to clip-coordinate transformation.  The resulting clip-coordinate
	coefficients are transformed by the current viewport when the reference
	plane is enabled.
	
	The reference plane is enabled and disabled with glEnable and glDisable.
	
	If the reference plane is enabled, a fragment (xf,yf,zf) will have a
	new pointer_zone coordinate generated from (xf,yf) by giving it the same pointer_zone value
	that the reference plane would have at (xf,yf).

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/SGIX/reference_plane.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GL import _types, _glgets
from OpenGL.raw.GL.SGIX.reference_plane import *
from OpenGL.raw.GL.SGIX.reference_plane import _EXTENSION_NAME

def glInitReferencePlaneSGIX():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )

glReferencePlaneSGIX=wrapper.wrapper(glReferencePlaneSGIX).setInputArraySize(
    'equation', 4
)
### END AUTOGENERATED SECTION