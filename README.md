# TinyToes

## Overview
TinyToes is a comprehensive web platform designed to help parents understand and care for their babies using advanced AI technology. It offers features such as baby cry analysis, milestone tracking, expert consultations, and a nanny booking service to provide seamless support to parents.


## Technology Stack
- **Frontend:** HTML, CSS, Bootstrap, JavaScript
- **Backend:** Django
- **Database:** MySQL
- **AI Model:** TensorFlow (ResNet50 for cry analysis)

## Installation & Setup
### Prerequisites
Ensure you have the following installed:
- Python 3.8+
- Node.js & npm
- MySQL

### Backend Setup
```bash
# Clone the repository
git clone https://github.com/Rajendran2201/babycare.git
cd babycare

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt

# Run database migrations
python manage.py migrate

# Start the server
python manage.py runserver
```

## Contribution
We welcome contributions! Please follow these steps:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-name`).
3. Commit your changes and push to your branch.
4. Open a pull request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact
For any queries or support, reach out to:
📧 Email: rajendran.stech@gmail.com
