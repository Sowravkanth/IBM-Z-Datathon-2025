import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Any
import os
import logging

class EmailNotifications:
    """Email notification system for job alerts and reminders"""
    
    def __init__(self):
        # In a production environment, these would be set up properly
        # For now, we'll create a framework that can be extended
        self.smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.environ.get('SMTP_PORT', '587'))
        self.sender_email = os.environ.get('SENDER_EMAIL', 'noreply@careersight.ai')
        self.sender_password = os.environ.get('SENDER_PASSWORD', '')
    
    def send_job_alert(self, recipient_email: str, jobs: List[Dict[str, Any]]) -> bool:
        """Send job alert email with matching jobs"""
        
        subject = "CareerSight AI: New Job Matches Found!"
        
        # Create HTML email body
        html_content = self._create_job_alert_html(jobs)
        
        return self._send_email(recipient_email, subject, html_content)
    
    def send_roadmap_reminder(self, recipient_email: str, milestone: str, week: int) -> bool:
        """Send learning roadmap milestone reminder"""
        
        subject = f"CareerSight AI: Week {week} Learning Milestone Reminder"
        
        html_content = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2 style="color: #1f77b4;">Learning Roadmap Reminder</h2>
                    <p>Hello!</p>
                    <p>This is a friendly reminder about your Week {week} learning milestone:</p>
                    <div style="background-color: #f0f2f6; padding: 15px; border-radius: 5px; margin: 20px 0;">
                        <p><strong>{milestone}</strong></p>
                    </div>
                    <p>Keep up the great work on your learning journey!</p>
                    <p>Best regards,<br>CareerSight AI Team</p>
                </div>
            </body>
        </html>
        """
        
        return self._send_email(recipient_email, subject, html_content)
    
    def send_application_update(self, recipient_email: str, job_title: str, company: str, status: str) -> bool:
        """Send application status update notification"""
        
        subject = f"CareerSight AI: Application Update - {job_title}"
        
        html_content = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2 style="color: #1f77b4;">Application Status Update</h2>
                    <p>Your application status has been updated:</p>
                    <div style="background-color: #f0f2f6; padding: 15px; border-radius: 5px; margin: 20px 0;">
                        <p><strong>Position:</strong> {job_title}</p>
                        <p><strong>Company:</strong> {company}</p>
                        <p><strong>Status:</strong> {status}</p>
                    </div>
                    <p>Keep track of all your applications in CareerSight AI!</p>
                    <p>Best regards,<br>CareerSight AI Team</p>
                </div>
            </body>
        </html>
        """
        
        return self._send_email(recipient_email, subject, html_content)
    
    def _create_job_alert_html(self, jobs: List[Dict[str, Any]]) -> str:
        """Create HTML content for job alert email"""
        
        jobs_html = ""
        for job in jobs[:5]:  # Limit to top 5 jobs
            jobs_html += f"""
            <div style="border-left: 4px solid #1f77b4; padding-left: 15px; margin: 20px 0;">
                <h3 style="color: #1f77b4; margin: 5px 0;">{job.get('job_title', 'N/A')}</h3>
                <p style="margin: 5px 0;"><strong>{job.get('company', 'N/A')}</strong> • {job.get('location', 'N/A')}</p>
                <p style="margin: 5px 0;">💰 ₹{job.get('salary_min', 0):.1f}L - ₹{job.get('salary_max', 0):.1f}L</p>
                <p style="margin: 5px 0; color: #666;">Match: {job.get('compatibility_score', 0)*100:.0f}%</p>
            </div>
            """
        
        html_content = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2 style="color: #1f77b4;">🎯 New Job Matches Found!</h2>
                    <p>We found {len(jobs)} new jobs matching your profile:</p>
                    {jobs_html}
                    <p style="margin-top: 30px;">
                        <a href="https://your-app-url.com" style="background-color: #1f77b4; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block;">
                            View All Matches
                        </a>
                    </p>
                    <p style="margin-top: 30px; color: #666; font-size: 12px;">
                        You're receiving this email because you enabled job alerts in CareerSight AI.
                    </p>
                </div>
            </body>
        </html>
        """
        
        return html_content
    
    def _send_email(self, recipient_email: str, subject: str, html_content: str) -> bool:
        """Send email using SMTP"""
        
        # For demonstration purposes, we'll just log the email
        # In production, this would use actual SMTP
        
        try:
            # Check if SMTP credentials are configured
            if not self.sender_password:
                logging.info(f"Email notification (not sent - no SMTP configured):")
                logging.info(f"To: {recipient_email}")
                logging.info(f"Subject: {subject}")
                logging.info(f"Content: {html_content[:200]}...")
                return False
            
            # Create message
            message = MIMEMultipart('alternative')
            message['Subject'] = subject
            message['From'] = self.sender_email
            message['To'] = recipient_email
            
            # Add HTML content
            html_part = MIMEText(html_content, 'html')
            message.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)
            
            logging.info(f"Email sent successfully to {recipient_email}")
            return True
            
        except Exception as e:
            logging.error(f"Error sending email: {e}")
            return False
    
    def schedule_notification(self, notification_type: str, recipient_email: str, data: Dict[str, Any]) -> bool:
        """Schedule a notification to be sent later"""
        
        # In a production environment, this would add to a job queue (e.g., Celery, Redis Queue)
        # For now, we'll just log it
        
        logging.info(f"Notification scheduled:")
        logging.info(f"Type: {notification_type}")
        logging.info(f"Recipient: {recipient_email}")
        logging.info(f"Data: {data}")
        
        return True
