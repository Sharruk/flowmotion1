from django.test import TestCase
from unittest.mock import patch
from habits.ai_utils import generate_notification_messages

class NotificationAITest(TestCase):
    @patch('requests.post')
    def test_generate_notification_messages(self, mock_post):
        # Mocking the Gemini API response
        mock_response = mock_post.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'candidates': [{
                'content': {
                    'parts': [{
                        'text': "PreReminder: Get ready for Water Plants!\nOnTime: Time to Water Plants now.\nOverdue: Don't forget to Water Plants."
                    }]
                }
            }]
        }

        messages = generate_notification_messages("Water Plants")
        
        self.assertIn('pre_reminder', messages)
        self.assertIn('on_time', messages)
        self.assertIn('overdue', messages)
        
        self.assertEqual(messages['pre_reminder'], "Get ready for Water Plants!")
        self.assertEqual(messages['on_time'], "Time to Water Plants now.")
        self.assertEqual(messages['overdue'], "Don't forget to Water Plants.")

    def test_fallback_messages(self):
        # Test fallback with no API key or failed call
        with patch('habits.ai_utils.GOOGLE_API_KEY', None):
            messages = generate_notification_messages("Exercise")
            self.assertEqual(messages['pre_reminder'], "Ready for Exercise? It starts in five minutes.")
