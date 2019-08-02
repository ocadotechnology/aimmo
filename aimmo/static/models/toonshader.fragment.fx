precision highp float;

// Lights
varying vec3 vPositionW;
varying vec3 vNormalW;
varying vec2 vUV;

// Refs
uniform sampler2D textureSampler;

void main(void) {
    float ToonThresholds[4];
    ToonThresholds[0] = 0.95;
    ToonThresholds[1] = 0.5;
    ToonThresholds[2] = 0.2;
    ToonThresholds[3] = 0.03;
    
    float ToonBrightnessLevels[5];
    ToonBrightnessLevels[0] = 1.0;
    ToonBrightnessLevels[1] = 0.8;
    ToonBrightnessLevels[2] = 0.6;
    ToonBrightnessLevels[3] = 0.5;
    ToonBrightnessLevels[4] = 0.4;
    
    vec3 vLightPosition = vec3(0,10,-10);
    
    // Light
    vec3 lightVectorW = normalize(vLightPosition - vPositionW);
    
    // diffuse
    float ndl = max(0., dot(vNormalW, lightVectorW));
    
    vec3 color = texture2D(textureSampler, vUV).rgb;
    
    if (ndl > ToonThresholds[0])
    {
        color *= ToonBrightnessLevels[0];
    }
    else if (ndl > ToonThresholds[1])
    {
        color *= ToonBrightnessLevels[1];
    }
    else if (ndl > ToonThresholds[2])
    {
        color *= ToonBrightnessLevels[2];
    }
    else if (ndl > ToonThresholds[3])
    {
        color *= ToonBrightnessLevels[3];
    }
    else
    {
        color *= ToonBrightnessLevels[4];
    }
    
    gl_FragColor = vec4(color, 1.);
}