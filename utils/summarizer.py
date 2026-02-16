"""
News summarization module
"""
class NewsSummarizer:
    """Class to handle news summarization"""
    
    @staticmethod
    def summarize(text, max_length=100):
        """Summarize given text"""
        if len(text) <= max_length:
            return text
        return text[:max_length] + "..."