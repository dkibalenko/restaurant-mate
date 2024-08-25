class RequiredFieldsMixin:
    required_fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.required_fields:
            if field in self.fields:
                self.fields[field].required = True
