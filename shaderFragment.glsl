#version 460

// uniform vec3 lightPos;

in vec3 cor;
in vec3 normal;
in vec3 pos;

out vec4 fragColor;

//float lightning(){
    // vec3 l = normalize(lightPos - pos);
    // vec3 n = normalize(normal);
    // float dif = max(0, dot(l, n));
    // return dif;
//}

void main(){
    // float dif = lightning();
    // fragColor = vec4(dif * color, 1.0);
    fragColor = vec4(cor, 1.0);
}