#version 330

in vec3 vertex_color;
out vec4 out_color;

void main()
{   
    out_color = vec4(vertex_color, 1);

}
