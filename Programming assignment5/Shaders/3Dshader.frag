uniform vec4 u_light_diffuse;
uniform vec4 u_light_specular;

uniform vec4 u_material_diffuse;
uniform vec4 u_material_specular;
uniform float u_material_shininess;

varying vec4 v_normal;
varying vec4 v_s;
varying vec4 v_h;

varying vec4 v_color;

void main(void) {
    float lambert = max(dot(v_normal, v_s), 0);
    float phong = max(dot(v_normal, v_h), 0);

    gl_FragColor = u_light_diffuse * u_material_diffuse * lambert
	             + u_light_specular * u_material_specular * pow(phong, u_material_shininess);
}