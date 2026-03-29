# Gherkin Writing Guide and Templates

> Gherkin is the structured language used to define acceptance criteria as executable specifications. Every slice must have at least one `.feature` file in the `features/` directory.
> **Numbered Step Rule:** Every scenario with 3+ Given/When/Then/And lines must include
> `# Step N/M` comments. Agents enumerate all steps before execution and report each
> result individually. Gaps must be explained.

---
## Rules for Good Gherkin

1. **One behavior per scenario.** Each scenario tests exactly one thing. If you need "and then also," that is a second scenario.

2. **Business language, not code.** Write what the user or system does, not how the code implements it. Say "the portfolio value is calculated" not "the calculateNAV() function returns a float."

3. **Given = precondition, When = action, Then = outcome.** Do not mix them. Given sets up the world. When is the single action under test. Then asserts the result.

4. **Use Scenario Outline for data-driven tests.** When the same behavior is tested with different inputs, use `Scenario Outline` with `Examples` tables instead of duplicating scenarios.

5. **Tag scenarios for filtering.** Use tags like `@slice-3`, `@critical`, `@frontend`, `@smoke` to enable selective test runs.

6. **Keep scenarios independent.** No scenario should depend on another scenario having run first. Each scenario sets up its own preconditions.

7. **Concrete values, not vague descriptions.** Say "the price is 105.50" not "the price is a number." Say "3 rows are displayed" not "some rows are displayed."

8. **Background for shared setup.** If every scenario in a feature shares the same Given steps, use a `Background` block.

---

## Template 1: Data Correctness Scenarios

> For slices that involve calculations, data transformations, or data integrity.

```gherkin
@slice-{SLICE_NUMBER} @data-correctness
Feature: {FEATURE_NAME} — Data Correctness
  As a {USER_ROLE}
  I want {DATA_OPERATION_DESCRIPTION}
  So that {BUSINESS_VALUE}

  Background:
    Given the system has loaded {DATA_SOURCE} with the following records:
      | {COLUMN_1} | {COLUMN_2} | {COLUMN_3} |
      | {VALUE_1A} | {VALUE_1B} | {VALUE_1C} |
      | {VALUE_2A} | {VALUE_2B} | {VALUE_2C} |
      | {VALUE_3A} | {VALUE_3B} | {VALUE_3C} |

  Scenario: Correct calculation with valid inputs
    Given all input data passes validation                                # Step 1/4
    When the {CALCULATION_NAME} is executed                               # Step 2/4
    Then the result should be {EXPECTED_RESULT}                           # Step 3/4
    And the result should be rounded to {DECIMAL_PLACES} decimal places   # Step 4/4

  Scenario: Correct aggregation across multiple records
    Given there are {COUNT} records in the dataset                        # Step 1/4
    When the {AGGREGATION_NAME} is computed                               # Step 2/4
    Then the total should be {EXPECTED_TOTAL}                             # Step 3/4
    And no records should be excluded from the calculation                # Step 4/4

  Scenario Outline: Calculation with varying inputs
    Given the input {INPUT_FIELD} is <input_value>
    When the {CALCULATION_NAME} is executed
    Then the result should be <expected_result>

    Examples:
      | input_value | expected_result |
      | {SAMPLE_1}  | {RESULT_1}      |
      | {SAMPLE_2}  | {RESULT_2}      |
      | {SAMPLE_3}  | {RESULT_3}      |

  Scenario: Data integrity after transformation
    Given the raw data contains {RAW_RECORD_COUNT} records                # Step 1/5
    When the data transformation pipeline completes                       # Step 2/5
    Then the output should contain {EXPECTED_RECORD_COUNT} records        # Step 3/5
    And no data should be silently dropped                                # Step 4/5
    And a transformation log entry should be created                      # Step 5/5
```

---

## Template 2: Frontend Rendering Scenarios

> For slices that involve UI components, pages, or visual elements.

