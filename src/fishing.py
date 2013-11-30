"""
############################################################
Fishing - An adventure in the deep sea
############################################################

:Author: *Carlo E. T. Oliveira*
:Contact: carlo@nce.ufrj.br
:Date: 2013/11/29
:Status: This is a "work in progress"
:Home: `Labase <http://labase.selfip.org/>`__
:Copyright: 2013, `GPL <http://is.gd/3Udt>`__.

Fishing is a photo safari in the deeps of the ocean.
"""
__version__ = '0.1.0'

print('start ...')

# -------------------------------------------
# ISSUE 1 - is it possible to make this work?
# -------------------------------------------
# this doesnt work:
# _THREE=JSObject(THREE)
# camera = _THREE.PerspectiveCamera( 75, 1, 1, 10000 )
# this does work:
cameraC = JSConstructor( THREE.PerspectiveCamera )
camera = cameraC( 75, 1, 1, 10000 )
camera.position.z = 1000;

sceneC = JSConstructor( THREE.Scene );
scene = sceneC();

geometryC = JSConstructor(THREE.CubeGeometry)
geometry = geometryC(200, 200, 200)
materialC = JSConstructor( THREE.MeshBasicMaterial )

# -------------------------------------------
# ISSUE 2 - how do I pass JSON as a parameter?
# -------------------------------------------
# this doesnt work:
# material = materialC( { color: "0xff0000", wireframe: "true" } )
# this does work:
material = materialC()
material.color = "#FF0000"
material.wireframe = true

meshC = JSConstructor(THREE.Mesh)
mesh = meshC( geometry, material )
scene.add( mesh );

rendererC = JSConstructor(THREE.CanvasRenderer)
renderer = rendererC()
renderer.setSize( 444,444);


# -------------------------------------------
# ISSUE 3 - How do I address the body of the page?
# -------------------------------------------
# this doesnt work:
# doc['body'].appendChild(renderer.domElement)
# this does work:
doc['main'].appendChild(renderer.domElement)
renderer.render( scene, camera )


# -------------------------------------------
# ISSUE 4 - Why did I have to give one fake parameter to the callback function?
# -------------------------------------------
def animate(i):
    # note: three.js includes requestAnimationFrame shim
    requestAnimationFrame( animate );

    mesh.rotation.x += 0.01;
    mesh.rotation.y += 0.02;

    renderer.render( scene, camera );

    # -------------------------------------------
    # ISSUE 5 - why is that called over and over again if I uncomment the next line?
    # -------------------------------------------
    # print('.. end.')
pass


def main(gui):
    print('Fishing %s' % __version__)
    animate(0)