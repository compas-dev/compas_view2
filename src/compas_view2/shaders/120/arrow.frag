#version 120

varying vec3 vcolor;
varying vec2 dir_norm;
uniform float aspect;


float DistToLine(vec2 pt1, vec2 pt2, vec2 testPt)
{
  vec2 lineDir = pt2 - pt1;
  vec2 perpDir = vec2(lineDir.y, -lineDir.x);
  vec2 dirToPt1 = pt1 - testPt;
  return abs(dot(normalize(perpDir), dirToPt1));
}

float DistToPt(vec2 pt, vec2 testPt)
{
  return length(pt - testPt);
}

void main()
{   
    vec2 xy = gl_PointCoord;
    
    vec2 dir = vec2(dir_norm.x * aspect, -dir_norm.y);
    dir = normalize(dir);

    float dis = dot(xy - vec2(0.5, 0.5), dir);
    float angle = acos(dot(dir, normalize(xy - vec2(0.5, 0.5)))); 
    if (dis > 0.25 || angle > 0.3) {
        discard;
    }

    gl_FragColor = vec4(vcolor, 1.0);
}
