#!/usr/bin/env python3
"""
Email sender for YouTube Monitor reports
Supports Gmail and generic SMTP
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from dotenv import load_dotenv

# Load environment
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(env_path)


class EmailSender:
    """Send email reports via SMTP."""

    def __init__(self):
        # Support both naming conventions
        self.smtp_host = os.getenv('SMTP_HOST') or os.getenv('EMAIL_SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT') or os.getenv('EMAIL_SMTP_PORT', '587'))
        self.smtp_user = os.getenv('SMTP_USER') or os.getenv('EMAIL_FROM')
        self.smtp_password = os.getenv('SMTP_PASSWORD') or os.getenv('EMAIL_PASSWORD')
        self.from_email = os.getenv('EMAIL_FROM', self.smtp_user)
        self.to_email = os.getenv('EMAIL_TO', self.smtp_user)

        if not self.smtp_user or not self.smtp_password:
            raise ValueError(
                "SMTP credentials not found in .env file.\n"
                "Add: EMAIL_FROM=your_email@gmail.com\n"
                "     EMAIL_PASSWORD=your_app_password\n"
                "     EMAIL_TO=your_email@gmail.com"
            )

    def send_report(self, report_path, subject=None):
        """Send the daily report via email."""

        # Read report content
        with open(report_path) as f:
            report_content = f.read()

        # Default subject
        if not subject:
            from datetime import datetime
            subject = f"AI YouTube Daily Report - {datetime.now().strftime('%B %d, %Y')}"

        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = self.from_email
        msg['To'] = self.to_email

        # Convert markdown to HTML (basic conversion)
        html_content = self.markdown_to_html(report_content)

        # Attach both plain text and HTML versions
        text_part = MIMEText(report_content, 'plain')
        html_part = MIMEText(html_content, 'html')

        msg.attach(text_part)
        msg.attach(html_part)

        # Send email
        try:
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)

            print(f"✅ Email sent to {self.to_email}")
            return True

        except Exception as e:
            print(f"❌ Error sending email: {e}")
            return False

    def markdown_to_html(self, markdown_content):
        """Convert markdown to basic HTML for email."""
        html = "<html><body style='font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto;'>"

        lines = markdown_content.split('\n')
        in_list = False

        for line in lines:
            line = line.strip()

            if not line:
                if in_list:
                    html += "</ul>"
                    in_list = False
                html += "<br>"
                continue

            # Headers
            if line.startswith('# '):
                html += f"<h1 style='color: #2c3e50;'>{line[2:]}</h1>"
            elif line.startswith('## '):
                html += f"<h2 style='color: #34495e; border-bottom: 2px solid #3498db; padding-bottom: 5px;'>{line[3:]}</h2>"
            elif line.startswith('### '):
                html += f"<h3 style='color: #7f8c8d;'>{line[4:]}</h3>"

            # Bold
            elif line.startswith('**'):
                html += f"<p style='margin: 5px 0;'><strong>{line.replace('**', '')}</strong></p>"

            # Lists
            elif line.startswith('- '):
                if not in_list:
                    html += "<ul style='margin: 10px 0;'>"
                    in_list = True
                html += f"<li style='margin: 5px 0;'>{line[2:]}</li>"

            # Links (simplified)
            elif '[Watch Video]' in line or '📹' in line:
                html += f"<p style='margin: 10px 0; padding: 10px; background-color: #f8f9fa; border-left: 4px solid #3498db;'>{line}</p>"

            # Blockquotes
            elif line.startswith('>'):
                html += f"<blockquote style='margin: 10px 0; padding: 10px; background-color: #ecf0f1; border-left: 4px solid #95a5a6; font-style: italic;'>{line[1:].strip()}</blockquote>"

            # Horizontal rule
            elif line == '---':
                html += "<hr style='border: none; border-top: 2px solid #bdc3c7; margin: 20px 0;'>"

            # Regular paragraph
            else:
                html += f"<p style='margin: 5px 0;'>{line}</p>"

        if in_list:
            html += "</ul>"

        html += "</body></html>"
        return html


def main():
    """Test email sending."""
    import argparse

    parser = argparse.ArgumentParser(description='Send YouTube report via email')
    parser.add_argument('report_path', help='Path to report markdown file')
    parser.add_argument('--subject', help='Email subject (optional)')

    args = parser.parse_args()

    sender = EmailSender()
    sender.send_report(args.report_path, args.subject)


if __name__ == '__main__':
    main()
