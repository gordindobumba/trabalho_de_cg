#version 460

// uniform vec3 lightPos;
// uniform vec3 camPos;
// uniform vec3 lightColor;
// uniform int isShaded;

in vec3 cor;
in vec3 normal;
in vec3 pos;

out vec4 fragColor;

//vec3 lightning(){
    // vec3 l = normalize(lightPos - pos);
    // vec3 n = normalize(normal);
    // float dif = max(0, dot(l, n));

    // vec3 v = normalize(camPos - pos);
    // vec3 h = normalize(l + v);
    // float spec = pow(max(0, dot(h, n)), 64);

    // vec3 amb = 0.1 * cor * lightColor;

    // vec3 shading = amb + lightColor * cor * dif + lightColor * vec3(1, 1, 1) * spec;

    // return shading
//}

void main(){
    // vec3 c
    // if(isShaded == 1) c = lightning();
    // else c = cor;
    // fragColor = vec4(dif * c, 1.0);
    fragColor = vec4(cor, 1.0);
}