#version 460

in vec3 cor;

out vec4 fragColor;

void main(){
    fragColor = vec4(cor, 1.0);
}