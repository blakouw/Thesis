from Visualization_software.calculate_limb_lenghts import limb_lengths_new
from Visualization_software import calculate_transforms, generation_handlers
from Visualization_software.calculate_time import calculate_time
from Visualization_software.read_from_excel import data_len
from Visualization_software.const import file_path_csv, file_path_csv_normglob, file_path_csv_normlokal


def generate_x3d_code(objects_dict, czas, file_name):
    """
    Generuje kod X3D na podstawie słownika obiektów, czasu cyklu i nazwy pliku.
    :param objects_dict: Słownik zawierający etykiety obiektów i ich wartości.
    :param czas: Czas trwania cyklu w milisekundach.
    :param file_name: Nazwa pliku, do którego ma zostać zapisany kod X3D.
    """
    x3d_code = "#X3D V3.3 utf8\n\n"
    x3d_code += f"DEF Clock TimeSensor {{\n    cycleInterval {int(czas / 1000)}\n    loop TRUE\n}}\n\n"
    r = 0.01
    i = 0
    for label, value in objects_dict.items():
        i += 1
        h = limb_lengths_new[str(label)]
        key = generation_handlers.print_key(data_len)

        keyValuePos = generation_handlers.format_midpoints(value)
        keyValueRot = generation_handlers.format_euler(value)

        x3d_code += f"DEF obj{i} Transform {{\n"
        x3d_code += "    children [\n"
        x3d_code += "        Shape {\n"
        x3d_code += "            appearance Appearance {\n"
        x3d_code += "                material Material {\n"
        x3d_code += "                    diffuseColor 1 0 0\n"
        x3d_code += "                }\n"
        x3d_code += "            }\n"
        x3d_code += f"            geometry Cylinder {{\n"
        x3d_code += f"                height {h}\n"
        x3d_code += f"                radius {r}\n"
        x3d_code += "            }\n"
        x3d_code += "        }\n"
        x3d_code += "    ]\n"
        x3d_code += "    # Initial position and orientation will be set here\n"
        x3d_code += "}\n\n"

        x3d_code += f"DEF Position{i} PositionInterpolator {{\n"
        x3d_code += f"    {key}\n"
        x3d_code += f"    keyValue [{keyValuePos}]\n"
        x3d_code += "}\n\n"

        x3d_code += f"DEF Rotate{i} OrientationInterpolator {{\n"
        x3d_code += f"    {key}\n"
        x3d_code += f"    keyValue [{keyValueRot}]\n"
        x3d_code += "}\n\n"

        x3d_code += f"ROUTE Clock.fraction_changed TO Position{i}.set_fraction\n"
        x3d_code += f"ROUTE Clock.fraction_changed TO Rotate{i}.set_fraction\n\n"
        x3d_code += f"ROUTE Position{i}.value_changed TO obj{i}.set_translation\n"
        x3d_code += f"ROUTE Rotate{i}.value_changed TO obj{i}.set_rotation\n\n"

        x3d_code += '''
Background {
    skyColor 0.5 0.3 1
}
DEF Podloga Transform {
    translation 0 0 0
    children [
        Shape {
            appearance Appearance {
                material Material {
                    diffuseColor 0.4 0.3 0
                }
            }
            geometry Box {
                size 10 10 0.05
            }
        }
    ]
}
DEF Punkt0 Transform {
    children [
        Shape {
            appearance Appearance {
                material Material {
                    diffuseColor 1 1 1
                }
            }
            geometry Sphere {
                radius 0.08
            }
        }
    ]
}
'''
    with open(f"{file_name}.x3dv", "w") as file:
        file.write(x3d_code)


generate_x3d_code(calculate_transforms.limb_midpoints_quaternions, calculate_time(file_path_csv_normlokal), "../Model_visualization/linia_prosta_norm_lokal")
print(calculate_time(file_path_csv) / 100)
