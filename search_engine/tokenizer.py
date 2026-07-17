"""Text preprocessing and tokenization utilities."""


def strip_non_ascii(text: str) -> str:
    """Strip non-ASCII characters from text.

    Args:
        text (str): Input text to process.

    Returns:
        str: Text with non-ASCII characters removed.
    """
    if isinstance(text, str):
        return "".join(char for char in text if ord(char) < 128)
    return text


def strip_special_characters(text: str) -> str:
    """Strip special characters from text.

    Args:
        text (str): Input text to process.

    Returns:
        str: Text with special characters removed.
    """
    if isinstance(text, str):
        return "".join(char for char in text if char.isalnum() or char.isspace())
    return text


def lowercase(text: str) -> str:
    """Convert text to lowercase.

    Args:
        text (str): Input text to process.

    Returns:
        str: Text in lowercase.
    """
    if isinstance(text, str):
        return text.lower()
    return text


DEFAULT_CLEANING_STEPS = [strip_non_ascii, strip_special_characters, lowercase]


def clean_text(text: str, steps: list | None = None) -> str:
    """Clean text by removing non-ascii characters and special characters.

    Args:
        text: Input text to clean.
        steps: List of cleaning functions to apply. If None, default steps are used.

    Returns:
        Cleaned text
    """
    if steps is None:
        steps = DEFAULT_CLEANING_STEPS
    for step in steps:
        text = step(text)
    return text


def remove_stop_words(text: str) -> str:
    from nltk.corpus import stopwords
    import nltk

    if isinstance(text, str):
        try:
            stop_words = set(stopwords.words("english"))
        except LookupError:
            nltk.download("stopwords")
            stop_words = set(stopwords.words("english"))
        return " ".join(word for word in text.split() if word not in stop_words)
    return text


def stem_words(text: str) -> str:
    from nltk.stem import PorterStemmer

    stemmer = PorterStemmer()
    if isinstance(text, str):
        return " ".join(stemmer.stem(word) for word in text.split())
    return text


DEFAULT_PREPROCESSING_STEPS = [remove_stop_words, stem_words]


def preprocess(
    text: str, cleaning_steps: list | None = None, preprocessing_steps: list | None = None
) -> str:
    """Preprocess text by cleaning, removing stop words, and stemming.

    Args:
        text: Input text to preprocess.
        cleaning_steps: List of cleaning functions to apply. If None, default steps are used.
        preprocessing_steps: List of preprocessing functions to apply. If None, default steps are used.

    Returns:
        Preprocessed text
    """
    if cleaning_steps is None:
        cleaning_steps = DEFAULT_CLEANING_STEPS

    # Clean the text
    cleaned_text = clean_text(text, cleaning_steps)

    if preprocessing_steps is None:
        preprocessing_steps = DEFAULT_PREPROCESSING_STEPS

    for step in preprocessing_steps:
        cleaned_text = step(cleaned_text)

    return cleaned_text


def tokenize(text: str) -> list[str]:
    """Tokenize text.

    Args:
        text: Input text to tokenize.

    Returns:
        List of tokens.
    """
    return text.split()
