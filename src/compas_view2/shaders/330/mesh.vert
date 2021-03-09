#version 330

in vec3 position;
in vec3 color;


out vec3 vertex_color;

uniform mat4 projection;
uniform mat4 viewworld;

void main()
{   
    vertex_color = color;
    gl_Position = projection * viewworld * vec4(position, 1.0);
}
