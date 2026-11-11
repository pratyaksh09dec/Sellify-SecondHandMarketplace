CATEGORY_DESCRIPTIONS = {
    "mobile": "a mobile phone",
    "laptop": "a laptop",
    "tablet": "a tablet computer",
    "headphones": "headphones or earphones",
    "camera": "a camera",
    "watch": "a wrist watch",
    "tv": "a television",
    "furniture": "furniture like a chair, table or sofa",
    "book": "a book",
    "bicycle": "a bicycle",
    "appliance": "a home appliance like a fridge, washing machine or fan",
}

_classifier = None


def _get_classifier():
    global _classifier
    if _classifier is None:
        from transformers import pipeline
        _classifier = pipeline(
            "zero-shot-image-classification",
            model="openai/clip-vit-base-patch32",
        )
    return _classifier


def detect_category(image_path):
    try:
        classifier = _get_classifier()
        labels = list(CATEGORY_DESCRIPTIONS.values())
        results = classifier(image_path, candidate_labels=labels)
        best = results[0]

        for key, text in CATEGORY_DESCRIPTIONS.items():
            if text == best["label"]:
                return key, round(best["score"] * 100, 1)
    except Exception as error:
        print("Image recognition failed:", error)
    return None, None