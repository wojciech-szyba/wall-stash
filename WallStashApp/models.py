"""
 Copyright (C) 2026 Wojciech Szyba - All Rights Reserved
 You may use, distribute and modify this code under the
 terms of the GNU GENERAL PUBLIC LICENSE license,
 You should have received a copy of the license with
 this file. If not, please visit :
https://github.com/wojciech-szyba/wall-stash/blob/main/LICENSE
 */
"""

from django.db import models
from django.urls import reverse

from datetime import datetime
from .embeds import extract_embed_sources, extract_urls, is_code_snippet
from urllib.parse import urlparse

CONTENT_ASSOCIATIONS = {
    'sourcecode': 'Code snippet',
    'website': 'Website note',
    'note': 'Plain text note',
    'idea': 'Idea note'
}




class MemoriesModel(models.Model):
    """A typical class defining a model, derived from the Model class."""

    # Fields
    title = models.CharField(max_length=20, help_text='Title', default='Untitled')
    content = models.TextField(max_length=4000, help_text='Content')
    date = models.DateTimeField(default=datetime.now, blank=True)
    archived = models.BooleanField(default=False)
    # …

    # Metadata
    class Meta:
        ordering = ['-date']

    @property
    def get_clean_content(self):
        lines = self.content.splitlines()
        lst = []
        for line in lines:
            if len(line.strip()) > 255:
                line = f'{line[0:255]}<br>{line[255:]}'
            lst = lst + [x for x in line.strip().split(' ') if not x.startswith('#')]
        return ' '.join(lst)

    @property
    def get_date_string(self):
        now = datetime.now()  # Now
        duration = now.replace(tzinfo=None) - self.date.replace(tzinfo=None)  # For build-in functions
        duration_in_s = duration.total_seconds()
        if duration_in_s < 60:
            return 'przed chwilą'
        elif 60 < duration_in_s < 3600:
            return 'ostatnia godzina'
        elif 3600*8 > duration_in_s > 3600:
            return f'{round(duration_in_s/3600)} godzin temu'
        else:
            return self.date

    @property
    def get_embeds(self):
        return extract_embed_sources(self.content)


    def get_tags(self):
        lines = self.content.splitlines()
        lst = []
        for line in lines:
            lst = lst + [x for x in line.strip().split(' ') if x.startswith('#')]
        return lst

    @property
    def get_category(self):
        if extract_urls(self.content):
                return 'website'
        if '#idea' in self.content:
            return 'idea'
        if is_code_snippet(self.content):
            return 'sourcecode'
        return 'note'

    @property
    def get_category_image(self):
        if extract_urls(self.content):
            main_url, *_ = extract_urls(self.content)
            base_url = urlparse(main_url)
            return f'//{base_url.netloc}/favicon.ico'
        if '#idea' in self.content:
            return '/static/res/idea.png'
        if is_code_snippet(self.content):
            return '/static/res/sourcecode.png'
        return '/static/res/plain.png'

    @property
    def get_categories(self):
        for key in CONTENT_ASSOCIATIONS.keys():
            yield CONTENT_ASSOCIATIONS[key]

    @property
    def get_title(self):
        if self.get_category:
            return f'{CONTENT_ASSOCIATIONS[self.get_category]}'
        else:
            return 'Note'

    # Methods
    def get_absolute_url(self):
        """Returns the URL to access a particular instance of MyModelName."""
        return reverse('model-detail-view', args=[str(self.id)])

    def __str__(self):
        """String for representing the MemoriesModel object (in Admin site etc.)."""
        return self.title
