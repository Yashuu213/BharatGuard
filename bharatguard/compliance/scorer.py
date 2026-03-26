from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class ComplianceScorer:
    """
    Weighted Compliance Scorer for BharatGuard.
    Calculates the final health percentage based on categorical rule results.
    """
    
    # Weight settings according to Phase 3 requirements
    WEIGHTS = {
        "GST": 0.35,
        "UPI": 0.25,
        "Aadhaar": 0.10, # Aadhaar/DPDP split from 0.20
        "DPDP": 0.10,   # Aadhaar/DPDP split from 0.20
        "RBI": 0.15,
        "Audit": 0.05
    }

    @classmethod
    def calculate_score(cls, results: List[Dict[str, Any]]) -> tuple[float, Dict[str, float]]:
        """
        Calculates the weighted score. 
        Returns (final_score, category_scores).
        """
        category_totals = {cat: 0 for cat in cls.WEIGHTS.keys()}
        category_counts = {cat: 0 for cat in cls.WEIGHTS.keys()}
        
        for res in results:
            cat = res["category"]
            if cat in category_totals:
                category_counts[cat] += 1
                if res["status"] == "passed":
                    category_totals[cat] += 1
        
        # Add Audit log completeness simulation (based on presence of RBI-002)
        audit_passed = any(r["rule_id"] == "RBI-002" and r["status"] == "passed" for r in results)
        category_totals["Audit"] = 1 if audit_passed else 0
        category_counts["Audit"] = 1

        weighted_score = 0.0
        category_percentages = {}
        
        for cat, weight in cls.WEIGHTS.items():
            count = category_counts[cat]
            if count > 0:
                percentage = (category_totals[cat] / count) * 100
                category_percentages[cat] = percentage
                weighted_score += (percentage * weight)
            else:
                # If no rules for this category, assume 100% or 0% behavior depends on requirements
                # Here we assume 100% compliance for unrelated categories to avoid penalty
                category_percentages[cat] = 100.0
                weighted_score += (100.0 * weight)
                
        return round(weighted_score, 2), category_percentages
