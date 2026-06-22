"""
Unit tests for rival_search_mcp.core.conflict.detect.

Covers the three detection strategies, with specific focus on the
bull/bear polarity cases that were missed before strategy 3 +
_find_sentiment_conflicts were added.
"""
import pytest
from rival_search_mcp.core.conflict.detect import (
    ConflictType,
    _claim_polarity,
    _sentiment_score,
    find_conflicts,
)


# ---------------------------------------------------------------------------
# _sentiment_score
# ---------------------------------------------------------------------------

class TestSentimentScore:
    def test_bullish_text_positive(self):
        text = "Analysts are bullish on the stock; strong buy rating with significant upside."
        assert _sentiment_score(text) > 0

    def test_bearish_text_negative(self):
        text = "Analysts are bearish; the stock is a sell with meaningful downside risk."
        assert _sentiment_score(text) < 0

    def test_neutral_text_near_zero(self):
        text = "The company reported quarterly results in line with expectations."
        assert abs(_sentiment_score(text)) < 0.15

    def test_strong_buy_phrase(self):
        text = "We issue a strong buy recommendation on this name."
        assert _sentiment_score(text) > 0

    def test_strong_sell_phrase(self):
        text = "We issue a strong sell recommendation; target cut."
        assert _sentiment_score(text) < 0


# ---------------------------------------------------------------------------
# _claim_polarity — strategies 1 & 2 (existing) + strategy 3 (new)
# ---------------------------------------------------------------------------

class TestClaimPolarity:
    # Strategy 1: direct substring
    def test_direct_match_supported(self):
        assert _claim_polarity("The drug is safe and effective.", "drug is safe") is True

    def test_direct_match_negated(self):
        assert _claim_polarity("The drug is not safe for patients.", "drug is safe") is False

    # Strategy 2: copula split
    def test_copula_split_negated(self):
        assert _claim_polarity("The vaccine is absolutely not effective.", "vaccine is effective") is False

    # Strategy 3: sentiment fallback for bull/bear
    def test_bullish_source_returns_true_for_bullish_claim(self):
        # "analysts" appears in both claim and source → strategy 3 anchor fires
        src = "Analysts are very bullish; this is a strong buy with 40% upside."
        result = _claim_polarity(src, "analysts outlook")
        assert result is True

    def test_bearish_source_returns_false_for_bullish_claim(self):
        # "analysts" appears in both claim and source → strategy 3 anchor fires
        src = "Analysts are very bearish; strong sell with significant downside risk."
        result = _claim_polarity(src, "analysts outlook")
        assert result is False

    def test_absent_subject_returns_none(self):
        src = "Analysts are bullish on tech stocks."
        # claim subject "pharma sector" is not in src
        result = _claim_polarity(src, "pharma sector outlook")
        assert result is None


# ---------------------------------------------------------------------------
# find_conflicts — end-to-end polarity conflict detection
# ---------------------------------------------------------------------------

class TestFindConflictsBullBear:
    def test_bull_vs_bear_detected_without_claim(self):
        sources = [
            "Goldman Sachs is bullish on Tesla stock; strong buy, target raised to $400.",
            "Morgan Stanley is bearish on Tesla stock; strong sell, target lowered to $120.",
        ]
        report = find_conflicts(sources)
        polarity = [c for c in report.conflicts if c.type == ConflictType.POLARITY]
        assert len(polarity) >= 1, "Should detect bull/bear conflict without a claim"
        c = polarity[0]
        assert c.value_a != c.value_b

    def test_bull_vs_bear_detected_with_claim(self):
        sources = [
            "Analysts are bullish on the company's growth; buy rating maintained.",
            "Analysts are bearish on the company's growth; sell rating on downside risks.",
        ]
        report = find_conflicts(sources, claim="company's growth outlook")
        polarity = [c for c in report.conflicts if c.type == ConflictType.POLARITY]
        assert len(polarity) >= 1

    def test_both_bullish_no_conflict(self):
        sources = [
            "Analyst A is bullish; buy recommendation with strong upside.",
            "Analyst B is also bullish; outperform rating, favorable conditions.",
        ]
        report = find_conflicts(sources)
        polarity = [c for c in report.conflicts if c.type == ConflictType.POLARITY]
        assert len(polarity) == 0, "Two bullish sources should not conflict"

    def test_neutral_sources_no_sentiment_conflict(self):
        sources = [
            "The company reported Q3 results. Revenue came in at $2.1B.",
            "The company announced Q3 earnings. Revenue was $1.8B.",
        ]
        report = find_conflicts(sources)
        polarity = [c for c in report.conflicts if c.type == ConflictType.POLARITY]
        assert len(polarity) == 0

    def test_unrelated_topics_no_conflict(self):
        # Both directional but on completely different subjects with minimal shared vocab.
        sources = [
            "The solar panel installation exceeded projections; momentum is very favorable.",
            "The bank's credit book deteriorated sharply; cautious on outlook, significant headwind.",
        ]
        report = find_conflicts(sources)
        polarity = [c for c in report.conflicts if c.type == ConflictType.POLARITY]
        assert len(polarity) == 0, "Unrelated topics should not conflict"


# ---------------------------------------------------------------------------
# Regression: existing numeric + date detection still works
# ---------------------------------------------------------------------------

class TestNumericAndDateRegression:
    def test_numeric_conflict_still_detected(self):
        sources = [
            "OpenAI raised $10 billion in its latest funding round.",
            "OpenAI raised $6.6 billion in its latest funding round.",
        ]
        report = find_conflicts(sources)
        numeric = [c for c in report.conflicts if c.type == ConflictType.NUMERIC]
        assert len(numeric) >= 1

    def test_date_conflict_still_detected(self):
        sources = [
            "The company was founded in 2015 by its current CEO.",
            "The company was founded in 2016 by its current CEO.",
        ]
        report = find_conflicts(sources)
        date_conflicts = [c for c in report.conflicts if c.type == ConflictType.DATE]
        assert len(date_conflicts) >= 1
