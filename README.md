# Educational Report Automation System

An intelligent automation platform for educational institutions that streamlines the creation and submission of student progress reports. The system combines web scraping, AI-powered report generation, and automated form filling to eliminate manual reporting tasks for teachers and administrators.

## Features

### Core Functionality
- **Automated Report Generation**: AI-powered creation of personalized student progress reports
- **Web Automation**: Seamless integration with Kids&Us educational platform
- **Batch Processing**: Handles multiple Excel files with hundreds of student records
- **Multi-Language Support**: Generates reports in Spanish with proper educational terminology
- **PDF Consolidation**: Combines all reports into professional PDF documents

### AI-Powered Report Creation
- **GPT-4/O3 Integration**: Uses advanced language models for natural, human-like report writing
- **Personalized Content**: Tailors each report to individual student performance and characteristics
- **Multi-Category Support**: Handles different course levels (Babies, Tweens, Teens, Ben&Brenda)
- **Historical Context**: Incorporates previous term data for comprehensive progress tracking

## Technology Stack

### Backend Technologies
- **Python 3.9+** - Core programming language
- **Flask** - Web application framework
- **Playwright** - Browser automation and web scraping
- **Pandas** - Data processing and Excel handling
- **ReportLab** - Professional PDF generation

### AI & Language Processing
- **OpenAI GPT-4/O3** - Advanced report generation
- **Structured Output Parsing** - JSON-formatted report validation
- **Pydantic Models** - Type-safe data validation

### Web Automation
- **Playwright Sync API** - Reliable browser automation
- **Form Automation** - Automated data entry and report submission
- **Session Management** - Persistent login and navigation states

## Architecture

```
Excel Upload Interface (Flask)
    ↓
Data Processing Pipeline (Pandas)
    ↓
Web Automation Engine (Playwright)
    ├── Login & Navigation
    ├── Student Data Extraction
    └── Historical Data Retrieval
    ↓
AI Report Generation (OpenAI)
    ├── Previous Term Context
    ├── Personalized Content Creation
    └── Multi-Category Processing
    ↓
Automated Report Submission
    ├── Form Field Mapping
    ├── Rating Selection
    └── Comment Input
    ↓
PDF Generation & Consolidation
```

## Installation

### Prerequisites
```bash
pip install flask pandas playwright python-dotenv pydantic openai reportlab
playwright install chromium
```

### Environment Setup
Create a `.env` file:
```env
OPENAI_API_KEY=your_openai_api_key
```

### Project Structure
```
project/
├── main.py                    # Flask application entry point
├── report_automation.py       # Playwright automation logic
├── report_generator.py        # AI report generation
├── templates/
│   └── upload.html           # File upload interface
├── reports/                  # Generated PDF outputs
└── data/                     # Processing workspace
```

## Usage

### Starting the Application
```bash
python main.py
```
Access the web interface at `http://localhost:8080`

### Processing Workflow
1. **Upload Excel Files**: Upload one or more Excel files containing student data
2. **Provide Credentials**: Enter Kids&Us platform login credentials  
3. **Automated Processing**: System processes each student automatically
4. **Report Generation**: AI creates personalized reports for each student
5. **Platform Submission**: Reports are automatically submitted to the platform
6. **PDF Export**: Consolidated PDF report is generated for download

## Key Components

### 1. Report Automation Engine (`ReportAutomation`)
```python
class ReportAutomation:
    def login(self)                           # Platform authentication
    def navigate_to_reports(self, ...)        # Navigate to student groups
    def extract_scores(self, ...)             # Extract historical data
    def enter_report(self, ...)               # Submit generated reports
```

**Key Features:**
- Persistent browser sessions with Chromium
- Intelligent navigation between schools, courses, and groups
- Robust error handling and retry logic
- Historical data extraction for context

### 2. AI Report Generator (`generar_reporte`)
```python
def generar_reporte(student, anterior_trimestre):
    # Generates comprehensive student reports using GPT-4/O3
    # Returns structured JSON with ratings and comments
```

**Report Sections:**
- **Motivación y Participación**: Student engagement and participation
- **Aprendizaje**: Learning progress and skill development  
- **Comportamiento**: Classroom behavior assessment
- **Evaluaciones**: Oral and written test performance
- **Evaluación General**: Overall progress summary

### 3. Data Processing Pipeline
- **Excel Parsing**: Handles multiple sheets and formats
- **Column Mapping**: Flexible field mapping system
- **Data Sanitization**: Cleans and validates input data
- **Duplicate Prevention**: Tracks processed students

### 4. Multi-Category Support
- **Standard Courses**: Babies, Kids courses with basic assessment
- **Advanced Courses**: Tweens/Teens with comprehensive evaluation
- **Ben&Brenda**: Specialized curriculum handling
- **Custom Adaptations**: Category-specific report formatting

