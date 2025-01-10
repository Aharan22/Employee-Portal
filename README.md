# Ontash Employee Portal

## Overview

The Employee Portal is a custom-built solution designed for Ontash employees. This platform leverages facial recognition technology for seamless employee login and admin verification during the registration process. Developed using the Dlib library, it aims to provide a secure, efficient, and modern approach to employee management. This repository is in active development and contributions are highly encouraged to enhance its functionality and usability.

## Features

- **Employee Login**: Utilizes face recognition to authenticate employees, ensuring secure and efficient access.
- **Admin Registration**: Admin users are required to verify their identity through face recognition before registering new employees.
- **Database Integration**: Stores employee details and face embeddings in a secure SQLite database.
- **Resource Organization**: Clearly structured files and directories to manage scripts, templates, and static assets effectively.

## Technologies Used
![Uploading dilibimage.png…]()

- **Python**: Core programming language.
- **Dlib**: Utilized for face detection and recognition, leveraging models such as:
  - `shape_predictor_68_face_landmarks.dat`: For facial landmark detection.
  - `dlib_face_recognition_resnet_model_v1.dat`: For face encoding and recognition.
- **Flask**: Lightweight web framework for building the portal.
- **SQLite**: Database for storing employee information.

## Directory Structure

```
.![directorystructure](https://github.com/user-attachments/assets/946a6642-5973-4d67-ba0c-14261059d477)

|-- instance
|-- known_faces
|-- static
|-- templates
|-- README.md
|-- app.py
|-- database.db
|-- dlib_face_recognition_resnet_model_v1.dat
|-- requirements.txt
|-- shape_predictor_68_face_landmarks.dat
```

- **instance**: Contains runtime-specific data.
- **known\_faces**: Stores known face encodings and images.
- **static**: Houses static files like CSS, JavaScript, and images.
- **templates**: Contains HTML templates for the portal interface.
- **app.py**: Main application file to run the Flask server.
- **database.db**: SQLite database storing employee and admin data.
- **dlib\_face\_recognition\_resnet\_model\_v1.dat**: Pre-trained Dlib model for face recognition.
- **shape\_predictor\_68\_face\_landmarks.dat**: Pre-trained Dlib model for facial landmarks.

## Getting Started

### Prerequisites

Ensure you have the following installed:

- Python 3.7 or above
- pip (Python package installer)

### Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_name>
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python app.py
   ```

The portal will be accessible at `http://127.0.0.1:5000/`.

## Usage

- **Login**: Employees can log in by presenting their face to the camera.
- **Registration**: Admins can add new employees by verifying their own identity and uploading necessary information.

## Known Issues

1. **Login Issues**: The application may fail to detect user faces during login. Even though some employees have been saved in the `known_faces` directory (including an admin image, `admin.jpg`), the script might not match the face encodings with the ones on the screen.
   ![issue1](https://github.com/user-attachments/assets/418cdd70-8032-46b8-8303-d6bea258296f)

   ![Login Page Issue](register_page.png)
![login_page](https://github.com/user-attachments/assets/9c9c471f-e1a7-481b-b33d-33f1ef9be23b)

2. **Registration Issues**: While the webcam activates during registration, the webcam feed does not display on the webpage. This might be related to:![register_page](https://github.com/user-attachments/assets/a3dbe01c-df4c-49a9-a480-d31b0cb96d2f)

   - Issues with the face encoding logic in the database.
   - Errors in the primary script (`app.py`) preventing proper encoding and matching.
   
   ![Registration Page Issue](login_page.png)
![issueregistration](https://github.com/user-attachments/assets/7fb2b3c0-1340-425e-bb9d-77d98385e3b8)

3. **HTML Template Loading**:
   - Some templates, like the registration page and the employee dashboard, fail to load.
   - Ensure templates are correctly referenced in `app.py` and located in the `templates` directory.
4. **CSS Styling**: The CSS file is not consistently applied to all pages. Debug template linking for better styling consistency.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes and push the branch.
4. Submit a pull request with a detailed description of your changes.

## Future Enhancements

- Integration with external APIs for extended functionality.
- Enhanced user interface and experience.
- Support for multiple database backends.
- Real-time notification systems.

## License

This project is open-source and available for contributions. Licensing details will be added in future updates.

## Acknowledgments

Special thanks to Ontash for providing the inspiration and resources to build this Employee Portal.

