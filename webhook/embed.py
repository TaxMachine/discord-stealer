import json


class Embed:
    def __init__(self):
        self.title = None
        self.description = None
        self.author = None
        self.timestamp = None
        self.fields = None
        self.color = None
        self.thumbnail = None
        self.image = None
        self.footer = None

    def setTitle(self, title: str):
        if len(title) > 256:
            raise ValueError("Title has to be less than 256 characters")
        self.title = title

    def setColor(self, r: int, g: int, b: int):
        decimal = (r << 16) + (g << 8) + b
        self.color = decimal

    def setDescription(self, description: str):
        if len(description) > 4096:
            raise ValueError("Description has to be less than 4096 characters")
        self.description = description

    def setAuthor(self, name: str, icon_url: str = None, url: str = None):
        if len(name) > 256:
            raise ValueError("Author name can only be less than 256 characters")
        self.author = {"name": name}
        if icon_url is not None:
            self.author["icon_url"]: str = icon_url
        if url is not None:
            self.author["url"]: str = url

    def setTimestamp(self, timestamp: int):
        self.timestamp: int = timestamp

    def setThumbnail(self, url: str):
        self.thumbnail = {"url": url}

    def setImage(self, url: str):
        self.image = {"url": url}

    def setFooter(self, text: str, icon_url: str = None):
        if len(text) > 2048:
            raise ValueError("Footer text has to be less than 2048 characters")
        self.footer = {"text": text}
        if icon_url is not None:
            self.footer["icon_url"]: str = icon_url

    def addField(self, name: str, value: str, inline: bool = False):
        if self.fields is not None and len(self.fields) == 25:
            raise ValueError("An embed can only contains 25 fields max")
        if len(name) > 256:
            raise ValueError("Field name has to be less than 256 characters")
        field = {"name": name}
        if len(value) > 1024:
            raise ValueError("Field value has to be less than 1024 characters")
        field["value"]: str = value
        field["inline"]: bool = inline
        if self.fields is None:
            self.fields = []
        self.fields.append(field)

    def toJson(self):
        return json.dumps(self.__dict__)
