import requests
import logging
from backend.app.core.config import settings
import os

logger = logging.getLogger(__name__)

class NotificationService:
    def __init__(self):
        # Allow an optional webhook URL in .env, e.g., SLACK_WEBHOOK_URL
        self.webhook_url = os.getenv("SLACK_WEBHOOK_URL")

    def send_alert(self, task_id: int, component: str, analysis: dict, recommendation: str, decision: str):
        """
        Sends an enterprise-grade alert regarding market intelligence.
        """
        cheapest = (analysis or {}).get("cheapest") or {}
        price_anomaly = (analysis or {}).get("price_anomaly", False)
        
        # We only want to trigger HIGH PRIORITY alerts for action-oriented decisions or anomalies
        is_high_priority = decision in ["MARKETING_BLITZ", "ADJUST_PRICE"] or price_anomaly
        priority_tag = "🚨 [HIGH PRIORITY]" if is_high_priority else "ℹ️ [INFO]"
        
        message = (
            f"{priority_tag} **Market Intelligence Alert: {component}**\n"
            f"Task ID: #{task_id}\n\n"
            f"**Cheapest Competitor Found:**\n"
            f"- Product: {cheapest.get('name', 'N/A')}\n"
            f"- Price: {cheapest.get('price', 'N/A')}\n\n"
            f"**AI Strategy Decision:** `{decision}`\n"
            f"**Recommendation:** {recommendation}\n"
        )
        
        if self.webhook_url:
            try:
                response = requests.post(self.webhook_url, json={"text": message})
                if response.status_code == 200:
                    logger.info(f"Notification sent successfully to webhook for Task {task_id}")
                else:
                    logger.warning(f"Webhook returned status {response.status_code}")
            except Exception as e:
                logger.error(f"Failed to send webhook notification: {e}")
        
        # Always print a beautiful simulated log for the Hackathon Demo
        print("\n" + "="*60)
        print("🔔 ENTERPRISE NOTIFICATION SYSTEM TRIGGERED")
        print("="*60)
        print(message)
        print("="*60 + "\n")

# Singleton instance
notifier = NotificationService()