```gherkin
@slice-{SLICE_NUMBER} @frontend @ui
Feature: {FEATURE_NAME} — Frontend Rendering
  As a {USER_ROLE}
  I want to see {UI_ELEMENT_DESCRIPTION}
  So that {BUSINESS_VALUE}

  Background:
    Given I am logged in as a {USER_ROLE}
    And I am on the "{PAGE_NAME}" page

  Scenario: Page loads with correct initial state
    Then I should see the "{PAGE_TITLE}" heading                          # Step 1/4
    And the {COMPONENT_NAME} should display {EXPECTED_INITIAL_STATE}     # Step 2/4
    And no error messages should be visible                              # Step 3/4
    And the page should load within {MAX_LOAD_TIME_MS} milliseconds      # Step 4/4

  Scenario: Table displays data correctly
    Given there are {ROW_COUNT} records to display                       # Step 1/5
    When the page finishes loading                                       # Step 2/5
    Then the table should show {ROW_COUNT} rows                          # Step 3/5
    And each row should display {COLUMN_LIST}                            # Step 4/5
    And the data should be sorted by {DEFAULT_SORT_COLUMN} in {ASC_OR_DESC} order # Step 5/5

  Scenario: User applies filter
    Given the table shows {INITIAL_COUNT} records                        # Step 1/5
    When I select "{FILTER_VALUE}" from the "{FILTER_NAME}" filter       # Step 2/5
    Then the table should show {FILTERED_COUNT} records                  # Step 3/5
    And all visible records should match the filter criteria             # Step 4/5
    And the filter selection should be visually indicated                # Step 5/5

  Scenario: Empty state displays correctly
    Given there are no records matching the current view                 # Step 1/4
    When the page finishes loading                                       # Step 2/4
    Then I should see the empty state message "{EMPTY_STATE_MESSAGE}"    # Step 3/4
    And a {CALL_TO_ACTION_DESCRIPTION} should be visible                 # Step 4/4

  Scenario: Responsive layout on mobile
    Given I am viewing the page on a {MOBILE_WIDTH}px wide screen        # Step 1/3
    Then the {COMPONENT_NAME} should {RESPONSIVE_BEHAVIOR}               # Step 2/3
    And all content should be readable without horizontal scrolling      # Step 3/3
```

---

## Template 3: Edge Case Scenarios

> For testing boundary conditions, unusual inputs, and failure modes.

```gherkin
@slice-{SLICE_NUMBER} @edge-cases
Feature: {FEATURE_NAME} — Edge Cases
  As a {USER_ROLE}
  I want the system to handle unusual inputs gracefully
  So that {BUSINESS_VALUE}

  Scenario: Empty input is handled
    Given the {INPUT_FIELD} is empty                                     # Step 1/4
    When I submit the form                                               # Step 2/4
    Then I should see the validation message "{VALIDATION_MESSAGE}"      # Step 3/4
    And the submission should not be processed                           # Step 4/4

  Scenario: Maximum length input is accepted
    Given the {INPUT_FIELD} contains {MAX_LENGTH} characters             # Step 1/4
    When I submit the form                                               # Step 2/4
    Then the submission should be processed successfully                 # Step 3/4
    And the full input should be stored without truncation               # Step 4/4

  Scenario: Input exceeding maximum length is rejected
    Given the {INPUT_FIELD} contains {MAX_LENGTH_PLUS_1} characters
    When I submit the form
    Then I should see the validation message "{LENGTH_EXCEEDED_MESSAGE}"

  Scenario: Special characters in input
    Given the {INPUT_FIELD} contains "{SPECIAL_CHAR_STRING}"             # Step 1/4
    When I submit the form                                               # Step 2/4
    Then the input should be sanitized                                   # Step 3/4
    And the submission should be processed without errors                # Step 4/4

  Scenario: Duplicate submission is prevented
    Given I have already submitted {ITEM_DESCRIPTION}                    # Step 1/4
    When I submit the same {ITEM_DESCRIPTION} again                      # Step 2/4
    Then I should see the message "{DUPLICATE_MESSAGE}"                  # Step 3/4
    And only one record should exist in the system                       # Step 4/4

  Scenario: Concurrent modification is handled
    Given User A is editing {ENTITY_NAME} record #{RECORD_ID}           # Step 1/6
    And User B is also editing {ENTITY_NAME} record #{RECORD_ID}        # Step 2/6
    When User A saves their changes                                      # Step 3/6
    And User B attempts to save their changes                            # Step 4/6
    Then User B should see a conflict notification                       # Step 5/6
    And User A's changes should be preserved                             # Step 6/6

  Scenario: Network timeout during operation
    Given I am performing {OPERATION_NAME}                               # Step 1/4
    When the network connection is interrupted for {TIMEOUT_SECONDS} seconds # Step 2/4
    Then the operation should {TIMEOUT_BEHAVIOR — e.g., retry automatically, show error} # Step 3/4
    And no partial data should be persisted                              # Step 4/4

  Scenario: Zero and negative values
    Given the {NUMERIC_FIELD} is set to <value>
    When the {CALCULATION_NAME} is executed
    Then the result should be <expected_behavior>

    Examples:
      | value | expected_behavior                     |
      | 0     | {ZERO_BEHAVIOR}                       |
      | -1    | {NEGATIVE_BEHAVIOR}                   |
      | 0.001 | {VERY_SMALL_POSITIVE_BEHAVIOR}        |
```

---

## Template 4: Performance Scenarios

> For slices with performance requirements or large data volumes.

