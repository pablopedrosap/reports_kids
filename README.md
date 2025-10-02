# Student Report Automation System

An automated system for generating personalized student progress reports for English language learning programs. The system integrates with web-based classroom management platforms to extract student data and generate comprehensive, AI-powered educational assessments.

## Features

- **Automated Report Generation**: Uses OpenAI's GPT models to create personalized, detailed student reports in Spanish
- **Web Scraping Integration**: Automatically extracts student performance data from online classroom platforms
- **Multi-Category Support**: Handles different age groups and course levels (Babies, Tweens, Teens, etc.)
- **Batch Processing**: Processes multiple students and generates consolidated PDF reports
- **Customizable Templates**: Different report structures for various course categories
- **Quality Assurance**: Built-in validation to ensure reports meet educational standards

## Technology Stack

- **Backend**: Python 3.x, Flask
- **AI/ML**: OpenAI API (GPT-4o, o4-mini)
- **Web Automation**: Selenium WebDriver
- **PDF Generation**: ReportLab
- **Data Processing**: Pandas, NumPy
- **Frontend**: HTML templates

## Project Structure

```
├── main.py                     # Flask application entry point
├── report_generator.py         # AI-powered report generation logic
├── report_automation.py        # Web scraping and automation
├── templates/                  # HTML templates for web interface
├── reports/                    # Generated PDF reports output
├── requirements.txt            # Python dependencies
└── Dockerfile                  # Container configuration
```

## Setup Instructions

### Prerequisites

- Python 3.8+
- Chrome/Chromium browser (for Selenium)
- OpenAI API key

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd reports_kids
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root:
```bash
OPENAI_API_KEY=your_api_key_here
```

5. Configure credentials for the classroom platform in your `.env` file.

### Running the Application

**Development mode:**
```bash
python main.py
```

The application will be available at `http://localhost:8080`

**Docker deployment:**
```bash
docker build -t report-automation .
docker run -p 8080:8080 --env-file .env report-automation
```

## Usage

1. Access the web interface at `http://localhost:8080`
2. Enter credentials for the classroom management system
3. Upload Excel files containing student data
4. The system will:
   - Process each student's performance data
   - Generate personalized reports using AI
   - Create a consolidated PDF with all reports
5. Download the generated reports from the `reports/` directory

## Report Categories

- **Babies & Toddlers**: Focus on engagement and comprehension indicators
- **Kids Courses**: Comprehensive reports covering motivation, learning, behavior, homework, and tests
- **Tweens & Teens**: Advanced reports including written/oral assessments and skills analysis

## Data Format

Input Excel files should contain the following columns:

| Column Name | Description | Example |
|------------|-------------|---------|
| Centro | School name | "Center Name" |
| Curso | Course level | "Course 1", "Tweens 2" |
| Nombre grupo | Group schedule | "Monday 16:00 - 17:00" |
| Profesora | Teacher name | "Teacher Name" |
| Nombre alumno | Student name | "Student Name" |
| Motivación y participación | Participation score (1-4) | "3" |
| Aprendizaje | Learning score (1-4) | "4" |
| Comportamiento | Behavior score (1-4) | "4" |
| Deberes | Homework notes | "Always completes" |
| Actividad favorita | Favorite activity | "Role-playing games" |
| Frases aprendidas | Learned phrases (English/Spanish) | "I like cats. / Me gustan los gatos." |
| Nota oral | Oral test score | "3" |
| Nota escrita | Written test score (if applicable) | "4" |
| term | Term number | 1, 2, or 3 |

**Note**: Different course categories may require different columns. Tweens/Teens courses include additional fields for work habits and performance.

## Security Notes

- Never commit `.env` files or files containing API keys
- Ensure sensitive student data is handled in compliance with privacy regulations
- The system includes automatic tracking of processed students to prevent duplicates

## Development

### Adding New Report Templates

Modify `report_generator.py` and define new Pydantic models for different report structures.

### Customizing AI Prompts

Edit the prompt templates in `generar_reporte()` and `generar_reporte_tweens()` functions to adjust report generation behavior.

## Architecture Overview

```
┌─────────────┐
│   Flask     │  Web interface for file uploads
│   Server    │
└──────┬──────┘
       │
       ├──────> Excel Parser (Pandas)
       │        Reads student data from uploaded files
       │
       ├──────> Report Generator (OpenAI GPT)
       │        AI-powered personalized report creation
       │
       ├──────> Web Automation (Playwright)
       │        Navigates classroom platform and submits reports
       │
       └──────> PDF Generator (ReportLab)
                Creates consolidated reports
```

## Real-World Deployment

This system has been successfully deployed across more than 5 English language learning centers in Spain, demonstrating:

- **Time Savings**: Reduces report writing from ~10 min/student to seconds
- **Consistency**: Ensures all reports meet educational standards
- **Personalization**: Each report is unique and tailored to the student
- **Quality**: AI-powered content is reviewed and refined through validation

## Limitations & Considerations

- Requires valid credentials for the classroom management system
- OpenAI API usage incurs costs based on usage
- Web scraping may be affected by platform UI changes
- Suitable for batch processing but not real-time operations

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is for educational and demonstration purposes. Not licensed for commercial use.

## Contact

For questions about this project or collaboration opportunities, please open an issue on GitHub.
