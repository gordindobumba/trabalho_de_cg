#version 460

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projMatrix;

layout(location = 0) in vec3 a_pos;
layout(location = 1) in vec3 a_cor;

out vec3 cor;

void main(){
    cor = a_cor;
    gl_Position = projMatrix * viewMatrix * modelMatrix * vec4(a_pos, 1);
}