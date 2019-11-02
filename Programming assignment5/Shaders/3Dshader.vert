attribute vec3 a_position;
attribute vec3 a_normal;
attribute vec2 a_uv;

uniform mat4 u_model_matrix;
uniform mat4 u_view_matrix;
uniform mat4 u_projection_matrix;

uniform vec4 u_eye_position;

uniform vec4 u_light_position;
uniform vec4 u_light_position_2;

varying vec4 v_normal;
varying vec4 v_s;
varying vec4 v_s2;

varying vec4 v_h;
varying vec4 v_h2;

varying vec2 v_uv;

void main(void) {
	vec4 position = vec4(a_position.x, a_position.y, a_position.z, 1.0);
	vec4 normal = vec4(a_normal.x, a_normal.y, a_normal.z, 0.0);

	// UV coords send into per-pixel use
	v_uv = a_uv;

	position = u_model_matrix * position;
	v_normal = normalize(u_model_matrix * normal);

	// Global coordinates
	v_s = normalize(u_light_position - position);
    v_s2 = normalize(u_light_position_2 - position);

	vec4 v = normalize(u_eye_position - position);
	v_h = normalize(v_s + v);
    v_h2 = normalize(v_s2 + v);

	position = u_projection_matrix * (u_view_matrix * position);

	gl_Position = position;
}