```gherkin
@slice-{SLICE_NUMBER} @performance
Feature: {FEATURE_NAME} — Performance
  As a {USER_ROLE}
  I want {OPERATION_DESCRIPTION} to complete quickly
  So that {BUSINESS_VALUE}

  Scenario: Page load time under threshold
    Given {RECORD_COUNT} records exist in the database                   # Step 1/4
    When I navigate to the "{PAGE_NAME}" page                            # Step 2/4
    Then the page should be interactive within {MAX_LOAD_TIME_MS} milliseconds # Step 3/4
    And the first contentful paint should occur within {FCP_TIME_MS} milliseconds # Step 4/4

  Scenario: Bulk operation completes within time limit
    Given I have {BULK_COUNT} items to process                           # Step 1/4
    When I trigger the {BULK_OPERATION_NAME}                             # Step 2/4
    Then all items should be processed within {MAX_DURATION_SECONDS} seconds # Step 3/4
    And a progress indicator should be visible during processing         # Step 4/4

  Scenario: Search responds within acceptable time
    Given the dataset contains {TOTAL_RECORDS} records                   # Step 1/4
    When I search for "{SEARCH_TERM}"                                    # Step 2/4
    Then results should appear within {MAX_SEARCH_TIME_MS} milliseconds  # Step 3/4
    And at least the first {INITIAL_RESULT_COUNT} results should be displayed # Step 4/4

  Scenario: Concurrent user load
    Given {CONCURRENT_USERS} users are accessing the {PAGE_NAME} simultaneously # Step 1/4
    When each user performs {ACTION_DESCRIPTION}                         # Step 2/4
    Then the average response time should be under {AVG_RESPONSE_MS} milliseconds # Step 3/4
    And no requests should fail with server errors                       # Step 4/4

  Scenario: Large file upload
    Given I have a file of {FILE_SIZE_MB} MB                             # Step 1/5
    When I upload the file via {UPLOAD_ENDPOINT}                         # Step 2/5
    Then the upload should complete within {MAX_UPLOAD_SECONDS} seconds  # Step 3/5
    And a progress indicator should update at least every {PROGRESS_INTERVAL_SECONDS} seconds # Step 4/5
    And the file should be fully persisted after upload completes        # Step 5/5
```

---

## Template 5: Goal Achievement Test Scenario

> The single most important test for any slice. Binary PASS/FAIL: can a user complete the full intended workflow from start to finish?

```gherkin
@slice-{SLICE_NUMBER} @goal-achievement @critical
Feature: {FEATURE_NAME} — Goal Achievement
  As a {USER_ROLE}
  I want to {COMPLETE_END_TO_END_GOAL}
  So that {BUSINESS_VALUE}

  # This is the Goal Achievement Test. It validates the complete workflow
  # from start to finish. There is no partial credit — the user either
  # achieves their goal or they do not.

  Scenario: User completes full workflow successfully
    # Step 1: Entry point
    Given I am logged in as a {USER_ROLE}
    And I am on the "{STARTING_PAGE}" page

    # Step 2: Initiate the workflow
    When I {FIRST_ACTION — e.g., click "Create New Report"}

    # Step 3: Provide required inputs
    And I enter "{INPUT_VALUE_1}" in the "{FIELD_1}" field
    And I select "{INPUT_VALUE_2}" from the "{FIELD_2}" dropdown
    And I upload the file "{SAMPLE_FILE_NAME}"

    # Step 4: Submit / execute
    And I click "{SUBMIT_BUTTON_TEXT}"

    # Step 5: Processing (if applicable)
    And I wait for processing to complete

    # Step 6: Verify the goal is achieved
    Then I should see the "{SUCCESS_PAGE_OR_COMPONENT}"
    And the {OUTPUT_DESCRIPTION} should display {EXPECTED_OUTPUT}
    And I should be able to {VERIFY_ACTION — e.g., download the report, see the updated record}

    # Step 7: Verify persistence (the result survives a page refresh)
    When I refresh the page
    Then the {OUTPUT_DESCRIPTION} should still display {EXPECTED_OUTPUT}
```

---
## File Naming Convention

Place feature files in the `features/` directory using this naming pattern:

```
features/slice-{N}-{feature-name}.feature
```

Examples:
- `features/slice-1-data-ingestion.feature`
- `features/slice-3-portfolio-dashboard.feature`
- `features/slice-5-report-generation.feature`

---

## Tag Reference

| Tag | Purpose | When to Use |
|-----|---------|-------------|
| `@slice-N` | Slice association | Every scenario — enables per-slice test runs |
| `@critical` | Must-pass tests | Goal achievement, core business logic |
| `@frontend` | UI tests | Scenarios requiring browser interaction |
| `@data-correctness` | Data tests | Calculations, transformations, aggregations |
| `@edge-cases` | Boundary tests | Unusual inputs, error conditions |
| `@performance` | Performance tests | Timing, load, scalability tests |
| `@smoke` | Quick validation | Subset of tests for fast feedback |
| `@goal-achievement` | End-to-end goal | The binary pass/fail workflow test |
| `@wip` | Work in progress | Scenarios not yet fully implemented |
