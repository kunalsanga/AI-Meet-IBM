"""
Meeting Summarizer Utility Module

This module provides advanced summarization and analysis capabilities for meeting transcripts,
including prompt engineering, post-processing, and structured output formatting.
"""

import re
import json
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class MeetingSummarizer:
    """Advanced meeting summarization and analysis utility."""
    
    def __init__(self):
        """Initialize the meeting summarizer."""
        self.priority_keywords = {
            'high': ['urgent', 'critical', 'asap', 'immediately', 'priority', 'important'],
            'medium': ['soon', 'next week', 'following week', 'moderate'],
            'low': ['when possible', 'low priority', 'nice to have']
        }
    
    def enhance_summary(self, summary_data: Dict[str, any]) -> Dict[str, any]:
        """
        Enhance the summary with additional analysis and formatting.
        
        Args:
            summary_data (Dict): Raw summary data from Granite API
            
        Returns:
            Dict: Enhanced summary with additional insights
        """
        enhanced = summary_data.copy()
        
        # Add metadata
        enhanced['metadata'] = {
            'processed_at': datetime.now().isoformat(),
            'total_action_items': len(summary_data.get('action_items', [])),
            'meeting_type': self._classify_meeting_type(summary_data),
            'estimated_duration': self._estimate_meeting_duration(summary_data)
        }
        
        # Enhance action items
        enhanced['action_items'] = self._enhance_action_items(
            summary_data.get('action_items', [])
        )
        
        # Add insights
        enhanced['insights'] = self._generate_insights(summary_data)
        
        # Add timeline analysis
        enhanced['timeline'] = self._analyze_timeline(summary_data)
        
        return enhanced
    
    def _classify_meeting_type(self, summary_data: Dict[str, any]) -> str:
        """Classify the type of meeting based on content."""
        topics = ' '.join(summary_data.get('topics_discussed', [])).lower()
        summary = summary_data.get('summary', '').lower()
        
        if any(word in topics + summary for word in ['kickoff', 'launch', 'start']):
            return 'Project Kickoff'
        elif any(word in topics + summary for word in ['review', 'status', 'progress']):
            return 'Status Review'
        elif any(word in topics + summary for word in ['planning', 'strategy', 'roadmap']):
            return 'Planning'
        elif any(word in topics + summary for word in ['retrospective', 'post-mortem', 'lessons']):
            return 'Retrospective'
        elif any(word in topics + summary for word in ['decision', 'approval', 'sign-off']):
            return 'Decision Making'
        else:
            return 'General Discussion'
    
    def _estimate_meeting_duration(self, summary_data: Dict[str, any]) -> str:
        """Estimate meeting duration based on content length and complexity."""
        transcript_length = len(summary_data.get('summary', ''))
        action_items_count = len(summary_data.get('action_items', []))
        topics_count = len(summary_data.get('topics_discussed', []))
        
        # Rough estimation based on content complexity
        base_time = 15  # minutes
        time_per_topic = 10
        time_per_action_item = 5
        
        estimated_minutes = base_time + (topics_count * time_per_topic) + (action_items_count * time_per_action_item)
        
        if estimated_minutes <= 30:
            return f"{estimated_minutes} minutes"
        elif estimated_minutes <= 60:
            return f"{estimated_minutes} minutes"
        else:
            hours = estimated_minutes // 60
            minutes = estimated_minutes % 60
            return f"{hours}h {minutes}m"
    
    def _enhance_action_items(self, action_items: List[Dict]) -> List[Dict]:
        """Enhance action items with additional analysis."""
        enhanced_items = []
        
        for item in action_items:
            enhanced_item = item.copy()
            
            # Add priority if not present
            if 'priority' not in enhanced_item:
                enhanced_item['priority'] = self._determine_priority(item)
            
            # Add estimated effort
            enhanced_item['estimated_effort'] = self._estimate_effort(item)
            
            # Add status
            enhanced_item['status'] = 'Pending'
            
            # Add unique ID
            enhanced_item['id'] = f"task_{len(enhanced_items) + 1}"
            
            enhanced_items.append(enhanced_item)
        
        return enhanced_items
    
    def _determine_priority(self, action_item: Dict) -> str:
        """Determine priority based on keywords and context."""
        task_text = action_item.get('task', '').lower()
        deadline = action_item.get('deadline', '').lower()
        
        # Check for urgent keywords
        if any(keyword in task_text for keyword in self.priority_keywords['high']):
            return 'High'
        elif any(keyword in deadline for word in ['today', 'tomorrow', 'asap', 'urgent']):
            return 'High'
        elif any(keyword in task_text for keyword in self.priority_keywords['medium']):
            return 'Medium'
        elif any(keyword in task_text for keyword in self.priority_keywords['low']):
            return 'Low'
        else:
            return 'Medium'  # Default priority
    
    def _estimate_effort(self, action_item: Dict) -> str:
        """Estimate effort required for the task."""
        task_text = action_item.get('task', '').lower()
        
        if any(word in task_text for word in ['review', 'check', 'verify']):
            return 'Low (1-2 hours)'
        elif any(word in task_text for word in ['prepare', 'create', 'draft']):
            return 'Medium (4-8 hours)'
        elif any(word in task_text for word in ['implement', 'develop', 'build']):
            return 'High (1-3 days)'
        elif any(word in task_text for word in ['coordinate', 'organize', 'plan']):
            return 'Medium (1-2 days)'
        else:
            return 'Medium (1 day)'
    
    def _generate_insights(self, summary_data: Dict[str, any]) -> List[str]:
        """Generate insights from the meeting content."""
        insights = []
        
        action_items = summary_data.get('action_items', [])
        topics = summary_data.get('topics_discussed', [])
        decisions = summary_data.get('key_decisions', [])
        
        # Analyze action item distribution
        if action_items:
            owners = [item.get('owner', 'Unknown') for item in action_items]
            owner_counts = {}
            for owner in owners:
                owner_counts[owner] = owner_counts.get(owner, 0) + 1
            
            if len(owner_counts) > 1:
                insights.append(f"Workload distribution: {', '.join([f'{owner} ({count} tasks)' for owner, count in owner_counts.items()])}")
            
            # Priority distribution
            priorities = [item.get('priority', 'Medium') for item in action_items]
            high_priority_count = priorities.count('High')
            if high_priority_count > len(priorities) / 2:
                insights.append("High number of urgent tasks identified - consider resource allocation")
        
        # Topic analysis
        if len(topics) > 5:
            insights.append("Meeting covered many topics - consider breaking into focused sessions")
        
        # Decision analysis
        if decisions:
            insights.append(f"Key decisions made: {len(decisions)} important outcomes")
        
        return insights
    
    def _analyze_timeline(self, summary_data: Dict[str, any]) -> Dict[str, any]:
        """Analyze timeline and deadlines from the meeting."""
        action_items = summary_data.get('action_items', [])
        
        timeline = {
            'immediate': [],
            'this_week': [],
            'next_week': [],
            'future': []
        }
        
        for item in action_items:
            deadline = item.get('deadline', '').lower()
            
            if any(word in deadline for word in ['today', 'tomorrow', 'asap']):
                timeline['immediate'].append(item)
            elif any(word in deadline for word in ['friday', 'this week', 'week']):
                timeline['this_week'].append(item)
            elif any(word in deadline for word in ['next week', 'following week']):
                timeline['next_week'].append(item)
            else:
                timeline['future'].append(item)
        
        return timeline
    
    def format_for_export(self, enhanced_summary: Dict[str, any], format_type: str = 'text') -> str:
        """
        Format the summary for export in different formats.
        
        Args:
            enhanced_summary (Dict): Enhanced summary data
            format_type (str): Export format ('text', 'markdown', 'json')
            
        Returns:
            str: Formatted output
        """
        if format_type == 'json':
            return json.dumps(enhanced_summary, indent=2)
        elif format_type == 'markdown':
            return self._format_markdown(enhanced_summary)
        else:
            return self._format_text(enhanced_summary)
    
    def _format_markdown(self, summary: Dict[str, any]) -> str:
        """Format summary as markdown."""
        md = f"# Meeting Summary\n\n"
        md += f"**Date:** {summary['metadata']['processed_at'][:10]}\n"
        md += f"**Type:** {summary['metadata']['meeting_type']}\n"
        md += f"**Duration:** {summary['metadata']['estimated_duration']}\n\n"
        
        md += f"## Summary\n{summary['summary']}\n\n"
        
        md += f"## Topics Discussed\n"
        for topic in summary.get('topics_discussed', []):
            md += f"- {topic}\n"
        md += "\n"
        
        md += f"## Key Decisions\n"
        for decision in summary.get('key_decisions', []):
            md += f"- {decision}\n"
        md += "\n"
        
        md += f"## Action Items\n"
        for item in summary.get('action_items', []):
            md += f"- **{item['task']}** (Owner: {item['owner']}, Priority: {item['priority']}, Deadline: {item['deadline']})\n"
        md += "\n"
        
        md += f"## Next Steps\n{summary.get('next_steps', '')}\n\n"
        
        if summary.get('insights'):
            md += f"## Insights\n"
            for insight in summary['insights']:
                md += f"- {insight}\n"
        
        return md
    
    def _format_text(self, summary: Dict[str, any]) -> str:
        """Format summary as plain text."""
        text = f"MEETING SUMMARY\n"
        text += f"Date: {summary['metadata']['processed_at'][:10]}\n"
        text += f"Type: {summary['metadata']['meeting_type']}\n"
        text += f"Duration: {summary['metadata']['estimated_duration']}\n\n"
        
        text += f"SUMMARY:\n{summary['summary']}\n\n"
        
        text += f"TOPICS DISCUSSED:\n"
        for topic in summary.get('topics_discussed', []):
            text += f"- {topic}\n"
        text += "\n"
        
        text += f"KEY DECISIONS:\n"
        for decision in summary.get('key_decisions', []):
            text += f"- {decision}\n"
        text += "\n"
        
        text += f"ACTION ITEMS:\n"
        for item in summary.get('action_items', []):
            text += f"- {item['task']} (Owner: {item['owner']}, Priority: {item['priority']}, Deadline: {item['deadline']})\n"
        text += "\n"
        
        text += f"NEXT STEPS:\n{summary.get('next_steps', '')}\n"
        
        return text


# Global instance for easy access
summarizer = MeetingSummarizer() 