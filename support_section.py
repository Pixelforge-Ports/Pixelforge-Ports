"""Shared support cards. Empty destinations remain visibly unavailable."""
import html
from urllib.parse import urlsplit

def render_support(links):
    cards=[]
    for key,title,description,icon in [
        ('discord','Discord','Join our community','◉'),
        ('source','Source','Explore PixelForge Ports','⌘'),
        ('sponsors','Sponsors','Support the next port','♥'),
        ('kofi','Ko-fi','Fuel the forge','☕'),
    ]:
        url=links.get(key,'').strip()
        if url and (urlsplit(url).scheme!='https' or not urlsplit(url).netloc):
            raise ValueError('Support links must be complete HTTPS URLs: '+key)
        content=f'<span class="support-icon {key}" aria-hidden="true">{icon}</span><span><h3>{title}</h3><p>{description if url else "Link coming soon"}</p></span>'
        if url:
            cards.append(f'<a class="support-card" href="{html.escape(url,quote=True)}">{content}<span class="support-arrow" aria-hidden="true">↗</span></a>')
        else:
            cards.append(f'<div class="support-card unavailable">{content}</div>')
    return '<section id="connect" class="support-section"><div class="wrap"><p class="eyebrow">KEEP THE FORGE GLOWING</p><h2>Connect &amp; Support</h2><div class="support-grid">'+''.join(cards)+'</div></div></section>'
