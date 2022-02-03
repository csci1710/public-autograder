import sys
import json

if __name__ == "__main__":
    assert len(sys.argv) == 3, "Usage: python3 translate_to_gradescope.py <from> <to>"
    (_, from_file, to_file) = sys.argv

    with open(from_file, "r") as f:
        raw_results = json.loads(f.read())

    gradescope_results = []
    summary_results = []

    for sub_assignment_number, sub_assignment in enumerate(raw_results):
        for test_suite_number, test_suite in enumerate(sub_assignment["functionality"]):
            sub_results_tests = []
            num_passed, total = 0, 0
            for test_result_number, test_result in enumerate(test_suite):
                name, passed = test_result["name"], test_result["passed?"]

                num_passed += 1 if passed else 0
                total += 1

                sub_results_tests.append({
                            "score": 0,
                            "max_score": 0 if passed else 1,
                            "name": f"{sub_assignment['name']} test: {name}",
                            #"number": f"{sub_assignment_number}.{test_suite_number}.{test_result_number}",
                            "output": "Test passed!" if passed else "Test failed.",
                            "visibility": "after_published",
                        })

            summary_results.append({
                    "score": num_passed,
                    "max_score": total,
                    "name": f"Functionality for {sub_assignment['name']}",
                    #"number": f"{sub_assignment_number}.{test_suite_number}",
                    "visibility": "hidden",
                })
            gradescope_results += sub_results_tests

        # wheat_fail_tests = set()
        # for wheat_number, wheat in enumerate(sub_assignment["wheats"]):
        #     wheat_results = wheat["results"]
        #     failed = {test["name"] for test in wheat_results if not test["passed?"]}
        #     if failed:
        #         wheat_fail_tests = wheat_fail_tests.union(failed)
        #         gradescope_results.append({
        #             "score": 0,
        #             "max_score": 1,
        #             "name": f"{sub_assignment['name']}: wheat {wheat_number + 1}",
        #             "output": f"Wheat failed on these tests:\n{failed}\n"\
        #                 + "These tests are invalid and cannot be used to catch chaffs.",
        #             "visibility": "after_published",
        #         })
        #     else:
        #         gradescope_results.append({
        #             "score": 0,
        #             "max_score": 0,
        #             "name": f"{sub_assignment['name']}: wheat {wheat_number + 1}",
        #             "output": f"Wheat passed!",
        #             "visibility": "after_published",
        #         })

        # chaffs_caught = 0
        # for chaff in sub_assignment["chaffs"]:
        #     chaff_results = chaff["results"]
        #     failed = {test["name"] for test in chaff_results if not test["passed?"]}
        #     # can't use invalid tests to catch chaffs
        #     failed = failed - wheat_fail_tests
        #     if failed:
        #         chaffs_caught += 1
        #         gradescope_results.append({
        #             "score": 0,
        #             "max_score": 0,
        #             "name": f"{sub_assignment['name']} chaff: {chaff['name']}",
        #             "output": f"Chaff caught with these tests:\n{failed}",
        #             "visibility": "after_published",
        #         })
        #     else:
        #         gradescope_results.append({
        #             "score": 0,
        #             "max_score": 1,
        #             "name": f"{sub_assignment['name']} chaff: {chaff['name']}",
        #             "output": f"Chaff not caught.",
        #             "visibility": "after_published",
        #         })
        # if sub_assignment["chaffs"]:
        #     summary_results.append({
        #         "score": chaffs_caught,
        #         "max_score": len(sub_assignment["chaffs"]),
        #         "name": f"Chaffs for {sub_assignment['name']}",
        #         "output": f"Also, wheats {'failed' if wheat_fail_tests else 'passed'}",
        #         "visibility": "hidden",
        #     })

    gradescope_results += summary_results


    full_report = {
            "score": 0,
            "output": "Your code ran successfully! You can see your results after we publish your grades.",
            "visibility": "visible",
            "stdout_visibility": "hidden",
            "tests": gradescope_results,
        }

    with open(to_file, "w") as f:
        json.dump(full_report, f)

"""
{ "score": 44.0, // optional, but required if not on each test case below. Overrides total of tests if specified.
  "execution_time": 136, // optional, seconds
  "output": "Text relevant to the entire submission", // optional
  "visibility": "after_due_date", // Optional visibility setting
  "stdout_visibility": "visible", // Optional stdout visibility setting
  "extra_data": {}, // Optional extra data to be stored
  "tests": // Optional, but required if no top-level score
    [
        {
            "score": 2.0, // optional, but required if not on top level submission
            "max_score": 2.0, // optional
            "name": "Your name here", // optional
            "number": "1.1", // optional (will just be numbered in order of array if no number given)
            "output": "Giant multiline string that will be placed in a <pre> tag and collapsed by default", // optional
            "tags": ["tag1", "tag2", "tag3"], // optional
            "visibility": "visible", // Optional visibility setting
            "extra_data": {} // Optional extra data to be stored
        },
        // and more test cases...
    ],
  "leaderboard": // Optional, will set up leaderboards for these values
    [
      {"name": "Accuracy", "value": .926},
      {"name": "Time", "value": 15.1, "order": "asc"},
      {"name": "Stars", "value": "*****"}
    ]
}
"""
