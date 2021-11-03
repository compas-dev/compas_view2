#version 120

attribute vec3 position;
attribute vec3 direction;
attribute vec3 color;

uniform mat4 projection;
uniform mat4 viewworld;
uniform mat4 transform;
uniform float aspect;

varying vec3 vcolor;
varying vec2 dir_norm;

void main()
{
    vec4 start_position = projection * viewworld * transform * vec4(position, 1.0);
    vec4 end_position = projection * viewworld * transform * vec4(position + direction, 1.0);
    vec2 dir = end_position.xy - start_position.xy;
    gl_PointSize = 100;
    dir_norm = normalize(dir);
    gl_Position = start_position;
    vcolor = color;
}