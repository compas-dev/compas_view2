#version 120

varying vec3 vertex_color;
varying vec3 ec_pos;

uniform float opacity;
uniform float object_opacity;
uniform bool is_lighted;
uniform bool is_selected;
uniform vec3 selection_color;

void main()
{   
    vec3 color = vertex_color;
    if (is_selected) {
        color = selection_color;
    }

    vec3 light_pos = vec3(0, 0, 0);
    if (is_lighted){
        vec3 ec_normal = normalize(cross(dFdx(ec_pos), dFdy(ec_pos)));
        vec3 L = normalize(-ec_pos); 
        gl_FragColor = vec4(color * dot(ec_normal, L), opacity * object_opacity);
    }else{
        gl_FragColor = vec4(color, opacity * object_opacity);
    }
}
