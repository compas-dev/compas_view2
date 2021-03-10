#version 330

layout(location = 0) in vec3 position;
layout(location = 1) in vec3 color;


out vec3 vertex_color;

uniform mat4 projection;
uniform mat4 viewworld;

void main()
{   
    vertex_color = color;
    gl_Position = projection * viewworld * vec4(position, 1.0);
}
