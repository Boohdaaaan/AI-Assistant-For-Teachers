# AI Assistant For English Teacher

Welcome to the AI Assistant For English Teacher! This project is designed to assist English teachers in preparing for their lessons efficiently and effectively. By leveraging the power of LLMs, this program helps create detailed lesson plans and practical exercises tailored to the specific needs of students.


## Models
* __Lesson Plan Generator__: This model generates a detailed lesson plan based on: lesson subject, student data and lesson duration.
 
* __Exercise Generator__: This model creates practical exercises tailored to the lesson plan. The exercises can be used during the lesson or assigned as homework.

Both models are based on OpenAI's GPT-4, ensuring high-quality and contextually appropriate content generation.

## Usage

### Requirements
* Python 3.x

### Setup
* Clone repository
```bash
  git clone https://github.com/Boohdaaaan/AI-Assistant-For-Teachers.git
```

* Move to project folder
```bash
  cd AI-Assistant-For-Teachers
```

* Set environment variable in the .env file (OpenAI API key)
```bash
  echo "OPENAI_API_KEY=your-api-key-goes-here" > .env
```

* Start the project
```bash
  python src/main.py  
```


## Acknowledgments
Special thanks to the developers and communities behind the libraries and tools used in this project for their valuable contributions.
