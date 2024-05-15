import os
import smtplib
import markdown
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import Dict


def send_plan(lesson_subject: str, lesson_duration: int, lesson_plan: str, tutor_data: Dict[str, str],
              student_data: Dict[str, str], attachment_path: str) -> None:
    """
    Send an email containing the lesson plan for an upcoming English session.

    Args:
       lesson_subject (str): The topic of the English lesson.
       lesson_duration (int): The duration of the English lesson.
       lesson_plan (str): The detailed plan for the English lesson.
       tutor_data (Dict[str, str]): Information about the tutor.
       student_data (Dict[str, str]): Information about the student.
       attachment_path (str): Path to the file you want to attach.
    """
    # Email sender information
    sender = "bohdan1404@gmail.com"
    password = os.getenv('PASSWORD_EMAIL_APP')

    # Setting up SMTP server
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    # Markdown template for the lesson plan email
    markdown_plan_template = f"""\
    # English Lesson Plan for {student_data["Full Name"]}

    Dear {tutor_data["Full Name"]},

    Here is the lesson plan for the upcoming online English session with {student_data["Full Name"]}.

    #### Lesson Details:

    - **Lesson Topic:** {lesson_subject}
    - **Lesson Duration:** {lesson_duration} minutes.
    - **Student's Name:** {student_data["Full Name"]}
    - **Student's Email:** {student_data["Email"]}
    - **Level of English Proficiency:** {student_data["Level of English Proficiency"]}
    - **Learning Goals:** {student_data["Learning Goals"]}
    - **Areas of Difficulty:** {student_data["Areas of Difficulty"]}
    - **Areas of Interest:** {student_data["Areas of Interest"]}
    - **Strengths:** {student_data["Strengths"]}
    - **Preferred Learning Methodology:** {student_data["Preferred Learning Methodology"]}

    {lesson_plan}

    We believe that this lesson plan, tailored to student's needs and learning style, will facilitate a productive and enriching session.

    Thank you for your dedication to our students' growth and development. Should you have any questions or require further assistance, please feel free to reach out.

    Best regards,
    Your AI Assistant!\
    """

    markdown_plan_template = "\n".join(line.lstrip() for line in markdown_plan_template.split("\n"))

    try:
        # Logging in to the email server
        server.login(sender, password)

        # Creating the email message
        msg = MIMEMultipart()
        msg['Subject'] = f'English Lesson Plan for {student_data["Full Name"]}'
        msg.attach(MIMEText(markdown.markdown(markdown_plan_template), 'html'))

        # Attaching the file
        with open(attachment_path, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())

        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename= {os.path.basename(attachment_path)}')
        msg.attach(part)

        # Sending the email
        server.sendmail(sender, tutor_data["Email"], msg.as_string())
    except Exception as e:
        print(e)
