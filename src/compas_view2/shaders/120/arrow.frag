#version 120


uniform sampler2D tex;
uniform int text_num;
uniform vec3 text_color;
varying vec2 dir_norm;


float DistToLine(vec2 pt1, vec2 pt2, vec2 testPt)
{
  vec2 lineDir = pt2 - pt1;
  vec2 perpDir = vec2(lineDir.y, -lineDir.x);
  vec2 dirToPt1 = pt1 - testPt;
  return abs(dot(normalize(perpDir), dirToPt1));
}

void main()
{   
    vec2 xy = gl_PointCoord;
    // xy.y -= 0.5;
    // xy.y *= text_num;
    // if (xy.y > 0 || xy.y < -0.5) {
    //     discard;
    // }
    // float a = texture2D(tex, xy).r;
    // gl_FragColor = vec4(text_color, a);
    // if (a <= 0){
    //     discard;
    // }

    float dis = DistToLine(vec2(0.5, 0.5), (vec2(0.5, 0.5) + (dir_norm / 2)), xy);

    if (dis > 0.1) {
        discard;
    }

    gl_FragColor = vec4(1.0, 0.0, 0.0, 1.0);
}
