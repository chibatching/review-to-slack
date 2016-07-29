class Review:
    def __init__(self, json):
        self.userName = json["authorName"]
        self.reviewerLanguage = json["comments"][0]["userComment"]["reviewerLanguage"]
        self.reviewId = json["reviewId"]

        text = json["comments"][0]["userComment"]["text"].split("\t")
        if len(text) == 2:
            self.title = text[0]
            self.text = text[1]
        else:
            self.title = None
            self.text = text[0]

        self.starRating = json["comments"][0]["userComment"]["starRating"]
        self.lastModified = json["comments"][0]["userComment"]["lastModified"]["seconds"]

        if "device" in json["comments"][0]["userComment"]:
            self.device = json["comments"][0]["userComment"]["device"]
        else:
            self.device = None

        if "androidOsVersion" in json["comments"][0]["userComment"]:
            self.androidOsVersion = json["comments"][0]["userComment"]["androidOsVersion"]
        else:
            self.androidOsVersion = None

        if "appVersionName" in json["comments"][0]["userComment"]:
            self.appVersionName = json["comments"][0]["userComment"]["appVersionName"]
        else:
            self.appVersionName = None

        if "appVersionCode" in json["comments"][0]["userComment"]:
            self.appVersionCode = json["comments"][0]["userComment"]["appVersionCode"]
        else:
            self.appVersionCode = None
