#version 460

uniform vec3 lightPos;
uniform vec3 camPos;
uniform vec3 lightColor;
uniform int isLight;
in vec2 textCoord;

uniform sampler2D texturaCor;
uniform sampler2D texturaNormal;
uniform sampler2D texturaRugosa;

uniform int ativarTextura;

in vec3 cor;
in vec3 normal;
in vec3 pos;

out vec4 fragColor;

vec3 lightning(vec3 cor, vec3 normais, float rugosidade){
    vec3 l = normalize(lightPos - pos);
    vec3 n = normalize(normal);
    float dif = max(0.0, dot(l, n));

    vec3 v = normalize(camPos - pos);
    vec3 h = normalize(l + v);

    float e = mix(64, 2, rugosidade);
    float spec = pow(max(0.0, dot(h, n)), e);

    vec3 amb = 0.4 * cor * lightColor;
    vec3 shading = amb + lightColor * cor * dif + lightColor * vec3(1, 1, 1) * spec;

    return shading;
}

void main(){
    vec3 corOg = cor;
    vec3 normalOg = normal;
    float rugosidade = 0.5;

    if(isLight == 1){
        fragColor = vec4(cor, 1.0);
    }
    else{
        if(ativarTextura == 1){
            corOg = texture(texturaCor, textCoord).rgb;
            normalOg = texture(texturaNormal, textCoord).rgb * 2.0 - 1.0;
            rugosidade = texture(texturaRugosa, textCoord).r;
        }
        vec3 c = lightning(corOg, normalOg, rugosidade);
        fragColor = vec4(c * cor, 1.0);
    }
}