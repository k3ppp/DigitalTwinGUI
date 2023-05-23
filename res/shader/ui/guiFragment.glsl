#version 430 core

uniform sampler2D uTextures[%max_textures%];

// layout (std430, binding = 0) buffer internalPos {
//   vec4 TMAT[];
// };

layout (std430, binding = 0) buffer textureParams {
  int textureIds[];
};

in vec4 fColor;
in vec2 fTexCoords;
flat in uint fUiId;
flat in uint fRId;

layout (location = 0) out vec4 color;
layout (location = 1) out uvec3 picking;

void main() {
	if(fColor.a <= 0)discard;

	if(textureIds[fRId] > -0.5){
		color = fColor * texture(uTextures[textureIds[fRId]], fTexCoords);
	}else{
		color = fColor;
	}
	if(color.a <= 0)discard;
	picking = uvec3(fUiId+1,fUiId,gl_PrimitiveID);
}