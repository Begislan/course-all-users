from django import template
import re

register = template.Library()

@register.filter
def embed_youtube_url(value):
    """
    Преобразует обычную YouTube-ссылку в формат для iframe-вставки.
    """
    youtube_regex = r'(?:https?:\/\/)?(?:www\.)?youtu(?:\.be\/|be\.com\/watch\?v=)([\w\-]{11})'
    match = re.search(youtube_regex, value)
    if match:
        video_id = match.group(1)
        return f'https://www.youtube.com/embed/{video_id}'
    return value  # Возвращаем оригинал, если не похоже на YouTube

register = template.Library()

@register.filter
def youtube_embed_url(url):
    # Преобразование YouTube URL в embed формат
    regex = r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
    match = re.match(regex, url)
    if match:
        video_id = match.group(6)
        return f'https://www.youtube.com/embed/{video_id}'
    return None