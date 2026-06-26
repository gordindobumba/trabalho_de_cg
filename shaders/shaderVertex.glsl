#version 460

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projMatrix;
uniform mat4 normalMatrix;
uniform vec3 objectColor;

layout(location = 0) in vec3 a_pos;
layout(location = 1) in vec3 a_normal;
layout(location = 2) in vec3 a_color;
layout(location = 3) in vec2 a_textura;

out vec3 pos;
out vec3 normal;
out vec3 cor;
out vec2 textCoord;

void main(){
    pos = vec3(modelMatrix * vec4(a_pos, 1.0));
    normal = mat3(normalMatrix) * a_normal;
    cor = objectColor;
    gl_Position = projMatrix * viewMatrix * modelMatrix * vec4(a_pos, 1);
}