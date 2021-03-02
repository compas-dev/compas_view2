#version 120

varying vec3 vertex_color;
varying vec3 ec_pos;

uniform float opacity;
uniform bool is_instance_mask;
uniform bool lighted;
uniform vec3 instance_color;

void main()
{   
    vec3 light_pos = vec3(0, 0, 0);
    if (is_instance_mask) {
        gl_FragColor = vec4(instance_color, 1);
    }
    else{
        if (lighted){
            vec3 ec_normal = normalize(cross(dFdx(ec_pos), dFdy(ec_pos)));
            vec3 L = normalize(-ec_pos); 
            gl_FragColor = vec4(vertex_color * dot(ec_normal, L), opacity);
        }else{
            gl_FragColor = vec4(vertex_color, opacity);
        }
    }

   
}
