#version 130

varying vec4 vertex_color;
uniform bool is_instance_mask;
uniform vec3 instance_color;
uniform bool is_text;
uniform sampler2D tex;

void main()
{
    if (is_instance_mask) {
        gl_FragColor = vec4(instance_color, 1);
    }
    else {
        
        gl_FragColor = vertex_color;
        
    }
    if (is_text){
        gl_FragColor = vec4(0, 0, 0, texture(tex, gl_PointCoord).r);
    }
}
