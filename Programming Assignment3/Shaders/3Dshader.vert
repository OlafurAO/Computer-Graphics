/*
attribute vec3 vec_position;
attribute vec3 vec_normal;

uniform mat4 vec_model_matrix;
uniform mat4 vec_view_matrix;
uniform mat4 vec_projection_matrix;

uniform vec4 u_color;
varying vec4 v_color;

void main(void) {
    vec4 position = vec4(vec_position.x, vec_position.y, vec_position.z, 1.0) * vec_model_matrix;
    vec4 normal = vec4(vec_normal.x, vec_normal.y, vec_normal.z, 0.0) * vec_model_matrix;

    float light_factor_1 = max(dot(normalize(normal), normalize(vec4(1, 2, 3, 0))), 0.0);
    float light_factor_2 = max(dot(normalize(normal), normalize(vec4(-3, -2, -1, 0))), 0.0);
    v_color = (light_factor_1 + light_factor_2) * vec4(u_color);

    position = vec_projection_matrix * (vec_view_matrix * position);
    gl_Position = position;
}*/

attribute vec3 a_position;
attribute vec3 a_normal;

uniform mat4 u_model_matrix;
uniform mat4 u_view_matrix;
uniform mat4 u_projection_matrix;

uniform vec4 u_color;
varying vec4 v_color;

void main(void)
{
	vec4 position = vec4(a_position.x, a_position.y, a_position.z, 1.0);
	vec4 normal = vec4(a_normal.x, a_normal.y, a_normal.z, 0.0);

	position = u_model_matrix * position;
	normal = u_model_matrix * normal;

	// Global coordinates
	float light_factor_1 = max(dot(normalize(normal), normalize(vec4(1, 2, 3, 0))), 0.0);
	float light_factor_2 = max(dot(normalize(normal), normalize(vec4(-3, -2, -1, 0))), 0.0);
	v_color = (light_factor_1 + light_factor_2) * vec4(u_color);

	position = u_projection_matrix * (u_view_matrix * position);

	gl_Position = position;
}