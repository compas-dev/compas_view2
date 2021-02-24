#version 130

attribute vec3 position;
attribute vec3 color;

uniform mat4 projection;
uniform mat4 viewworld;
uniform mat4 transform;

uniform bool is_selected;
uniform bool is_text;
uniform int text_size;
uniform float opacity;
uniform vec3 selection_color;

varying vec4 vertex_color;

void main()
{
    if (is_selected) {
        vertex_color = vec4(selection_color, opacity);
    }
    else {
        vertex_color = vec4(color, opacity);
    }

    if (is_text){
        gl_PointSize = text_size;
    }

    gl_Position = projection * viewworld * transform * vec4(position, 1.0);
}
