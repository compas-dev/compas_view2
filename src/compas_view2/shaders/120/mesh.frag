#version 130

varying vec4 vertex_color;
uniform bool is_instance_mask;
uniform vec3 instance_color;
uniform bool is_text;
uniform sampler2D tex;
uniform int text_num;
uniform vec3 text_color;


void main()
{
    if (is_text){
        vec2 xy = gl_PointCoord;
        xy.y -= 0.5;
        xy.y *= text_num;
        if (xy.y > 0 || xy.y < -0.5) {
            discard;
        }
        float a = texture(tex, xy).r;
        gl_FragColor = vec4(text_color, a);
        if (a <= 0){
            discard;
        }
    } else {
        if (is_instance_mask) {
            gl_FragColor = vec4(instance_color, 1);
        }
        else {
            gl_FragColor = vertex_color;
        }
    }
}
