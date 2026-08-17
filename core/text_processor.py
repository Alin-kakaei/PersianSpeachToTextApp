from hazm import Normalizer


class FarsiTextProcessor:
    def __init__(self):
        # Hazm normalizer handles zero-width non-joiners (half-spaces) and character standardizations
        self.normalizer = Normalizer()

    def process(self, text: str) -> str:
        if not text:
            return ""

        # Normalize syntax
        clean_text = self.normalizer.normalize(text)

        # (Optional) You can add custom Regex here later to convert numbers to words
        # or implement a dictionary look-up for missing short vowels (G2P).

        return clean_text.strip()