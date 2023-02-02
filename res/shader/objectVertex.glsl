#version 330 core

uniform mat4 transformationMatrix;
uniform mat4 projectionMatrix;
uniform mat4 viewMatrix;

layout (location = 0) in vec3 vertexPos;
layout (location = 1) in vec3 vertexNormal;
layout (location = 2) in vec3 vertexColor;

out float shade;
out vec3 color;

void main() {
  vec3 lightVec = normalize(vec3(-0.5, -2, 1));
  vec4 tnormal = transformationMatrix * vec4(vertexNormal,0.0);

  shade = dot(lightVec, tnormal.xyz)/2+0.5;
  color = vertexColor;

  vec4 worldPos = transformationMatrix * vec4(vertexPos, 1.0);
  vec4 relPos = viewMatrix * worldPos;
  vec4 screenPos = projectionMatrix*relPos;
  gl_Position = screenPos;
}