## Advanced Features

### Intelligent Student Navigation
- **Pattern Matching**: Finds students across multiple groups
- **Flexible Search**: Handles name variations and scheduling changes
- **Context Preservation**: Maintains navigation state between students

### Historical Context Integration
```python
def extract_scores(self, student_name, term, category):
    # Extracts comprehensive previous term data
    # Returns structured context for AI processing
```

### Professional Report Generation
- **Natural Language Processing**: Human-like report writing
- **Educational Standards**: Aligned with Spanish educational practices
- **Quality Assurance**: Built-in error checking and validation
- **Consistency Maintenance**: Standardized tone and format

### Automated Quality Control
```python
errores_comunes = '''
- Incomplete reports despite available information
- Inconsistent gender references
- Excessive or inappropriate vocabulary
- Missing required translations
- Contradictory assessments
'''
```

## Report Structure

### Standard Report Format
```json
{
    "Motivación_y_Participación": {
        "Rating": "Excellent/Very good/Good/Satisfactory",
        "Comment": "Detailed 300-600 character assessment"
    },
    "Aprendizaje": {
        "Rating": "Excellent/Very good/Good/Satisfactory", 
        "Comment": "Learning progress and skills acquired"
    },
    "Comportamiento": {
        "Rating": "Excellent/Very good/Good/Satisfactory",
        "Comment": "Classroom behavior assessment"
    },
    "Nota_de_prueba_oral": "Standardized oral assessment",
    "Nota_de_prueba_escrita": "Written test evaluation",
    "Evaluación_general": "Overall progress summary"
}
```

### Tweens/Teens Extended Format
Additional sections for advanced courses:
- **Trabajo**: Work habits and study skills
- **Rendimiento**: Performance across all skills
- **My_Way**: App-based learning assessment
- **Deberes**: Homework completion and quality
- **Nota_Global**: Overall grade justification

## Performance Optimization

### Batch Processing
- **Concurrent Processing**: Handles multiple students simultaneously
- **Session Reuse**: Maintains browser sessions across students
- **Smart Navigation**: Minimizes page loads and transitions

### Error Handling
- **Retry Logic**: Automatic recovery from temporary failures
- **Graceful Degradation**: Continues processing despite individual errors
- **Comprehensive Logging**: Detailed error tracking and debugging

### Resource Management
- **Memory Optimization**: Efficient handling of large datasets
- **Browser Management**: Proper cleanup and resource release
- **File Processing**: Streaming Excel processing for large files

## Security Considerations

### Authentication
- **Secure Credential Handling**: Environment-based credential storage
- **Session Security**: Proper session management and cleanup
- **Data Privacy**: Local processing with minimal external exposure

### Data Protection
- **Student Privacy**: Compliant with educational data protection standards
- **Audit Trail**: Complete processing history for accountability
- **Access Control**: Web interface with secure file handling

## Quality Assurance

### Report Quality Standards
- **Length Requirements**: 300-600 characters per section
- **Language Standards**: Proper Spanish educational terminology
- **Consistency Checks**: Automated validation of report coherence
- **Personalization**: Individual student name integration

### Content Guidelines
- **Positive Reinforcement**: Constructive feedback approach
- **Age-Appropriate Language**: Suitable for different age groups
- **Cultural Sensitivity**: Spanish educational context awareness
- **Professional Tone**: Maintains educational standards

## Monitoring & Maintenance

### System Monitoring
- **Processing Logs**: Detailed operation tracking
- **Error Reporting**: Comprehensive error categorization
- **Performance Metrics**: Processing speed and success rates

### Regular Maintenance
- **Database Cleanup**: Processed student record management
- **Browser Updates**: Playwright and Chromium maintenance
- **AI Model Updates**: OpenAI API version management

## Future Enhancements

### Planned Features
- **Multi-Language Support**: Additional language options
- **Advanced Analytics**: Student progress trend analysis
- **Integration APIs**: Direct platform integrations
- **Mobile Interface**: Responsive design improvements

### Scalability Improvements
- **Cloud Deployment**: Distributed processing capabilities
- **Database Integration**: Persistent data storage
- **API Development**: Third-party integration support
- **Performance Optimization**: Enhanced processing speeds

## Support & Documentation

### User Support
- **Processing Guides**: Step-by-step usage instructions
- **Troubleshooting**: Common issue resolution
- **Best Practices**: Optimal workflow recommendations
- **Training Materials**: User education resources

## License

This system is designed for educational institution use with appropriate student data privacy and security considerations. All rights reserved.

## Technical Support

For technical issues, configuration assistance, or feature requests, please refer to the system documentation or contact the development team.
