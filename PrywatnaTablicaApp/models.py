from django.db import models
from django.urls import reverse

from datetime import datetime
from urllib.parse import urlparse

CONTENT_ASSOCIATIONS = {
    'youtube.com': 'youtube',
    'def ': 'sourcecode',
    'open.spotify.com': 'spotify',
    'www.': 'website'
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
    def check_if_content_has_embed(self):
        if 'youtube' in self.content:
            if '.com' in self.content:
                return f'{self.content.replace("https://","//")}'
            else:
                return self.content
        else:
            return self.content

    @property
    def extract_embed_source(content):
        url_data = urlparse(content)
        print(url_data)
        if url_data.query:
            query_items = url_data.query.split('&')
            for query_item in query_items:
                if 'v=' in query_item:
                    return query_item.replace('v=', '')
                else:
                    pass
            embed = url_data.path.split('/')[-1]
        else:
            embed = url_data.path.split('/')[-1]

        return f'https://www.youtube.com/embed/{embed}'

    def get_tags(self):
        lines = self.content.splitlines()
        lst = []
        for line in lines:
            lst = lst + [x for x in line.strip().split(' ') if x.startswith('#')]
        return lst

    @property
    def get_category(self):
        for key in CONTENT_ASSOCIATIONS.keys():
            if key in self.content:
                return CONTENT_ASSOCIATIONS[key]

    @property
    def get_categories(self):
        for key in CONTENT_ASSOCIATIONS.keys():
            yield CONTENT_ASSOCIATIONS[key]

    @property
    def get_title(self):
        return f'{self.get_category.capitalize()} note'

    # Methods
    def get_absolute_url(self):
        """Returns the URL to access a particular instance of MyModelName."""
        return reverse('model-detail-view', args=[str(self.id)])

    def __str__(self):
        """String for representing the MemoriesModel object (in Admin site etc.)."""
        return self.title
