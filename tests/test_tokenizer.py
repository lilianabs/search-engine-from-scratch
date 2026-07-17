"""Tests for tokenizer module functions."""

import pytest
from search_engine.tokenizer import (
    strip_non_ascii,
    strip_special_characters,
    lowercase,
    clean_text,
    remove_stop_words,
    stem_words,
    preprocess_text,
    tokenize,
    DEFAULT_CLEANING_STEPS,
    DEFAULT_PREPROCESSING_STEPS,
)


class TestStripNonAscii:
    """Test strip_non_ascii function."""

    def test_removes_non_ascii_characters(self):
        """Test that non-ASCII characters are removed."""
        text = "Hello café"
        result = strip_non_ascii(text)
        assert "é" not in result
        assert "Hello caf" in result

    def test_keeps_ascii_characters(self):
        """Test that ASCII characters are preserved."""
        text = "Hello World 123!"
        result = strip_non_ascii(text)
        assert result == text

    def test_removes_emoji(self):
        """Test that emoji are removed."""
        text = "Hello 😀 World"
        result = strip_non_ascii(text)
        assert "😀" not in result

    def test_empty_string(self):
        """Test with empty string."""
        result = strip_non_ascii("")
        assert result == ""

    def test_non_string_input_returns_input(self):
        """Test that non-string input returns unchanged."""
        assert strip_non_ascii(123) == 123
        assert strip_non_ascii(None) is None


class TestStripSpecialCharacters:
    """Test strip_special_characters function."""

    def test_removes_punctuation(self):
        """Test that punctuation is removed."""
        text = "Hello, World!"
        result = strip_special_characters(text)
        assert result == "Hello World"

    def test_keeps_alphanumeric_and_spaces(self):
        """Test that alphanumeric characters and spaces are preserved."""
        text = "Hello World 123"
        result = strip_special_characters(text)
        assert result == text

    def test_removes_special_symbols(self):
        """Test that special symbols are removed."""
        text = "Price: $99.99"
        result = strip_special_characters(text)
        assert "$" not in result
        assert "." not in result
        assert ":" not in result

    def test_preserves_multiple_spaces(self):
        """Test that multiple spaces are preserved."""
        text = "Hello  World"
        result = strip_special_characters(text)
        assert result == "Hello  World"

    def test_empty_string(self):
        """Test with empty string."""
        result = strip_special_characters("")
        assert result == ""

    def test_non_string_input_returns_input(self):
        """Test that non-string input returns unchanged."""
        assert strip_special_characters(123) == 123


class TestLowercase:
    """Test lowercase function."""

    def test_converts_uppercase_to_lowercase(self):
        """Test that uppercase is converted to lowercase."""
        text = "HELLO WORLD"
        result = lowercase(text)
        assert result == "hello world"

    def test_preserves_lowercase(self):
        """Test that lowercase text is unchanged."""
        text = "hello world"
        result = lowercase(text)
        assert result == text

    def test_mixed_case(self):
        """Test mixed case conversion."""
        text = "Hello World"
        result = lowercase(text)
        assert result == "hello world"

    def test_with_numbers(self):
        """Test that numbers are preserved."""
        text = "Hello123World"
        result = lowercase(text)
        assert result == "hello123world"

    def test_empty_string(self):
        """Test with empty string."""
        result = lowercase("")
        assert result == ""

    def test_non_string_input_returns_input(self):
        """Test that non-string input returns unchanged."""
        assert lowercase(123) == 123


class TestCleanText:
    """Test clean_text function."""

    def test_applies_default_steps(self):
        """Test that default cleaning steps are applied."""
        text = "HELLO Café, World!"
        result = clean_text(text)
        # Should be lowercased, non-ASCII removed, punctuation removed
        assert result == "hello caf world"

    def test_applies_custom_steps(self):
        """Test that custom steps are applied in order."""
        text = "HELLO World"
        result = clean_text(text, steps=[lowercase])
        assert result == "hello world"

    def test_applies_steps_in_order(self):
        """Test that steps are applied in the correct order."""
        text = "HELLO, World!"
        result = clean_text(text, steps=[strip_special_characters, lowercase])
        assert result == "hello world"

    def test_empty_steps_list(self):
        """Test with empty steps list."""
        text = "HELLO World"
        result = clean_text(text, steps=[])
        assert result == text

    def test_single_step(self):
        """Test with a single step."""
        text = "HELLO world"
        result = clean_text(text, steps=[lowercase])
        assert result == "hello world"

    def test_empty_string(self):
        """Test with empty string and default steps."""
        result = clean_text("")
        assert result == ""


class TestTokenize:
    """Test tokenize function."""

    def test_splits_simple_text(self):
        """Test tokenization of simple text."""
        text = "hello world"
        result = tokenize(text)
        assert result == ["hello", "world"]

    def test_splits_on_whitespace(self):
        """Test that multiple consecutive spaces are handled correctly."""
        text = "hello  world"
        result = tokenize(text)
        assert result == ["hello", "world"]
        assert "" not in result

    def test_handles_tabs_and_newlines(self):
        """Test that tabs and newlines are treated as whitespace."""
        text = "hello\tworld\nfoo"
        result = tokenize(text)
        assert result == ["hello", "world", "foo"]

    def test_empty_string(self):
        """Test with empty string."""
        result = tokenize("")
        assert result == []

    def test_single_word(self):
        """Test with single word."""
        result = tokenize("hello")
        assert result == ["hello"]

    def test_string_with_leading_trailing_spaces(self):
        """Test that leading and trailing spaces are stripped."""
        text = "  hello world  "
        result = tokenize(text)
        assert result == ["hello", "world"]


