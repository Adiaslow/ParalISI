# src/PyISI/analysis/statistics.py

from typing import Dict, Optional, Tuple
import numpy as np
from numpy.typing import NDArray
from scipy import stats
from dataclasses import dataclass
from ..core.exceptions import StatisticsError

@dataclass
class StatTestResult:
    """Container for statistical test results"""
    statistic: float
    pvalue: float
    confidence_interval: Optional[Tuple[float, float]] = None
    effect_size: Optional[float] = None

class StatisticalAnalyzer:
    """Performs statistical analysis on experimental data."""

    def __init__(self, alpha: float = 0.05):
        self.alpha = alpha

    def compare_conditions(
        self,
        condition1: NDArray,
        condition2: NDArray,
        test: str = 'ttest',
        paired: bool = False
    ) -> StatTestResult:
        """Compare two experimental conditions.

        Parameters
        ----------
        condition1 : NDArray
            Data from first condition
        condition2 : NDArray
            Data from second condition
        test : str, optional
            Statistical test to use, by default 'ttest'
        paired : bool, optional
            Whether to use paired test, by default False

        Returns
        -------
        StatTestResult
            Test results
        """
        try:
            if test == 'ttest':
                result = self._run_ttest(condition1, condition2, paired)
            elif test == 'wilcoxon':
                result = self._run_wilcoxon(condition1, condition2, paired)
            else:
                raise ValueError(f"Unknown test: {test}")

            return result

        except Exception as e:
            raise StatisticsError(f"Statistical comparison failed: {str(e)}") from e

    def _run_ttest(
        self,
        x1: NDArray,
        x2: NDArray,
        paired: bool
    ) -> StatTestResult:
        """Run t-test"""
        if paired:
            stat, pval = stats.ttest_rel(x1, x2)
        else:
            stat, pval = stats.ttest_ind(x1, x2)

        # Calculate confidence interval
        if paired:
            diff = x1 - x2
            ci = stats.t.interval(
                1 - self.alpha,
                len(diff) - 1,
                loc=np.mean(diff),
                scale=stats.sem(diff)
            )
        else:
            ci = None

        # Calculate effect size (Cohen's d)
        effect = (np.mean(x1) - np.mean(x2)) / np.sqrt(
            (np.var(x1) + np.var(x2)) / 2
        )

        return StatTestResult(
            statistic=float(stat),
            pvalue=float(pval),
            confidence_interval=ci,
            effect_size=float(effect)
        )

    def _run_wilcoxon(
        self,
        x1: NDArray,
        x2: NDArray,
        paired: bool
    ) -> StatTestResult:
        """Run Wilcoxon test"""
        if paired:
            stat, pval = stats.wilcoxon(x1, x2)
        else:
            stat, pval = stats.mannwhitneyu(x1, x2)

        # Calculate effect size (r = Z / sqrt(N))
        n = len(x1) + len(x2)
        z = stats.norm.ppf(1 - pval/2)
        effect = z / np.sqrt(n)

        return StatTestResult(
            statistic=float(stat),
            pvalue=float(pval),
            effect_size=float(effect)
        )

# Example usage
if __name__ == "__main__":
    # Create analyzers
    metrics = MetricsCalculator(sampling_rate=30.0)
    quality = QualityAnalyzer()
    stats_analyzer = StatisticalAnalyzer()

    # Example data
    data = np.random.randn(100, 64, 64)
    baseline = data[:20]
    response = data[20:]

    # Calculate metrics
    response_metrics = metrics.compute_response_metrics(
        response,
        baseline,
        stimulus_onset=20
    )

    # Assess quality
    quality_assessment = quality.assess_quality(data)

    # Run statistical comparison
    condition1 = np.random.randn(30)
    condition2 = np.random.randn(30) + 0.5
    stats_result = stats_analyzer.compare_conditions(
        condition1,
        condition2,
        test='ttest',
        paired=True
    )

    print("\nAnalysis Results:")
    print(f"SNR: {response_metrics.snr:.2f}")
    print(f"Quality: {quality_assessment.overall_quality.value}")
    print(f"Statistical test p-value: {stats_result.pvalue:.4f}")
