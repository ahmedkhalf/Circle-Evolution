import moderngl
import numpy as np

from pathlib import Path


class CircleRenderer:
    def __init__(self, size: tuple[int, int]) -> None:
        # Initialize ModernGL context
        ctx = moderngl.create_standalone_context()

        self.gpu_name = ctx.info['GL_RENDERER']

        current_folder = Path(__file__).parent.resolve()
        with open(current_folder / "base.vert", 'r') as f:
            vertex_shader = f.read()
        with open(current_folder / "circles.frag", 'r') as f:
            fragment_shader = f.read()

        # Compile the shaders
        self._prog = ctx.program(
            vertex_shader=vertex_shader,
            fragment_shader=fragment_shader,
        )

        # Set the image width and height as a vec2 uniform
        self._width, self._height = size
        self._prog['iResolution'] = size

        # Create a fullscreen quad VAO
        quad_vertices = np.array([-1.0, -1.0, 1.0, -1.0, -1.0, 1.0, 1.0, 1.0], dtype='f4')
        vbo = ctx.buffer(quad_vertices)
        self._vao = ctx.simple_vertex_array(self._prog, vbo, 'in_vert')

        # Create a framebuffer to render into
        self._fbo = ctx.framebuffer(
            color_attachments=[ctx.texture(size, 4)],
        )

        # Use the framebuffer for rendering
        self._fbo.use()

        # Clear the framebuffer
        ctx.clear()

    def render(self, count, pos, radii, colors):
        self._prog['circleCount'] = count
        self._prog['pos'] = pos
        self._prog['radii'] = radii
        self._prog['colors'] = colors

        # Render the fullscreen quad
        self._vao.render(moderngl.TRIANGLE_STRIP)

        # Read the rendered image from the framebuffer
        pixels = self._fbo.read(components=3, dtype='f1')

        # Convert the image to a numpy array
        image_data = np.frombuffer(pixels, dtype=np.uint8)
        image_data = image_data.reshape((self._height, self._width, 3))

        return image_data
