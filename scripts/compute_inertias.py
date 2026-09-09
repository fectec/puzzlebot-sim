"""
Computes mass and inertia tensors from STL meshes using trimesh.
"""

import os
import trimesh

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        ".."
    )
)

ROS2_WS_DIR = os.path.join(PROJECT_ROOT, "ros2_ws")
DESCRIPTION_DIR = os.path.join(
    ROS2_WS_DIR,
    "src",
    "puzzlebot_description"
)

# STL folders to search
MESH_FOLDERS = [
    os.path.join(DESCRIPTION_DIR, "models"),
    os.path.join(DESCRIPTION_DIR, "meshes"),
]

# Output file
OUTPUT_FILE = os.path.join(
    DESCRIPTION_DIR,
    "inertias_urdf.txt"
)

# Scale applied to meshes

# 0.001 -> STL exported in millimeters
# 1.0   -> STL already in meters

MESH_SCALE = 1.0

# Material densities (kg/m^3)
DENSITIES = {
    "PLA":      1240,
    "ACRYLIC":  1180,
    "ALUMINUM": 2700,
    "STEEL":    7850,
}

# -----------------------------------------------------------------------------
# OBJECT CONFIGURATION
#
# Key:
#   STL filename without ".stl"
#
# Options:
#
#   material:
#       Material used for density
#
#   xacro_name:
#       Prefix used in xacro properties
#
#   skip:
#       Ignore this STL
#
#   real_mass:
#       Override geometry mass
#
#   extra_mass:
#       Additional attached mass not in the STL
# -----------------------------------------------------------------------------

OBJECTS = {

    # -------------------------------------------------------------------------
    # Pallet
    # -------------------------------------------------------------------------

    "pallet": {
        "material":   "PLA",
        "xacro_name": "pallet",
    },

    # -------------------------------------------------------------------------
    # Chassis
    # -------------------------------------------------------------------------

    "chassis": {

        "material":   "ACRYLIC",
        "xacro_name": "base_link",

        "extra_mass": {

            "battery":      0.300,
            "electronics":  0.150,
            "caster":       0.060,
        }
    },

    # -------------------------------------------------------------------------
    # Wheels
    # -------------------------------------------------------------------------

    "wheel_left": {
        "material":   "ACRYLIC",
        "xacro_name": "wheel_link",
    },

    "wheel_right": {
        "material": "ACRYLIC",
        "skip": True,
    },

    # -------------------------------------------------------------------------
    # Forklift
    # -------------------------------------------------------------------------

    "forklift_train": {
        "material":   "PLA",
        "xacro_name": "forks_link",
    },

    # -------------------------------------------------------------------------
    # Camera
    # -------------------------------------------------------------------------

    "camera": {

        "material":   "PLA",
        "xacro_name": "camera_link",

        # Real measured mass
        "real_mass": 0.003,
    },

    # -------------------------------------------------------------------------
    # LiDAR
    # -------------------------------------------------------------------------

    "laser_link": {

        "material":   "PLA",
        "xacro_name": "laser",

        # Real measured mass
        "real_mass": 0.170,
    },
}

# Default material if object is not listed above
DEFAULT_MATERIAL = "PLA"

# =============================================================================
# FUNCTIONS
# =============================================================================

def load_mesh(path):
    """
    Loads and repairs a mesh.
    """

    mesh = trimesh.load_mesh(path, process=True)

    if mesh.is_empty:
        raise ValueError("Mesh is empty")

    # Apply unit conversion
    mesh.apply_scale(MESH_SCALE)

    # If mesh is not watertight,
    # convex hull is more stable
    if not mesh.is_watertight:
        mesh = mesh.convex_hull

    # Fix inverted normals
    if mesh.volume < 0:
        mesh.invert()

    if mesh.volume <= 0:
        raise ValueError(
            f"Invalid mesh volume: {mesh.volume}"
        )

    return mesh

def compute_inertia(mesh, density):
    """
    Computes:
    - mass
    - inertia tensor
    """

    mass = mesh.volume * density

    # trimesh assumes density = 1 internally
    inertia = mesh.moment_inertia * density

    ixx = inertia[0][0]
    iyy = inertia[1][1]
    izz = inertia[2][2]

    return mass, ixx, iyy, izz

def scale_inertia(ixx, iyy, izz, old_mass, new_mass):
    """
    Rescales inertia tensor when mass changes.
    """

    ratio = new_mass / old_mass

    return (
        ixx * ratio,
        iyy * ratio,
        izz * ratio
    )

def create_xacro_block(name, mass, ixx, iyy, izz):
    """
    Generates xacro properties.
    """

    return f"""
<xacro:property name="{name}_m"   value="{mass:.9f}"/>
<xacro:property name="{name}_ixx" value="{ixx:.9e}"/>
<xacro:property name="{name}_iyy" value="{iyy:.9e}"/>
<xacro:property name="{name}_izz" value="{izz:.9e}"/>
""".strip()

# =============================================================================
# MAIN
# =============================================================================

