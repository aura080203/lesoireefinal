import subprocess
import os


def create_virtualenv_and_install_dependencies(subproject_path):
    # Capture the current directory path
    current_dir = os.getcwd()

    # Change directory to the subproject directory
    os.chdir(subproject_path)

    # Create virtual environment
    subprocess.run(["python", "-m", "venv", "env_" + os.path.basename(subproject_path)])

    # Return to parent folder
    os.chdir(current_dir)

    # Print success statement
    print(
        f"'env_{os.path.basename(subproject_path)}' ENV created successfully: {subproject_path}"
    )


if __name__ == "__main__":
    print("_____Starting Execution_____")
    current_dir = os.getcwd()
    print("Parent directory:", current_dir)
    # Change to the directory of the main project
    main_project_path = "./"
    os.chdir(main_project_path)

    # Create virtual environment and install dependencies for subproject 1
    create_virtualenv_and_install_dependencies(
        os.path.join(main_project_path, "backend_api")
    )

    # Create virtual environment and install dependencies for subproject 2
    create_virtualenv_and_install_dependencies(
        os.path.join(main_project_path, "admin_portal")
    )
