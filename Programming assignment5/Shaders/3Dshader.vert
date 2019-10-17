attribute vec3 a_position;
attribute vec3 a_normal;

uniform mat4 u_model_matrix;
uniform mat4 u_view_matrix;
uniform mat4 u_projection_matrix;

uniform vec4 u_light_position;
uniform vec4 u_light_diffuse;
uniform vec4 u_material_diffuse;

varying vec4 v_color;

void main(void) {
	vec4 position = vec4(a_position.x, a_position.y, a_position.z, 1.0);
	vec4 normal = vec4(a_normal.x, a_normal.y, a_normal.z, 0.0);

	position = u_model_matrix * position;
	normal = normalize(u_model_matrix * normal);

	// Global coordinates
	vec4 s = normalize(u_light_position - position);
	float lambert = max(dot(normal, s), 0);
	v_color = lambert * u_color;


	position = u_projection_matrix * (u_view_matrix * position);

	gl_Position = position;
}