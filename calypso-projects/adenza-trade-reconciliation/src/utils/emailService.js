const nodemailer = require('nodemailer');
const logger = require('./logger');

class EmailService {
  async send(emailData, smtpConfig) {
    try {
      const transporter = nodemailer.createTransport({
        host: smtpConfig.host,
        port: smtpConfig.port,
        secure: smtpConfig.secure,
        auth: {
          user: smtpConfig.user,
          pass: smtpConfig.password
        }
      });

      const info = await transporter.sendMail({
        from: emailData.from,
        to: emailData.to,
        subject: emailData.subject,
        text: emailData.text,
        html: emailData.html,
        attachments: emailData.attachments || []
      });

      logger.info(`Email sent: ${info.messageId}`);
      return info;
    } catch (error) {
      logger.error('Error sending email', error);
      throw error;
    }
  }
}

module.exports = new EmailService();

