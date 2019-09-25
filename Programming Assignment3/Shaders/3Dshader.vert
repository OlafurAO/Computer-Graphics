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
}