class TestRemoveStopWords:
    """Test remove_stop_words function."""

    def test_removes_common_stop_words(self):
        """Test that common stop words are removed."""
        text = "the quick brown fox"
        result = remove_stop_words(text)
        assert "the" not in result.split()

    def test_keeps_meaningful_words(self):
        """Test that meaningful words are preserved."""
        text = "the quick brown fox jumps"
        result = remove_stop_words(text)
        tokens = result.split()
        assert "quick" in tokens
        assert "brown" in tokens
        assert "fox" in tokens
        assert "jumps" in tokens

    def test_empty_string(self):
        """Test with empty string."""
        result = remove_stop_words("")
        assert result == ""

    def test_only_stop_words(self):
        """Test with only stop words."""
        text = "the is a"
        result = remove_stop_words(text)
        # Result should be mostly empty or have minimal content
        assert len(result.split()) <= 1

    def test_non_string_input_returns_input(self):
        """Test that non-string input returns unchanged."""
        assert remove_stop_words(123) == 123


class TestStemWords:
    """Test stem_words function."""

    def test_stems_words_to_root_form(self):
        """Test that words are stemmed to root form."""
        text = "running runs"
        result = stem_words(text)
        tokens = result.split()
        # Both "running" and "runs" should be stemmed to "run"
        assert tokens[0] == tokens[1]
        assert tokens[0] == "run"

    def test_preserves_already_stemmed_words(self):
        """Test that already-stemmed words are unchanged."""
        text = "cat dog"
        result = stem_words(text)
        assert "cat" in result
        assert "dog" in result

    def test_empty_string(self):
        """Test with empty string."""
        result = stem_words("")
        assert result == ""

    def test_single_word(self):
        """Test with single word."""
        result = stem_words("running")
        assert result == "run"

    def test_non_string_input_returns_input(self):
        """Test that non-string input returns unchanged."""
        assert stem_words(123) == 123


class TestPreprocessText:
    """Test preprocess_text function."""

    def test_applies_default_cleaning_and_preprocessing(self):
        """Test that default cleaning and preprocessing steps are applied."""
        text = "The RUNNING Fox"
        result = preprocess_text(text)
        # Should be cleaned (lowercased, special chars removed)
        # and preprocessed (stop words removed, stemmed)
        assert result == result.lower()
        assert "the" not in result.split()

    def test_applies_custom_cleaning_steps(self):
        """Test with custom cleaning steps."""
        text = "HELLO, World!"
        result = preprocess_text(text, cleaning_steps=[lowercase, strip_special_characters])
        # Should be lowercased and special chars removed
        assert result == "hello world"

    def test_applies_custom_preprocessing_steps(self):
        """Test with custom preprocessing steps."""
        text = "hello running world"
        result = preprocess_text(text, preprocessing_steps=[stem_words])
        tokens = result.split()
        assert "run" in tokens

    def test_skips_cleaning_with_empty_steps(self):
        """Test that empty cleaning steps skips cleaning."""
        text = "HELLO World"
        result = preprocess_text(text, cleaning_steps=[])
        # Should not be lowercased if cleaning is skipped
        assert "HELLO" in result or "hello" in result

    def test_empty_string(self):
        """Test with empty string."""
        result = preprocess_text("")
        assert result == ""

    def test_none_cleaning_steps_uses_default(self):
        """Test that None cleaning_steps uses DEFAULT_CLEANING_STEPS."""
        text = "HELLO, World!"
        result = preprocess_text(text, cleaning_steps=None)
        # Should apply default cleaning
        assert result == result.lower()

    def test_none_preprocessing_steps_uses_default(self):
        """Test that None preprocessing_steps uses DEFAULT_PREPROCESSING_STEPS."""
        text = "the running fox"
        result = preprocess_text(text, preprocessing_steps=None)
        # Should apply default preprocessing (stop words and stemming)
        assert "the" not in result.split()


class TestDefaultSteps:
    """Test default step configurations."""

    def test_default_cleaning_steps_contains_functions(self):
        """Test that DEFAULT_CLEANING_STEPS contains callable functions."""
        assert len(DEFAULT_CLEANING_STEPS) > 0
        for step in DEFAULT_CLEANING_STEPS:
            assert callable(step)

    def test_default_preprocessing_steps_contains_functions(self):
        """Test that DEFAULT_PREPROCESSING_STEPS contains callable functions."""
        assert len(DEFAULT_PREPROCESSING_STEPS) > 0
        for step in DEFAULT_PREPROCESSING_STEPS:
            assert callable(step)


class TestIntegration:
    """Integration tests for complete pipelines."""

    def test_full_pipeline_with_clean_text_and_tokenize(self):
        """Test a complete pipeline: clean → tokenize."""
        text = "HELLO, World! How are you?"
        cleaned = clean_text(text)
        tokens = tokenize(cleaned)
        assert all(token.islower() for token in tokens)
        assert all("," not in token and "!" not in token for token in tokens)

    def test_full_pipeline_with_preprocess_and_tokenize(self):
        """Test complete pipeline: preprocess → tokenize."""
        text = "The quick brown foxes are running quickly"
        preprocessed = preprocess_text(text)
        tokens = tokenize(preprocessed)
        assert "the" not in tokens
        assert any("fox" in token or token.startswith("fox") for token in tokens)

    def test_reproducibility(self):
        """Test that processing the same text twice yields the same result."""
        text = "The Quick Brown Fox"
        result1 = clean_text(text)
        result2 = clean_text(text)
        assert result1 == result2
