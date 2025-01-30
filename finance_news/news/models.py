from djongo import models

class News(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField(unique=True)
    source = models.CharField(max_length=100)
    published_at = models.DateTimeField()
    summary = models.TextField()
    content = models.TextField(null=True, blank=True)
    category = models.CharField(max_length=50, choices=[
        ("market", "Market"),
        ("crypto", "Crypto"),
        ("stocks", "Stocks"),
        ("economy", "Economy"),
    ])

    class Meta:
        ordering = ["-published_at"]


