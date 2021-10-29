#version 120

attribute vec3 position;
attribute vec3 direction;

uniform mat4 projection;
uniform mat4 viewworld;
uniform mat4 transform;

varying vec2 dir_norm;

void main()
{
    vec4 start_position = projection * viewworld * transform * vec4(position, 1.0);
    vec4 end_position = projection * viewworld * transform * vec4(position + direction, 1.0);
    vec2 dir = end_position.xy - start_position.xy;
    gl_PointSize = length(dir) * 20;
    dir_norm = dir / length(dir);
    gl_Position = start_position;
}