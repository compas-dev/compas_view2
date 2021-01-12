#version 120

varying vec4 vertex_color;
uniform bool is_instance_mask;
uniform vec3 instance_color;

void main()
{
    if (is_instance_mask) {
        gl_FragColor = vec4(instance_color, 1);
    }
    else {
        gl_FragColor = vertex_color;
    }
}
