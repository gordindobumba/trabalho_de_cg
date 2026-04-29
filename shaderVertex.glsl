#version 460

uniform mat4 modelMatrix;

layout(location = 0) in vec2 a_pos;
layout(location = 1) in vec3 a_cor;

out vec3 cor;

void main(){
    cor = a_cor;
    gl_Position = modelMatrix * vec4(a_pos, 0, 1);
}