def main():

    # -------------------------------------------------------------------------
    # Find all STL files
    # -------------------------------------------------------------------------

    stl_files = []

    for folder in MESH_FOLDERS:

        if not os.path.exists(folder):
            continue

        for file in os.listdir(folder):

            if file.endswith(".stl"):

                full_path = os.path.join(folder, file)

                stl_files.append(full_path)

    if not stl_files:

        print("No STL files found.")
        return

    results = []
    errors = []

    print("\n==================================================")
    print("COMPUTING INERTIAS")
    print("==================================================\n")

    # -------------------------------------------------------------------------
    # Process each STL
    # -------------------------------------------------------------------------

    for path in stl_files:

        filename = os.path.basename(path)

        stl_name = os.path.splitext(filename)[0]

        config = OBJECTS.get(stl_name, {})

        # Skip ignored meshes
        if config.get("skip", False):

            print(f"Skipping: {stl_name}")

            continue

        material = config.get(
            "material",
            DEFAULT_MATERIAL
        )

        density = DENSITIES[material]

        xacro_name = config.get(
            "xacro_name",
            stl_name
        )

        real_mass = config.get("real_mass")

        extra_mass_dict = config.get(
            "extra_mass",
            {}
        )

        extra_mass = sum(
            extra_mass_dict.values()
        )

        try:

            print(f"Processing: {filename}")

            mesh = load_mesh(path)

            # Print approximate mesh size
            extents = mesh.bounding_box.extents

            print(
                f"  Size : "
                f"{extents[0]:.3f} x "
                f"{extents[1]:.3f} x "
                f"{extents[2]:.3f} m"
            )

            geo_mass, ixx, iyy, izz = compute_inertia(
                mesh,
                density
            )

            final_mass = geo_mass

            notes = []

            # -----------------------------------------------------------------
            # Replace geometry mass with real mass
            # -----------------------------------------------------------------

            if real_mass is not None:

                ixx, iyy, izz = scale_inertia(
                    ixx,
                    iyy,
                    izz,
                    geo_mass,
                    real_mass
                )

                final_mass = real_mass

                notes.append(
                    f"real mass override = {real_mass:.3f} kg"
                )

            # -----------------------------------------------------------------
            # Add attached masses
            # -----------------------------------------------------------------

            if extra_mass > 0:

                total_mass = final_mass + extra_mass

                ixx, iyy, izz = scale_inertia(
                    ixx,
                    iyy,
                    izz,
                    final_mass,
                    total_mass
                )

                final_mass = total_mass

                notes.append(
                    f"extra attached mass = {extra_mass:.3f} kg"
                )

            # -----------------------------------------------------------------
            # Terminal output
            # -----------------------------------------------------------------

            print(f"  Material : {material}")
            print(f"  Mass     : {final_mass:.6f} kg")
            print(f"  IXX      : {ixx:.9e}")
            print(f"  IYY      : {iyy:.9e}")
            print(f"  IZZ      : {izz:.9e}")

            results.append({

                "name": xacro_name,
                "mass": final_mass,

                "ixx": ixx,
                "iyy": iyy,
                "izz": izz,

                "material": material,
                "notes": notes,
            })

            print()

        except Exception as e:

            errors.append((stl_name, str(e)))

            print(f"ERROR: {stl_name}")
            print(e)
            print()

    # =========================================================================
    # WRITE OUTPUT FILE
    # =========================================================================

    with open(OUTPUT_FILE, "w") as f:

        f.write(
            "==================================================\n"
        )

        f.write(
            "AUTO-GENERATED URDF INERTIAS\n"
        )

        f.write(
            "==================================================\n\n"
        )

        # ---------------------------------------------------------------------
        # Xacro properties
        # ---------------------------------------------------------------------

        f.write("<!-- XACRO PROPERTIES -->\n\n")

        for r in results:

            f.write(
                f"<!-- {r['name']} [{r['material']}] -->\n"
            )

            if r["notes"]:

                for note in r["notes"]:

                    f.write(
                        f"<!-- {note} -->\n"
                    )

            f.write(
                create_xacro_block(
                    r["name"],
                    r["mass"],
                    r["ixx"],
                    r["iyy"],
                    r["izz"]
                )
            )

            f.write("\n\n")

        # ---------------------------------------------------------------------
        # Plain summary
        # ---------------------------------------------------------------------

        f.write("\n\nPLAIN SUMMARY\n")
        f.write("--------------------------------------------------\n\n")

        for r in results:

            f.write(f"{r['name']}\n")

            f.write(
                f"material : {r['material']}\n"
            )

            f.write(
                f"mass     : {r['mass']:.6f} kg\n"
            )

            f.write(
                f"ixx      : {r['ixx']:.9e}\n"
            )

            f.write(
                f"iyy      : {r['iyy']:.9e}\n"
            )

            f.write(
                f"izz      : {r['izz']:.9e}\n"
            )

            if r["notes"]:

                f.write(
                    f"notes    : {' | '.join(r['notes'])}\n"
                )

            f.write("\n")

        # ---------------------------------------------------------------------
        # Errors
        # ---------------------------------------------------------------------

        if errors:

            f.write("\nERRORS\n")
            f.write("--------------------------------------------------\n")

            for name, msg in errors:

                f.write(f"{name}: {msg}\n")

    # =========================================================================
    # Final terminal output
    # =========================================================================

    print("==================================================")
    print("DONE")
    print("==================================================\n")

    print(f"Output file:\n{OUTPUT_FILE}")

    if errors:

        print(f"\nErrors found: {len(errors)}")


if __name__ == "__main__":
    main()