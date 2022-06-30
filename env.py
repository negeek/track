
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'danieladebowale192@gmail.com'
EMAIL_HOST_PASSWORD = 'dlion5ive'
EMAIL_PORT = 587
DB_PASSWORD = 'dlion5ive'


class env:
    def aws_access_key_id(self):
        return 'AKIAXYZ5OJWC6B5BCBUP'

    def aws_secret_access_key(self):
        return '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'

    def aws_storage_bucket_name(self):
        return 'track-profile-avatars'

    def aws_querystring_auth(self):
        return False
