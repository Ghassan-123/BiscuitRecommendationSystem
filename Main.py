from RecommendationEngine import RecommendationEngine
from MyFacts import *


class Main:
    def __init__(self):
        pass

    def main(self):
        # Sample input - keys must match exactly with lowercase
        quality_report = {
            "cracked": {"size": 18.7},
            "burned": {"percentage": 4.3},
            "over_sized": {"size": 12.0},
            "contaminated": {},
        }

        #     recommendations = self.analyze_quality(quality_report)

        #     print("Quality Control Recommendations:")
        #     for i, rec in enumerate(recommendations, 1):
        #         print(f"{i}. {rec}")

        # def analyze_quality(self, quality_data):
        #     engine = RecommendationEngine()
        #     engine.reset()

        #     # Map must use lowercase keys matching quality_report
        #     fact_classes = {
        #         "cracked": Cracked,
        #         "burned": Burned,
        #         "under_cooked": UnderCooked,
        #         "over_sized": OverSized,
        #         "under_sized": UnderSized,
        #         "contaminated": Contaminated,
        #     }

        #     for fact_name, params in quality_data.items():
        #         if fact_name in fact_classes:
        #             engine.declare(fact_classes[fact_name](**params))

        #     engine.run()
        #     return engine.recommendations

        engine = RecommendationEngine()
        engine.reset()
        engine.run()
        # Collect predictions and recommendations
        predictions = []
        recommendations = set()  # Use set to avoid duplicates

        for fact in engine.facts.values():
            if isinstance(fact, Prediction):
                predictions.append(fact)
            elif fact.get("recommendation"):
                recommendations.add(fact["recommendation"])

        # Sort predictions by CF descending for prioritization
        predictions.sort(key=lambda p: p["cf"], reverse=True)

        # Format and print the output
        print("### Biscuit Production Line Recommendations\n")

        total = next(
            (
                f["text"]
                for f in engine.facts.values()
                if isinstance(f, Answer) and f["id"] == "total"
            ),
            0,
        )
        defected = next(
            (
                f["text"]
                for f in engine.facts.values()
                if isinstance(f, Answer) and f["id"] == "deffected"
            ),
            0,
        )
        overall_rate = (int(defected) / int(total) * 100) if int(total) > 0 else 0

        print(
            f"Based on the provided batch data (total: {total} biscuits, defective: {defected}), the system identified the following issues and corresponding actions. Recommendations are prioritized by severity (e.g., contamination is critical). Only triggered defects are listed.\n"
        )

        if predictions:
            for idx, pred in enumerate(predictions, 1):
                text_parts = pred["text"].split(" - ")
                if len(text_parts) >= 2:
                    defect_type = text_parts[0]
                    remaining = " - ".join(text_parts[1:])
                    level_parts = remaining.split(" (")
                    if len(level_parts) >= 2:
                        level = level_parts[0]
                        percentage_str = "(" + " (".join(level_parts[1:]).rstrip(")")
                    else:
                        level = remaining
                        percentage_str = ""
                else:
                    defect_type = pred["text"]
                    level = ""
                    percentage_str = ""

                cf = pred["cf"]

                header = f"#### {idx}. **{defect_type.strip()}"
                if level:
                    header += f" ({level.capitalize()}"
                    if percentage_str:
                        header += f" - {percentage_str}"
                    header += ")**"
                else:
                    header += "**"

                print(header)
                print(
                    f"   - **Certainty Factor (CF)**: {cf:.3f} (adjusted for severity and proportion)"
                )
                print("   - **Actions**:")
                # Find matching recommendation
                matching_rec = next(
                    (
                        rec
                        for rec in recommendations
                        if any(
                            key in rec.lower() for key in defect_type.lower().split()
                        )
                    ),
                    "No specific actions defined.",
                )
                for line in matching_rec.split("\n"):
                    print(f"     {line}")
                print()

                # Remove used recommendation to avoid duplication
                recommendations.discard(matching_rec)

        # Any remaining recommendations (e.g., overall)
        if recommendations:
            print("#### Additional Recommendations")
            for rec in recommendations:
                for line in rec.split("\n"):
                    print(f"   {line}")

        print("### Summary")
        print(
            f"- **Overall Defect Rate**: {overall_rate:.1f}% ({'critical' if overall_rate > 33 else 'moderate' if overall_rate > 10 else 'low'})."
        )


if __name__ == "__main__":
    Main().main()
