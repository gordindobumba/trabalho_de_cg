#version 460

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projMatrix;

layout(location = 0) in vec3 a_pos;
layout(location = 1) in vec3 a_cor;
layout(location = 2) in vec3 a_normal;

out vec3 pos;
out vec3 normal;
out vec3 cor;

void main(){
    pos = a_pos;
    normal = a_normal;
    cor = a_cor;
    gl_Position = projMatrix * viewMatrix * modelMatrix * vec4(a_pos, 1);
}