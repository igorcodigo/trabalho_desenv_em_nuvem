import os
import resend
from dotenv import load_dotenv
import base64
from django.conf import settings

# Load environment variables
load_dotenv()

# Get the current directory to facilitate file path connections
current_directory = os.path.dirname(os.path.abspath(__file__))

# Get API key from .env file
resend.api_key = os.getenv('RESEND_API_KEY')
TESTE_EMAIL_TO_EMAIL = os.getenv('TESTE_EMAIL_TO_EMAIL')
TESTE_EMAIL_FROM_EMAIL = os.getenv('TESTE_EMAIL_FROM_EMAIL')

def validate_api_key():
    """Verifies if the API key is properly configured."""
    if not resend.api_key:
        raise ValueError("Error: RESEND_API_KEY not found in .env file")

def load_email_template(template_name):
    """
    Loads an HTML template file.
    
    Args:
        template_name (str): Template file name without extension
        
    Returns:
        str: Content of the HTML file
    """
    template_path = os.path.join(current_directory, 'templates', f'{template_name}.html')
    
    with open(template_path, 'r', encoding='utf-8') as file:
        return file.read()

def customize_template(template_content, replacements):
    """
    Replaces placeholders in the template with actual values.
    
    Args:
        template_content (str): HTML template content
        replacements (dict): Dictionary with values to replace
        
    Returns:
        str: Customized HTML template
    """
    content = template_content
    for placeholder, value in replacements.items():
        content = content.replace(f'{{{{ {placeholder} }}}}', value)
    return content

def send_email_resend(subject, html_content, to_email, from_email=TESTE_EMAIL_FROM_EMAIL, attachments=None):
    """
    Sends an email using Resend API with optional attachments.
    
    Args:
        to_email (str): Recipient email
        subject (str): Email subject
        html_content (str): HTML email content
        from_email (str): Sender email
        attachments (list, optional): List of dictionaries with file details to attach
                                     Example: [{"filename": "file.pdf", "path": "/path/to/file.pdf"}]
        
    Returns:
        dict: Resend API response
    """
    try:
        email_data = {
            "from": from_email,
            "to": [to_email] if isinstance(to_email, str) else to_email,
            "subject": subject,
            "html": html_content
        }
        
        if attachments:
            email_data["attachments"] = []
            for attachment in attachments:
                if "path" in attachment and os.path.exists(attachment["path"]):
                    with open(attachment["path"], "rb") as file:
                        file_content = file.read()
                        file_base64 = base64.b64encode(file_content).decode("utf-8")
                        
                        filename = attachment.get("filename", os.path.basename(attachment["path"]))
                        
                        email_data["attachments"].append({
                            "filename": filename,
                            "content": file_base64
                        })
        
        response = resend.Emails.send(email_data)
        return response
    except Exception as e:
        raise Exception(f"Error sending email: {e}")

def send_welcome_email(email, name):
    """
    Sends a welcome email to a newly registered user.
    """
    validate_api_key()
    template_content = load_email_template('welcome_template')
    html_content = customize_template(template_content, {'name': name})
    
    return send_email_resend(
        to_email=email,
        subject="Bem-vindo(a) à nossa plataforma!",
        html_content=html_content
    )

def send_email_changed_notification(email, name):
    """
    Sends an email notification when user's email has changed.
    """
    validate_api_key()
    template_content = load_email_template('email_changed_template')
    html_content = customize_template(template_content, {'name': name})
    
    return send_email_resend(
        to_email=email,
        subject="Seu e-mail foi alterado!",
        html_content=html_content
    )

def send_password_changed_email(email, name):
    """
    Sends an email notification when user's password has changed.
    """
    validate_api_key()
    template_content = load_email_template('password_changed_notification_template')
    html_content = customize_template(template_content, {'name': name})
    
    return send_email_resend(
        to_email=email,
        subject="Sua senha foi alterada com sucesso!",
        html_content=html_content
    )
