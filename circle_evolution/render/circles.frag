#version 400

vec4 circle(vec2 uv, vec2 pos, float rad, vec4 color)
{
    float d = length(pos - uv) - rad;
    float t = clamp(d, 0.0, color.a);
    return vec4(color.xyz, color.a - t);
}

uniform int circleCount;
uniform vec2 pos[256];
uniform float radii[256];
uniform vec4 colors[256];

out vec4 fragColor;
in vec2 fragCoord;
uniform vec2 iResolution;

void main()
{
    vec2 uv = fragCoord.xy * iResolution;

    vec4 dest = vec4(0, 0, 0, 1); // RGB values

    for (int i = 0; i < circleCount; i++)
    {
        vec4 circ = circle(uv, pos[i], radii[i], colors[i]);
        dest = mix(dest, circ, circ.a);
    }

    fragColor = dest;
}
